import customtkinter as ctk
import json

class IngredientCard(ctk.CTkFrame):
    def __init__(self, parent, index, ingredient_data, width=400, height=500):
        super().__init__(parent, corner_radius=10, width=width, height=height)

        # Ingredient data (loaded from JSON)
        self.ingredient_data = ingredient_data
        self.index = index
        print(self.index, self.ingredient_data)
        # Layout of the card (using grid for better control)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Ingredient Card Title (e.g., Ingredient Name)
        self.card_label = ctk.CTkLabel(self, text=f"{self.ingredient_data['name'].capitalize()}", font=("Arial", 12))
        self.card_label.grid(row=0, column=0, pady=(10, 0))

        # Nutritional Information
        self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['protein']}g")
        self.protein_label.grid(row=1, column=0, pady=(0, 5))

        self.carbs_label = ctk.CTkLabel(self, text=f"Carbs: {self.ingredient_data['carbohydrates']}g")
        self.carbs_label.grid(row=2, column=0, pady=(0, 5))

        self.calories_label = ctk.CTkLabel(self, text=f"Calories: {self.ingredient_data['calories']}kcal")
        self.calories_label.grid(row=3, column=0, pady=(0, 10))

        # Checkbox (Optional)
        self.checkbox = ctk.CTkCheckBox(self, text="")
        self.checkbox.grid(row=4, column=0, padx=5, pady=(0, 10), sticky="se")

# Function to load the ingredients data from the JSON file
def load_ingredient_data():
    with open('data/ingredients.json', 'r') as file:
        data = json.load(file)
    
    ingredients = []
    for ingredient_name, details in data.items():
        # Add the ingredient name to each ingredient's details
        ingredient_details = details.copy()
        ingredient_details["name"] = ingredient_name
        ingredients.append(ingredient_details)
    
    return ingredients