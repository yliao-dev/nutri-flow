import customtkinter as ctk
from PIL import Image
import json
import tkinter as tk

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
        
        # Initialize elements as None, we'll add them later
        self.card_label = None
        self.protein_label = None
        self.carbs_label = None
        self.fat_label = None
        self.image_label = None

    def add_name(self):
        """Add the ingredient name label."""
        if not self.card_label:
            self.card_label = ctk.CTkLabel(
                self,
                text=f"{self.ingredient_data['name'].replace('_', ' ').title()}",
                font=("Arial", 14, "bold"),
            )
            self.card_label.grid(row=0, column=0, pady=(10, 0))
            # Bind hover and select events to the name label
            self.card_label.bind("<Enter>", self.on_hover)
            self.card_label.bind("<Leave>", self.on_leave)
            self.card_label.bind("<Button-1>", self.toggle_select)

    def add_custom_serving_size(self):
        """Add an editable entry for the custom serving size in grams."""
        if not hasattr(self, 'serving_size_entry'):  # Avoid creating multiple entries
            self.serving_size_var = ctk.StringVar(value="100")  # Initialize the serving size variable
            validate_command = self.register(self.validate_serving_size_input)
            # Create the entry widget for serving size
            self.serving_size_entry = ctk.CTkEntry(
                self,
                width=200,
                font=("Arial", 12),
                placeholder_text="Enter serving size in grams",
                textvariable=self.serving_size_var,
                validate="key",  # Enable validation for each key press
                validatecommand=(validate_command, "%P")
            )
            # Place it in the grid row after the image
            self.serving_size_entry.grid(row=5, column=0, pady=(10, 0))
            
    #TODO: everytime on_serving_size_change is called, update the ingredient.json file
    def on_serving_size_change(self, event=None):
        """Handle changes to the serving size when the user finishes editing."""
        new_serving_size = self.serving_size_var.get()
        try:
            new_serving_size = float(new_serving_size)
            self.ingredient_data["custom_serving_size"] = new_serving_size
            # print(f"Updated serving size: {new_serving_size} grams")
        except ValueError:
            print("Invalid serving size entered.")
    
    def validate_serving_size_input(self, value):
        """Validate the input for the serving size entry."""
        # Allow only digits and one decimal point
        if value == "" or value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit()):
            return True
        return False
    
    def add_nutrition_data(self):
        """Add the nutritional information labels."""
        if not self.protein_label:
            self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['nutrition']['protein']}g")
            self.protein_label.grid(row=1, column=0, pady=(0, 5))
            # Bind hover and select events to the protein label
            self.protein_label.bind("<Enter>", self.on_hover)
            self.protein_label.bind("<Leave>", self.on_leave)
            self.protein_label.bind("<Button-1>", self.toggle_select)

        if not self.carbs_label:
            self.carbs_label = ctk.CTkLabel(self, text=f"Carbs: {self.ingredient_data['nutrition']['carbohydrates']}g")
            self.carbs_label.grid(row=2, column=0, pady=(0, 5))
            # Bind hover and select events to the carbs label
            self.carbs_label.bind("<Enter>", self.on_hover)
            self.carbs_label.bind("<Leave>", self.on_leave)
            self.carbs_label.bind("<Button-1>", self.toggle_select)

        if not self.fat_label:
            self.fat_label = ctk.CTkLabel(self, text=f"Fat: {self.ingredient_data['nutrition']['fat']}g")
            self.fat_label.grid(row=3, column=0, pady=(0, 10))
            # Bind hover and select events to the fat label
            self.fat_label.bind("<Enter>", self.on_hover)
            self.fat_label.bind("<Leave>", self.on_leave)
            self.fat_label.bind("<Button-1>", self.toggle_select)

    def add_image(self, image_path=None):
        """Add the ingredient image if image_path is provided."""
        if image_path and not self.image_label:
            img = Image.open(image_path).convert("RGBA")
            img = img.resize((100, 100))
            img_ctk = ctk.CTkImage(img, size=(100, 100))
            self.image_label = ctk.CTkLabel(self, image=img_ctk, text=None)
            self.image_label.image = img_ctk
            self.image_label.grid(row=4, column=0, pady=(10, 5))
            # Bind hover and select events to the image label
            self.image_label.bind("<Enter>", self.on_hover)
            self.image_label.bind("<Leave>", self.on_leave)
            self.image_label.bind("<Button-1>", self.toggle_select)

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