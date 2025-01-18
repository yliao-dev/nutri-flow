import customtkinter as ctk
from ui.home_ui.progress_frame import ProgressFrame
from ui.ingredients_ui.ingredient_card import IngredientCard, load_ingredients_data
from ui.home_ui.bottom_frame import BottomFrame
from PIL import Image

DARK_MODE_IMG = "data/dark-mode.png"

class HomeScreen(ctk.CTkFrame):
    def __init__(self, master, nutrition_view_model):
        super().__init__(master)

        self.nutrition_view_model = nutrition_view_model
        self.ingredients_data = load_ingredients_data()
        self.user_goals = {
            "protein": self.nutrition_view_model.user_profile.goal_protein,
            "carbohydrate": self.nutrition_view_model.user_profile.goal_carbohydrates,
            "fat": self.nutrition_view_model.user_profile.goal_fat,
            "calories": self.nutrition_view_model.user_profile.goal_calories,
        }

        self.progress_frames = {}  # Dictionary to store the progress frames
        self.ingredient_cards = []  # List to store IngredientCard instances

        self.initialize_ui()

    def initialize_ui(self):
        self.label = ctk.CTkLabel(self, text="Nutrition Progress", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=1, columnspan=1, pady=10, sticky="nsew") 
        self.weight_label = ctk.CTkLabel(
                    self,
                    font=("Arial", 16, "bold"),
                    text=f"Weight: {self.nutrition_view_model.user_profile.weight}kg",
                    fg_color="transparent", 
                )
        self.weight_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        # Appearance Mode Selector (using a single image)
        self.mode_img = ctk.CTkImage(light_image=Image.open(DARK_MODE_IMG), size=(40, 40))
        self.mode_label = ctk.CTkLabel(
            self,
            text="", 
            image=self.mode_img, 
            fg_color="transparent", 
        )
        self.mode_label.bind("<Button-1>", lambda event: self.toggle_appearance_mode())
        # Prevent any hover effect
        self.mode_label.bind("<Enter>", lambda event: self.mode_label.configure(fg_color="transparent"))
        self.mode_label.bind("<Leave>", lambda event: self.mode_label.configure(fg_color="transparent"))
        self.mode_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
    
        # Configure the grid
        self.configure_grid()
       
        self.create_progress_frames()
        self.create_ingredients_frame()
        self.populate_ingredient_cards()
        self.create_bottom_frame()

    def configure_grid(self):
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="nutrition")
        self.grid_rowconfigure(1, weight=3, minsize=150)  # Adjusted minsize for better display
        self.grid_rowconfigure(2, weight=2)
        self.grid_rowconfigure(3, weight=1)

    def create_progress_frames(self):
        goal_names = ["protein", "carbohydrate", "fat"]
        consumed_values = self.nutrition_view_model.get_nutrition_data()
        goal_values = self.user_goals

        for index, goal_name in enumerate(goal_names):
            self.progress_frames[goal_name] = self.create_single_progress_frame(goal_name, index, consumed_values, goal_values)

    def create_single_progress_frame(self, goal_name, column_index, consumed_values, goal_values):
        progress_frame = ProgressFrame(
            master=self,
            goal_name=goal_name,
            goal_values=goal_values,
            consumed_value=consumed_values,
            update_callback=ProgressFrame.update_nutrition_label,
        )
        progress_frame.grid(row=1, column=column_index, padx=10, pady=10, sticky="nsew")
        return progress_frame

    def create_ingredients_frame(self):
        self.ingredients_frame = ctk.CTkFrame(self)
        self.ingredients_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.canvas = ctk.CTkCanvas(self.ingredients_frame, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.ingredients_frame, orientation="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def populate_ingredient_cards(self):
        for ingredient in self.ingredients_data:
            ingredient_card = IngredientCard(
                self.scrollable_frame,
                index=ingredient["id"],
                ingredient_data=ingredient,
                update_selected_data_callback=self.update_bottom_frame,
                selection_type="intake"
            )
            ingredient_card.add_name()
            ingredient_card.add_nutrition_data()
            ingredient_card.add_image(ingredient["image"])
            ingredient_card.add_custom_serving_size()
            ingredient_card.grid(row=0, column=ingredient["id"], padx=5, pady=5, sticky="nsew")
            self.ingredient_cards.append(ingredient_card)

    def update_bottom_frame(self, ingredients_data, add):
        self.bottom_frame.update_selected_data(ingredients_data, add)

    def create_bottom_frame(self):
        self.bottom_frame = BottomFrame(
            master=self,
            nutrition_view_model=self.nutrition_view_model,
            update_intake_callback=self.update_intake,
            ingredient_cards=self.ingredient_cards,
        )
        self.bottom_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def update_intake(self, nutrition_data):
        # Update each progress frame with the new data
        for _, progress_frame in self.progress_frames.items():
            progress_frame.update(nutrition_data)
            
            
    def toggle_appearance_mode(self):
        """Toggle between light and dark mode when clicked."""
        current_mode = ctk.get_appearance_mode()

        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")  # Switch to light mode
        else:
            ctk.set_appearance_mode("Dark")  # Switch to dark mode