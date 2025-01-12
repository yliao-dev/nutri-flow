import customtkinter as ctk
from PIL import Image
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

        # Highlight border to indicate selection
        self.highlight_color = "#2980B9"
        self.default_border_color = self.cget("fg_color")
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

        # Ingredient Card Title (e.g., Ingredient Name)
        self.card_label = ctk.CTkLabel(
            self,
            text=f"{self.ingredient_data['name'].title()}",
            font=("Arial", 14, "bold"),
        )
        self.card_label.grid(row=0, column=0, pady=(10, 0))
        self.card_label.bind("<Button-1>", self.toggle_select)

        # Nutritional Information
        self.protein_label = ctk.CTkLabel(self, text=f"Protein: {self.ingredient_data['protein']}g")
        self.protein_label.grid(row=1, column=0, pady=(0, 5))
        self.protein_label.bind("<Button-1>", self.toggle_select)

        self.carbs_label = ctk.CTkLabel(self, text=f"Carbs: {self.ingredient_data['carbohydrates']}g")
        self.carbs_label.grid(row=2, column=0, pady=(0, 5))
        self.carbs_label.bind("<Button-1>", self.toggle_select)

        self.calories_label = ctk.CTkLabel(self, text=f"Calories: {self.ingredient_data['calories']}kcal")
        self.calories_label.grid(row=3, column=0, pady=(0, 10))
        self.calories_label.bind("<Button-1>", self.toggle_select)

        # Load and display the image (if image_path is provided)
        if "image" in self.ingredient_data:
            self.display_image(self.ingredient_data["image"])

        # Enable dragging
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.perform_drag)

    def display_image(self, image_path):
        """Load and display the image using CTkImage."""
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((100, 100))
        img_ctk = ctk.CTkImage(img, size=(100, 100))
        self.image_label = ctk.CTkLabel(self, image=img_ctk, text=None)
        self.image_label.image = img_ctk
        self.image_label.grid(row=4, column=0, pady=(10, 5))
        self.image_label.bind("<Button-1>", self.toggle_select)

    def toggle_select(self, event=None):
        """Toggle selection of the ingredient card."""
        self.selected = not self.selected
        border_color = self.highlight_color if self.selected else self.default_border_color
        self.configure(fg_color=border_color)

        if self.selected:
            self.update_selected_data_callback(self.ingredient_data, add=True)
        else:
            self.update_selected_data_callback(self.ingredient_data, add=False)

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

    # Dragging-related methods
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def perform_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.place_configure(relx=self.winfo_x() + dx, rely=self.winfo_y() + dy)


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