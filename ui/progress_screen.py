import customtkinter as ctk
from ui.progress_frame import ProgressFrame
from ui.ingredient_card import IngredientCard, load_ingredient_data

class ProgressScreen(ctk.CTkFrame):
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model
        self.nutrition_manager = self.progress_view_model.nutrition_manager
        self.ingredients_data = load_ingredient_data()
        self.user_goals = {
            "protein": self.progress_view_model.user_profile.goal_protein,
            "carbohydrate": self.progress_view_model.user_profile.goal_carbs,
            "calories": self.progress_view_model.user_profile.goal_calories
        }

        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.configure_grid()
        self.create_progress_frames()
        self.create_ingredients_frame()

        self.selected_ingredients_label = ctk.CTkLabel(self, text="Selected Ingredients:", font=("Arial", 12))
        self.selected_ingredients_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.selected_nutrition_label = ctk.CTkLabel(self, text="Protein: 0g, Carbs: 0g, Calories: 0g", font=("Arial", 10))
        self.selected_nutrition_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals, state=ctk.DISABLED)
        self.update_button.grid(row=3, column=1, padx=10, pady=10)

        self.populate_ingredient_cards()

    def configure_grid(self):
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="nutrition")
        self.grid_rowconfigure(1, weight=3, minsize=100)
        self.grid_rowconfigure(2, weight=2)

    def create_progress_frames(self):
    # List of goal names and their corresponding columns
        goal_names = ["protein", "carbohydrate", "calories"]
        # Create a dictionary with all nutrient values for consumed and goal
        consumed_values = self.nutrition_manager.get_nutrition_data()
        goal_values = self.user_goals  # Assumed to be a dictionary with goal values for all nutrients
        
        for index, goal_name in enumerate(goal_names):
            self.create_single_progress_frame(goal_name, index, consumed_values, goal_values)

    def create_single_progress_frame(self, goal_name, column_index, consumed_values, goal_values):
        """Helper method to create a single progress frame."""
        # Create the progress frame for this nutrient
        progress_frame = ProgressFrame(
            master=self,
            goal_name=goal_name,
            goal_values=goal_values,  # Pass entire goal_values dictionary
            consumed_value=consumed_values,  # Pass entire consumed_values dictionary
            update_callback=ProgressFrame.update_nutrition_label
        )
        # Grid layout for the progress frame
        progress_frame.grid(row=1, column=column_index, padx=10, pady=10, sticky="nsew")
    
    
    def create_ingredients_frame(self):
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.canvas = ctk.CTkCanvas(self.ingredients_frame, bg="#ffffff", highlightthickness=3)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.ingredients_frame, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.selected_ingredients = []

    def populate_ingredient_cards(self):
        for ingredient in self.ingredients_data:
            ingredient_card = IngredientCard(self.scrollable_frame, ingredient['id'], ingredient, self.update_selected_data)
            ingredient_card.grid(row=0, column=ingredient['id'], padx=5, pady=5, sticky="nsew")

    def update_selected_data(self, ingredient_data, add=False):
        if add:
            if ingredient_data not in self.selected_ingredients:
                self.selected_ingredients.append(ingredient_data)
        else:
            if ingredient_data in self.selected_ingredients:
                self.selected_ingredients.remove(ingredient_data)

        self.update_selected_ingredients_label()
        self.update_button.configure(state=ctk.NORMAL if self.selected_ingredients else ctk.DISABLED)

    def update_selected_ingredients_label(self):
        selected_ingredients_text = self.format_ingredient_text(self.selected_ingredients)
        self.selected_ingredients_label.configure(text=f"Selected Ingredients: {', '.join([ingredient['name'] for ingredient in self.selected_ingredients])}")
        self.selected_nutrition_label.configure(text=selected_ingredients_text)

    def format_ingredient_text(self, ingredients):
        total_protein = round(sum([ingredient["protein"] for ingredient in ingredients]), 2)
        total_carbs = round(sum([ingredient["carbohydrates"] for ingredient in ingredients]), 2)
        total_calories = round(sum([ingredient["calories"] for ingredient in ingredients]), 2)

        return f"Protein: {total_protein}g, Carbs: {total_carbs}g, Calories: {total_calories}g"

    def update_goals(self):
        self.nutrition_manager.update_nutrition(self.selected_ingredients)
        nutrition_data = self.nutrition_manager.get_nutrition_data()
        # Update all progress frames with the same nutrition data
        self.protein_frame.update(nutrition_data)
        self.carbs_frame.update(nutrition_data)
        self.calories_frame.update(nutrition_data)
        
        self.update_selected_ingredients_label()
        self.reset_selection()

    def reset_selection(self):
        self.selected_ingredients = []
        for ingredient_card in self.scrollable_frame.winfo_children():
            if isinstance(ingredient_card, IngredientCard):
                ingredient_card.deselect()

        self.update_selected_ingredients_label()
        self.update_button.configure(state=ctk.DISABLED)