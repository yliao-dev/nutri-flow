import customtkinter as ctk
from PIL import Image
import json


class IngredientCard(ctk.CTkFrame):
    # Class-level attribute to keep track of the currently selected card for detail view
    currently_selected_card = None

    def __init__(self, parent, index, ingredient_data, update_selected_data_callback, selection_type, width=400, height=500):
        super().__init__(parent, corner_radius=10, width=width, height=height)

        # Ingredient data (loaded from JSON)
        self.ingredient_data = ingredient_data
        self.index = index
        self.update_selected_data_callback = update_selected_data_callback  # Store the callback function
        self.selected = False
        self.selection_type = selection_type  # 'intake' or 'detail'

        # Layout of the card (using grid for better control)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Highlight border to indicate selection
        self.highlight_color = "#2980B9"
        self.default_border_color = self.cget("fg_color")
        
        # Bind events to the parent frame
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.toggle_select)  # Bind selection to the whole frame

        # Initialize elements as None, we'll add them later
        self.card_label = None
        self.protein_label = None
        self.carbs_label = None
        self.calories_label = None
        self.image_label = None

    def add_name(self):
        """Add the ingredient name label."""
        if not self.card_label:
            self.card_label = ctk.CTkLabel(
                self,
                text=f"{self.ingredient_data['name'].title()}",
                font=("Arial", 14, "bold"),
            )
            self.card_label.grid(row=0, column=0, pady=(10, 0))

    def add_nutrition_data(self):
        """Add the nutritional information labels."""
        if not self.protein_label:
            self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['protein']}g")
            self.protein_label.grid(row=1, column=0, pady=(0, 5))

        if not self.carbs_label:
            self.carbs_label = ctk.CTkLabel(self, text=f"Carbs: {self.ingredient_data['carbohydrates']}g")
            self.carbs_label.grid(row=2, column=0, pady=(0, 5))

        if not self.calories_label:
            self.calories_label = ctk.CTkLabel(self, text=f"Calories: {self.ingredient_data['calories']}kcal")
            self.calories_label.grid(row=3, column=0, pady=(0, 10))

    def add_image(self, image_path=None):
        """Add the ingredient image if image_path is provided."""
        if image_path and not self.image_label:
            img = Image.open(image_path).convert("RGBA")
            img = img.resize((100, 100))
            img_ctk = ctk.CTkImage(img, size=(100, 100))
            self.image_label = ctk.CTkLabel(self, image=img_ctk, text=None)
            self.image_label.image = img_ctk
            self.image_label.grid(row=4, column=0, pady=(10, 5))

    def toggle_select(self, event=None):
        """Toggle selection of the ingredient card based on the selection type."""
        if self.selection_type == 'intake':
            self.toggle_select_intake(event)
        elif self.selection_type == 'detail':
            self.toggle_select_detail(event)

    def toggle_select_intake(self, event=None):
        """Toggle selection of the ingredient card for the intake screen."""
        if event is not None:
            event.widget.focus_set()  # Focus on the clicked widget to prevent other events from interfering

        self.selected = not self.selected
        border_color = self.highlight_color if self.selected else self.default_border_color
        self.configure(fg_color=border_color)

        if self.selected:
            self.update_selected_data_callback(self.ingredient_data, add=True)
        else:
            self.update_selected_data_callback(self.ingredient_data, add=False)

    def toggle_select_detail(self, event=None):
        """Allow only one card to be selected for the ingredient details screen."""
        # If another card is already selected, deselect it
        if IngredientCard.currently_selected_card and IngredientCard.currently_selected_card != self:
            IngredientCard.currently_selected_card.deselect()
        # Select the current card
        self.selected = True
        self.configure(fg_color=self.highlight_color)

        # Update the class-level variable to keep track of the currently selected card
        IngredientCard.currently_selected_card = self
        self.update_selected_data_callback(self.ingredient_data)

    def deselect(self):
        """Deselect the ingredient card."""
        self.selected = False
        self.configure(fg_color=self.default_border_color)

    def on_hover(self, event=None):
        """Change the appearance of the card on hover."""
        if not self.selected:
            self.configure(fg_color="lightgrey")

    def on_leave(self, event=None):
        """Reset the appearance of the card when the hover ends."""
        if not self.selected:
            self.configure(fg_color=self.default_border_color)


# Function to load the ingredients data from the JSON file
def load_ingredients_data():
    with open("data/ingredients.json", "r") as file:
        data = json.load(file)

    ingredients = []
    for ingredient_name, details in data.items():
        # Add the ingredient name to each ingredient's details
        ingredient_details = details.copy()
        ingredient_details["name"] = ingredient_name
        ingredients.append(ingredient_details)

    return ingredients