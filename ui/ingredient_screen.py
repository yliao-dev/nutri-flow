import customtkinter as ctk
from ui.ingredient_card import IngredientCard, load_ingredients_data


class IngredientScreen(ctk.CTkFrame):
    def __init__(self, parent, width=600, height=600):
        super().__init__(parent, width=width, height=height)

        # Load ingredient data
        self.ingredients_data = load_ingredients_data()
        self.selected_ingredients = []  # To keep track of selected ingredients

        # Initialize UI
        self.initialize_ui()

    def initialize_ui(self):
        # Configure the grid layout for the frame
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=3)  # Ingredient detail row
        self.grid_rowconfigure(2, weight=1)  # Ingredients frame row
        self.grid_columnconfigure(0, weight=1)

        # Title
        title = ctk.CTkLabel(self, text="Ingredients", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, pady=10, sticky="n")

        # Create the ingredients frame
        self.create_ingredients_frame()

        # Populate ingredient cards
        self.populate_ingredient_cards()

    def create_ingredients_frame(self):
        # Frame to hold the canvas and scrollbar
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

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

    def populate_ingredient_cards(self):
        self.ingredient_cards = []  # Store references to cards
        for index, ingredient in enumerate(self.ingredients_data):
            ingredient_card = IngredientCard(
                self.scrollable_frame,
                index=index,
                ingredient_data=ingredient,
                update_selected_data_callback=self.update_selected_ingredients,
            )
            ingredient_card.grid(row=0, column=index, padx=5, pady=5, sticky="nsew")
            self.ingredient_cards.append(ingredient_card)

    def update_selected_ingredients(self, ingredient, add=True):
        """Update the list of selected ingredients."""
        if add:
            if ingredient not in self.selected_ingredients:
                self.selected_ingredients.append(ingredient)
        else:
            if ingredient in self.selected_ingredients:
                self.selected_ingredients.remove(ingredient)

        # Debug print for testing (can be removed later)
        print("Selected Ingredients:", self.selected_ingredients)