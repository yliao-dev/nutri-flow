import customtkinter as ctk
from ui.ingredient_card import IngredientCard, load_ingredient_data  # Import the IngredientCard class

class ProgressScreen(ctk.CTkFrame):
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model
        self.nutrition_manager = self.progress_view_model.nutrition_manager  # Use the nutrition_manager from the VM
        self.ingredients_data = load_ingredient_data()  # Ensure this is called early
        self.user_goals = {
            "protein": self.progress_view_model.user_profile.goal_protein,
            "carbohydrate": self.progress_view_model.user_profile.goal_carbs,
            "calories": self.progress_view_model.user_profile.goal_calories
        }

        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid weights for columns and rows
        self.configure_grid()

        # Protein, Carbs, Calories Frames
        self.create_nutrition_frames()

        # Ingredients Frame with Scrollable Content
        self.create_ingredients_frame()

        # Selected Ingredients Label
        self.selectedGoals = ctk.CTkLabel(self, text="Selected Ingredients: None\nProtein: 0 g\nCarbohydrate: 0 g\nCalories: 0 g")
        self.selectedGoals.grid(row=3, column=0, padx=10, pady=10)

        # Update Goals Button
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals, state=ctk.DISABLED)
        self.update_button.grid(row=3, column=1, padx=10, pady=10)

        # Populate ingredient cards
        self.populate_ingredient_cards()

    def configure_grid(self):
        # Configure grid weights for columns
        self.grid_columnconfigure(0, weight=4)  # 80% of the row width for the selectedGoals label
        self.grid_columnconfigure(1, weight=1)  # 20% of the row width for the button

        # Configure rows to have weight for dynamic resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)  # Ensuring enough space for ingredient text

    def create_nutrition_frames(self):
        # Protein, Carbs, Calories Frames
        self.protein_label = self.create_nutrition_label("protein", 0)
        self.carbs_label = self.create_nutrition_label("carbohydrate", 1)
        self.calories_label = self.create_nutrition_label("calories", 2)

    def create_nutrition_label(self, goal_name, column):
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=column, padx=10, pady=10, sticky="nsew")

        label = ctk.CTkLabel(frame, text=f"{goal_name.capitalize()} Goal: {self.user_goals[goal_name]}g | Consumed: 0g | 0.0%")
        label.pack(pady=10)

        return label

    def create_ingredients_frame(self):
        # Ingredients Frame with Scrollable Content
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

        self.selected_ingredients = []  # To store selected ingredients

    def populate_ingredient_cards(self):
        # Loop through the ingredient data and create cards
        for ingredient in self.ingredients_data:
            ingredient_card = IngredientCard(self.scrollable_frame, ingredient['id'], ingredient, self.update_selected_data)
            ingredient_card.grid(row=0, column=ingredient['id'], padx=5, pady=5, sticky="nsew")

    def update_selected_data(self, ingredient_data, add=False):
        # Add or remove ingredient from selected_ingredients
        if add:
            if ingredient_data not in self.selected_ingredients:
                self.selected_ingredients.append(ingredient_data)
        else:
            if ingredient_data in self.selected_ingredients:
                self.selected_ingredients.remove(ingredient_data)
        
        # Update the selected ingredients label and nutritional info
        self.update_selected_ingredients_label()

        # Enable/Disable the "Update Goals" button
        self.update_button.configure(state=ctk.NORMAL if self.selected_ingredients else ctk.DISABLED)

    def update_selected_ingredients_label(self):
        selected_ingredients_text = self.format_ingredient_text(self.selected_ingredients)
        self.selectedGoals.configure(text=selected_ingredients_text)

    def format_ingredient_text(self, ingredients):

        ingredient_names = [ingredient["name"].capitalize() for ingredient in ingredients]
        ingredient_names_text = f"Ingredients selected: {', '.join(ingredient_names)}"

        total_protein = round(sum([ingredient["protein"] for ingredient in ingredients]), 2)
        total_carbs = round(sum([ingredient["carbohydrates"] for ingredient in ingredients]), 2)
        total_calories = round(sum([ingredient["calories"] for ingredient in ingredients]), 2)

        # Building the nutritional data display
        nutritional_info = (
            f"\nProtein: {total_protein} g\n"
            f"Carbohydrate: {total_carbs} g\n"
            f"Calories: {total_calories} g"
        )

        return f"{ingredient_names_text}{nutritional_info}"

    def update_goals(self):
        self.update_progress_labels()
        self.update_selected_ingredients_label()
        self.reset_selection()
        print("Update Goals clicked!")

    def update_progress_labels(self):
        # Update the nutrition manager with selected ingredients
        self.nutrition_manager.update_nutrition(self.selected_ingredients)

        # Retrieve the nutrition data from the manager
        nutrition_data = self.nutrition_manager.get_nutrition_data()

        # Retrieve user goals
        protein_goal = self.user_goals.get('protein', 0)
        carbs_goal = self.user_goals.get('carbohydrate', 0)
        calories_goal = self.user_goals.get('calories', 0)

        # Calculate and update progress for each goal
        self.update_nutrition_label(self.protein_label, 'protein', protein_goal, nutrition_data)
        self.update_nutrition_label(self.carbs_label, 'carbohydrate', carbs_goal, nutrition_data)
        self.update_nutrition_label(self.calories_label, 'calories', calories_goal, nutrition_data)

    def update_nutrition_label(self, label, goal_name, goal_value, nutrition_data):
        # Calculate percentage and update the label
        consumed_value = round(nutrition_data[goal_name], 2)
        percentage = self.nutrition_manager.calculate_percentage(goal_value, consumed_value)
        label.configure(
            text=f"{goal_name.capitalize()} Goal: {goal_value}g | Consumed: {consumed_value}g | {round(percentage, 2)}%"
        )
        
    def reset_selection(self):
        # Reset the selected ingredients list and deselect cards
        self.selected_ingredients = []
        for ingredient_card in self.scrollable_frame.winfo_children():
            if isinstance(ingredient_card, IngredientCard):
                ingredient_card.deselect()  # Call deselect method for each card
        
        # Update the selected ingredients label and disable the update button
        self.update_selected_ingredients_label()
        self.update_button.configure(state=ctk.DISABLED)