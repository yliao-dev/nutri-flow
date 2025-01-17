import customtkinter as ctk
from ui.ingredients_ui.ingredient_card import IngredientCard


class BottomFrame(ctk.CTkFrame):
    def __init__(self, master, nutrition_view_model, update_intake_callback, ingredient_cards):
        super().__init__(master)

        self.nutrition_view_model = nutrition_view_model
        self.update_intake_callback = update_intake_callback
        self.ingredient_cards = ingredient_cards
        self.selected_ingredients = []

        self.initialize_ui()

    def initialize_ui(self):
        # Configure grid for proper spacing and row/column weights
        self.grid_rowconfigure(0, weight=1)  # Row for the labels
        self.grid_rowconfigure(1, weight=3)  # Row for the button with higher weight to allow expansion
        self.grid_columnconfigure(0, weight=1)  # Column for the first label
        self.grid_columnconfigure(1, weight=1)  # Column for the second label (nutrition label)

        # Re-add the labels
        self.selected_ingredients_label = ctk.CTkLabel(self, text="Selected Ingredients:", font=("Arial", 12))
        self.selected_ingredients_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.selected_nutrition_label = ctk.CTkLabel(self, text="Protein: 0g | Carbs: 0g | Calories: 0g", font=("Arial", 12))
        self.selected_nutrition_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")  # Align to the east

        # Use the existing update_button and make it take the entire space (row 1)
        self.update_button = ctk.CTkButton(self, hover_color="#2c2c2c", text="Update Intake", command=self.update_intake, state=ctk.DISABLED)
        self.update_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")  # Button in a separate row, spanning both columns

        # Ensure the button expands both vertically and horizontally by setting weight to 1
        self.grid_rowconfigure(1, weight=3)  # Row with the button has weight=3 to allow it to expand
        self.grid_columnconfigure(0, weight=1)  # Column with the button has weight=1
        self.grid_columnconfigure(1, weight=1)  # Column for the button has weight=1 for the same grid

         
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
        total_protein = round(sum([ingredient['nutrition']["protein"] for ingredient in ingredients]), 2)
        total_carbs = round(sum([ingredient['nutrition']["carbohydrates"] for ingredient in ingredients]), 2)
        total_calories = round(sum([ingredient['nutrition']["calories"] for ingredient in ingredients]), 2)

        return f"Protein: {total_protein}g | Carbs: {total_carbs}g | Calories: {total_calories}g"

    def update_intake(self):
        self.nutrition_view_model.update_nutrition(self.selected_ingredients)
        nutrition_data = self.nutrition_view_model.get_nutrition_data()
        # Call the callback to update progress frames in HomeScreen
        self.update_intake_callback(nutrition_data)

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