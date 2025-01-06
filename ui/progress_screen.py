import customtkinter as ctk
from model.user_profile import NutritionData
from ui.ingredient_card import IngredientCard, load_ingredient_data  # Import the IngredientCard class

class ProgressScreen(ctk.CTkFrame):
    def __init__(self, master, progress_view_model):
        super().__init__(master)

        self.progress_view_model = progress_view_model
        self.ingredients_data = load_ingredient_data()  # Ensure this is called early
        self.user_goals = {
            "protein": self.progress_view_model.user_profile.goal_protein,
            "carbs": self.progress_view_model.user_profile.goal_carbs,
            "calories": self.progress_view_model.user_profile.goal_calories
        }

        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid weights for columns
        self.grid_columnconfigure(0, weight=4)  # 80% of the row width for the selectedGoals label
        self.grid_columnconfigure(1, weight=1)  # 20% of the row width for the button

        # Configure rows to have weight for dynamic resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=2)  # Ensuring enough space for ingredient text

        # Protein Frame
        self.protein_frame = ctk.CTkFrame(self)
        self.protein_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.protein_label = ctk.CTkLabel(self.protein_frame, text=f"Protein Goal: {self.user_goals['protein']}g | Consumed: 0g | 0.0%")
        self.protein_label.pack(pady=10)

        # Carbs Frame
        self.carbs_frame = ctk.CTkFrame(self)
        self.carbs_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.carbs_label = ctk.CTkLabel(self.carbs_frame, text=f"Carbs Goal: {self.user_goals['carbs']}g | Consumed: 0g | 0.0%")
        self.carbs_label.pack(pady=10)

        # Calories Frame
        self.calories_frame = ctk.CTkFrame(self)
        self.calories_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
        self.calories_label = ctk.CTkLabel(self.calories_frame, text=f"Calories Goal: {self.user_goals['calories']} | Consumed: 0 | 0.0%")
        self.calories_label.pack(pady=10)

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
        self.selectedGoals = ctk.CTkLabel(self, text="Selected Ingredients: None")
        self.selectedGoals.grid(row=3, column=0, padx=10, pady=10)

        # Populate ingredient cards
        self.populate_ingredient_cards()

        # Update Goals Button
        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals, state=ctk.DISABLED, fg_color=None)
        self.update_button.grid(row=3, column=1, padx=10, pady=10)

    def populate_ingredient_cards(self):
        # Loop through the ingredient data and create cards using the 'id' as a reference
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
        
        # Update the selected ingredients label and nutritional info
        selected_ingredients_text = self.format_ingredient_text(self.selected_ingredients)
        self.selectedGoals.configure(text=selected_ingredients_text)
        # Enable/Disable the "Update Goals" button
        if self.selected_ingredients:
            self.update_button.configure(state=ctk.NORMAL)
        else:
            self.update_button.configure(state=ctk.DISABLED)

    def format_ingredient_text(self, ingredients):
        # Format selected ingredients with nutritional values and totals
        if not ingredients:
            return "None"

        ingredient_names = [ingredient["name"].capitalize() for ingredient in ingredients]
        ingredient_names_text = f"Ingredients selected: {', '.join(ingredient_names)}"

        total_protein = sum([ingredient["protein"] for ingredient in ingredients])
        total_carbs = sum([ingredient["carbohydrates"] for ingredient in ingredients])
        total_calories = sum([ingredient["calories"] for ingredient in ingredients])

        # Formatting values with 2 decimal precision
        formatted_protein = round(total_protein, 2)
        formatted_carbs = round(total_carbs, 2)
        formatted_calories = round(total_calories, 2)

        # Building the nutritional data display
        nutritional_info = (
            f"\nProtein: {formatted_protein} g\n"
            f"Carbs: {formatted_carbs} g\n"
            f"Calories: {formatted_calories} g"
        )

        return f"{ingredient_names_text}{nutritional_info}"

    def update_goals(self):
        self.update_progress_labels()

        selected_ingredients_text = self.format_ingredient_text(self.selected_ingredients)
        self.selectedGoals.configure(text=selected_ingredients_text)

        self.reset_selection()
        print("Update Goals clicked!")


    def update_progress_labels(self):
        # Recalculate the progress for each goal
        total_protein = sum([ingredient["protein"] for ingredient in self.selected_ingredients])
        total_carbs = sum([ingredient["carbohydrates"] for ingredient in self.selected_ingredients])
        total_calories = sum([ingredient["calories"] for ingredient in self.selected_ingredients])

        protein_percentage = (total_protein / self.user_goals['protein']) * 100 if self.user_goals['protein'] else 0
        carbs_percentage = (total_carbs / self.user_goals['carbs']) * 100 if self.user_goals['carbs'] else 0
        calories_percentage = (total_calories / self.user_goals['calories']) * 100 if self.user_goals['calories'] else 0

        # Update the labels with the recalculated values
        self.protein_label.configure(
            text=f"Protein Goal: {self.user_goals['protein']}g | Consumed: {round(total_protein, 2)}g | {round(protein_percentage, 2)}%"
        )

        self.carbs_label.configure(
            text=f"Carbs Goal: {self.user_goals['carbs']}g | Consumed: {round(total_carbs, 2)}g | {round(carbs_percentage, 2)}%"
        )

        self.calories_label.configure(
            text=f"Calories Goal: {self.user_goals['calories']} | Consumed: {round(total_calories, 2)} | {round(calories_percentage, 2)}%"
        )
        
    def reset_selection(self):
        # Reset the selected ingredients list
        self.selected_ingredients = []
        # Reset ingredient card selections (unselect all cards)
        for ingredient_card in self.scrollable_frame.winfo_children():
            if isinstance(ingredient_card, IngredientCard):
                ingredient_card.deselect()  # Call deselect method for each card
        # Update the selected ingredients label
        selected_ingredients_text = self.format_ingredient_text(self.selected_ingredients)
        self.selectedGoals.configure(text=selected_ingredients_text)

        # Disable the update button
        self.update_button.configure(state=ctk.DISABLED)