import customtkinter as ctk
from ui.ingredient_card import IngredientCard


class BottomFrame(ctk.CTkFrame):
    def __init__(self, master, nutrition_manager, update_goals_callback, ingredient_cards):
        super().__init__(master)

        self.nutrition_manager = nutrition_manager
        self.update_goals_callback = update_goals_callback
        self.ingredient_cards = ingredient_cards
        self.selected_ingredients = []

        self.initialize_ui()

    def initialize_ui(self):
        self.selected_ingredients_label = ctk.CTkLabel(self, text="Selected Ingredients:", font=("Arial", 12))
        self.selected_ingredients_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.selected_nutrition_label = ctk.CTkLabel(
            self, text="Protein: 0g | Carbs: 0g | Calories: 0g", font=("Arial", 12)
        )
        self.selected_nutrition_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.update_button = ctk.CTkButton(self, text="Update Goals", command=self.update_goals, state=ctk.DISABLED)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

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
        self.selected_ingredients_label.configure(
            text=f"Selected Ingredients: {', '.join([ingredient['name'] for ingredient in self.selected_ingredients])}"
        )
        self.selected_nutrition_label.configure(text=selected_ingredients_text)

    def format_ingredient_text(self, ingredients):
        total_protein = round(sum([ingredient["protein"] for ingredient in ingredients]), 2)
        total_carbs = round(sum([ingredient["carbohydrates"] for ingredient in ingredients]), 2)
        total_calories = round(sum([ingredient["calories"] for ingredient in ingredients]), 2)

        return f"Protein: {total_protein}g | Carbs: {total_carbs}g | Calories: {total_calories}g"

    def update_goals(self):
        self.nutrition_manager.update_nutrition(self.selected_ingredients)
        nutrition_data = self.nutrition_manager.get_nutrition_data()

        # Call the callback to update progress frames in HomeScreen
        self.update_goals_callback(nutrition_data)

        # Reset selection after updating goals
        self.reset_selection()

    def reset_selection(self):
        self.selected_ingredients = []

        # Reset all ingredient cards
        for ingredient_card in self.ingredient_cards:
            if isinstance(ingredient_card, IngredientCard):
                ingredient_card.deselect()

        self.update_selected_ingredients_label()
        self.update_button.configure(state=ctk.DISABLED)