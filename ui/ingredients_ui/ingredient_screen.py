import customtkinter as ctk
from config import ADD_INGREDIENT_IMG
from ui.ingredients_ui.ingredient_card import IngredientCard
from PIL import Image
from model.data_manager import add_ingredient_to_ingredients_json, load_from_ingredients_json, sort_ingredients
from ui.ingredients_ui.add_ingredient_window import AddIngredientWindow  # Import new pop-up


class IngredientScreen(ctk.CTkFrame):
    def __init__(self, parent, width=600, height=600):
        super().__init__(parent, width=width, height=height)

        # Load ingredient data
        self.ingredients_data = load_from_ingredients_json()
        sorted_ingredients = sort_ingredients(self.ingredients_data, criteria="name", descending = False)
        self.ingredients_data = sorted_ingredients
        # Initialize UI
        self.initialize_ui()

    def initialize_ui(self):
        # Configure the grid layout for the frame
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=3)  # Ingredient detail row
        self.grid_rowconfigure(2, weight=1)  # Ingredients frame row
        self.grid_rowconfigure(3, weight=1)  # Add Ingredient frame row
        self.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(self, text="Ingredients", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, pady=10, sticky="n")

        self.create_ingredient_detail_frame()
        self.create_ingredients_frame()
        self.create_add_ingredient_frame()
        self.populate_ingredient_cards()

    def create_ingredients_frame(self):
        # Frame to hold the canvas and scrollbar
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        # Configure the grid for ingredients_frame
        self.ingredients_frame.grid_rowconfigure(0, weight=1)
        self.ingredients_frame.grid_columnconfigure(0, weight=1)

        # Canvas for scrolling
        self.canvas = ctk.CTkCanvas(self.ingredients_frame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")  # Place canvas in row 0

        # Scrollbar for horizontal scrolling
        self.scrollbar = ctk.CTkScrollbar(
            self.ingredients_frame, orientation="horizontal", command=self.canvas.xview
        )
        self.scrollbar.grid(row=1, column=0, sticky="ew")  # Place scrollbar in row 1, no gap

        # Configure the canvas to use the scrollbar
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create a scrollable frame inside the canvas
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.scrollable_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Update the scroll region whenever the scrollable frame changes size
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
    def create_ingredient_detail_frame(self):
        # Create a frame for displaying selected ingredient details
        self.ingredient_detail_frame = ctk.CTkFrame(self)
        self.ingredient_detail_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Configure grid layout for the detail frame
        self.ingredient_detail_frame.grid_rowconfigure(0, weight=1)  # Title row
        self.ingredient_detail_frame.grid_rowconfigure(1, weight=4)  # Image and details
        self.ingredient_detail_frame.grid_columnconfigure(0, weight=2)  # Image column
        self.ingredient_detail_frame.grid_columnconfigure(1, weight=1)  # Nutrition info column

        # Title widget: Centered at the top
        self.detail_title_label = ctk.CTkLabel(
            self.ingredient_detail_frame, text="Select an ingredient", font=("Arial", 16, "bold")
        )
        self.detail_title_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), sticky="n")

        # Image widget: Centered below the title
        self.detail_image_label = ctk.CTkLabel(self.ingredient_detail_frame, text="")
        self.detail_image_label.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        # Nutrition text widget: Placed on the right side
        self.detail_info_label = ctk.CTkLabel(self.ingredient_detail_frame, text="", font=("Arial", 12), justify="left")
        self.detail_info_label.grid(row=1, column=1, padx=10, pady=10, sticky="nw")
        
    def create_add_ingredient_frame(self):
        self.add_ingredient_frame = ctk.CTkFrame(self)
        self.add_ingredient_frame.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        self.add_ingredient_frame.grid_rowconfigure(0, weight=1)

        button_width = 120  # Set your preferred size
        button_height = 120  # Adjust height as needed

        # Load and resize image to exactly fit the button size
        img = Image.open(ADD_INGREDIENT_IMG)
        img = img.resize((button_width, button_height), Image.LANCZOS)

        add_ingredient_image = ctk.CTkImage(light_image=img, size=(button_width, button_height))

        # Create button with fixed size and stretched image
        self.add_ingredient_button = ctk.CTkButton(
            self.add_ingredient_frame,
            image=add_ingredient_image,
            text="",
            command=self.add_ingredient,
            width=button_width,
            height=button_height,
            fg_color="transparent",
            corner_radius=0
        )
        self.add_ingredient_button.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

    def update_selected_ingredient(self, ingredient_data):
        """Update the UI to display selected ingredient details."""
        self.detail_title_label.configure(text=ingredient_data["name"].replace('_', ' ').title())

        # Update the image if available
        if "image" in ingredient_data:
            img = Image.open(ingredient_data["image"]).resize((150, 150))
            img_ctk = ctk.CTkImage(img, size=(200, 200))
            self.detail_image_label.configure(image=img_ctk)
            self.detail_image_label.image = img_ctk
        else:
            self.detail_image_label.configure(image=None, text="No Image")

        # Update the nutritional information
        nutrition_text = (
            f"Protein: {ingredient_data['nutrition']['protein']}g\n"
            f"carbohydrate: {ingredient_data['nutrition']['carbohydrate']}g\n"
            f"Fat: {ingredient_data['nutrition']['fat']} g\n"
            f"Calories: {ingredient_data['nutrition']['calories']} kcal"
        )
        self.detail_info_label.configure(text=nutrition_text)


    def populate_ingredient_cards(self):
        self.ingredient_cards = []  # Store references to cards
        for index, ingredient in enumerate(self.ingredients_data):
            ingredient_card = IngredientCard(
                self.scrollable_frame,
                index=index,
                ingredient_data=ingredient,
                update_selected_data_callback=self.update_selected_ingredient,
                selection_type="detail",
                width=150,
                height=200,
            )
            ingredient_card.add_name()
            ingredient_card.add_image(ingredient["image"])

            ingredient_card.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
            self.ingredient_cards.append(ingredient_card)

    def add_ingredient(self):
        """Open the Add Ingredient pop-up window."""
        def on_confirm(new_ingredient):
            print("New Ingredient:", new_ingredient)
            add_ingredient_to_ingredients_json(new_ingredient)
        
        AddIngredientWindow(self, on_confirm)