import customtkinter as ctk
from ui.ingredients_ui.ingredient_card import IngredientCard
from model.data_manager import *

class BottomFrame(ctk.CTkFrame):
    def __init__(self, master, nutrition_view_model, update_intake_callback, sort_cards_callback, ingredient_cards):
        super().__init__(master)

        self.nutrition_view_model = nutrition_view_model
        self.update_intake_callback = update_intake_callback
        self.sort_cards_callback = sort_cards_callback
        self.ingredient_cards = ingredient_cards
        self.selected_ingredients = []

        self.initialize_ui()

    def initialize_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Sort dropdown on the most left side, row 0
        self.sorting_var = ctk.StringVar(value="Sort Cards by")
        self.sorting_menu = ctk.CTkOptionMenu(
            self, variable=self.sorting_var,
            values=["Frequency", "Alphabetical", "Recently Used"],
            command=self.toggle_sorting
        )
        self.sorting_menu.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Labels on row 1, left side
        self.selected_ingredients_label = ctk.CTkLabel(
            self, text="Selected Ingredients:", font=("Arial", 12)
        )
        self.selected_ingredients_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.selected_nutrition_label = ctk.CTkLabel(
            self, text="Protein: 0g | Carbs: 0g | Calories: 0g", font=("Arial", 12)
        )
        self.selected_nutrition_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Update Intake button on the most right side, taking 1/3 of the space, spanning both rows
        self.update_button = ctk.CTkButton(
            self, hover_color="#2c2c2c", text="Update Intake",
            command=self.update_intake, state=ctk.DISABLED
        )
        self.update_button.grid(row=0, column=2, rowspan=2, padx=10, pady=10, sticky="nsew")


    def toggle_sorting(self, selected_option):
        self.sort_cards_callback(selected_option)
    
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
            text=f"Selected Ingredients: {', '.join([ingredient['name'].replace('_', ' ').title() for ingredient in self.selected_ingredients])}"
        )
        self.selected_nutrition_label.configure(text=selected_ingredients_text)

    def format_ingredient_text(self, ingredients):
        total_protein = round(sum([
            ingredient['nutrition']["protein"] * (ingredient['custom_serving_size'] / ingredient['reference_serving_size'])
            for ingredient in ingredients
        ]), 2)
        
        total_carbohydrate = round(sum([
            ingredient['nutrition']["carbohydrate"] * (ingredient['custom_serving_size'] / ingredient['reference_serving_size'])
            for ingredient in ingredients
        ]), 2)
        
        total_fat = round(sum([
            ingredient['nutrition']["fat"] * (ingredient['custom_serving_size'] / ingredient['reference_serving_size'])
            for ingredient in ingredients
        ]), 2)
        
        return f"Protein: {total_protein}g | Carbohydrate: {total_carbohydrate}g | Fat: {total_fat}g"

    def update_intake(self):
        for ingredient_card in self.ingredient_cards:
            ingredient_card.on_serving_size_change()
        
        self.nutrition_view_model.update_nutrition(self.selected_ingredients)
        nutrition_data = self.nutrition_view_model.get_nutrition_data()
        self.update_intake_callback(nutrition_data)
        write_to_ingredients_json(self.selected_ingredients)
        write_to_user_config(self.nutrition_view_model)
        
        self.reset_selection()
        
    def reset_selection(self):
        self.selected_ingredients = []
        for ingredient_card in self.ingredient_cards:
            if isinstance(ingredient_card, IngredientCard):
                ingredient_card.deselect()

        self.update_selected_ingredients_label()
        self.update_button.configure(state=ctk.DISABLED)