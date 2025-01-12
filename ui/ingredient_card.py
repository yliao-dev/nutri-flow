import customtkinter as ctk
from PIL import Image, ImageTk
import json

class IngredientCard(ctk.CTkFrame):
    def __init__(self, parent, index, ingredient_data, update_selected_data_callback, width=400, height=500):
        super().__init__(parent, corner_radius=10, width=width, height=height)

        # Ingredient data (loaded from JSON)
        self.ingredient_data = ingredient_data
        self.index = index
        self.update_selected_data_callback = update_selected_data_callback  # Store the callback function
        self.selected = False
        
        # Layout of the card (using grid for better control)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Ingredient Card Title (e.g., Ingredient Name)
        self.card_label = ctk.CTkLabel(
            self, 
            text=f"{self.ingredient_data['name'].title()}", 
            font=("Arial", 14, "bold")
        )
        self.card_label.grid(row=0, column=0, pady=(10, 0))

        # Nutritional Information
        self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['protein']}g")
        self.protein_label.grid(row=1, column=0, pady=(0, 5))

        self.carbs_label = ctk.CTkLabel(self, text=f"Carbs: {self.ingredient_data['carbohydrates']}g")
        self.carbs_label.grid(row=2, column=0, pady=(0, 5))

        self.calories_label = ctk.CTkLabel(self, text=f"Calories: {self.ingredient_data['calories']}kcal")
        self.calories_label.grid(row=3, column=0, pady=(0, 10))

        # Load and display the image (if image_path is provided)
        if 'image' in self.ingredient_data:
            self.display_image(self.ingredient_data['image'])

        # Checkbox (Optional)
        self.checkbox = ctk.CTkCheckBox(self, text="")
        self.checkbox.configure(command=self.toggle_select)
        self.checkbox.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="se")
        
    def display_image(self, image_path):
        """Load and display the image using CTkImage."""
        # Open the image using PIL
        img = Image.open(image_path).convert("RGBA")  # Ensure transparency is preserved
        img = img.resize((100, 100))  # Resize image to fit the card
        
        # Convert to CTkImage
        img_ctk = ctk.CTkImage(img, size=(100, 100))

        # Create a label to display the image with no text
        self.image_label = ctk.CTkLabel(self, image=img_ctk, text=None)  # Set text to empty to avoid overlay
        self.image_label.image = img_ctk  # Keep a reference to the image
        self.image_label.grid(row=4, column=0, pady=(10, 5))
    
    def toggle_select(self):
        self.selected = not self.selected
        if self.selected:
            # Add ingredient to the selection using the callback
            self.update_selected_data_callback(self.ingredient_data, add=True)
        else:
            # Remove ingredient from the selection using the callback
            self.update_selected_data_callback(self.ingredient_data, add=False)

    def deselect(self):
        """Deselect the ingredient card."""
        self.selected = False
        self.checkbox.deselect()


# Function to load the ingredients data from the JSON file
def load_ingredients_data():
    with open('data/ingredients.json', 'r') as file:
        data = json.load(file)
    
    ingredients = []
    for ingredient_name, details in data.items():
        # Add the ingredient name to each ingredient's details
        ingredient_details = details.copy()
        ingredient_details["name"] = ingredient_name
        ingredients.append(ingredient_details)
    
    return ingredients