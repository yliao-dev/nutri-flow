import json
import customtkinter as ctk
from ui.sidebar_frame import Sidebar
from ui.home_ui.home_screen import HomeScreen
from ui.ingredients_ui.ingredient_screen import IngredientScreen
from ui.data_ui.data_screen import DataScreen
from viewmodel.nutrition_viewmodel import NutritionViewModel
from model.user_profile import UserProfile
from model.nutrition_model import NutritionModel
from config import *

class App(ctk.CTk):
    """
    The main application window for NutriFlow.
    """
    def __init__(self):
        super().__init__()

        self.title("NutriFlow")
        self.center_window(WIDTH, HEIGHT)

        # Configure grid layout (2 columns: Sidebar + Main Content)
        self.grid_columnconfigure(0, weight=0)  # Fixed width for Sidebar
        self.grid_columnconfigure(1, weight=1)  # Expandable main content area
        self.grid_rowconfigure(0, weight=1)  # Expandable row

        # Tabs and event handling methods
        tabs = ["Home", "Ingredients", "Data"]

        # Create Sidebar and pass event handlers
        self.sidebar = Sidebar(
            parent=self,
            tabs=tabs, 
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        user_profile_data = self.read_user_profile_from_json()
        print(user_profile_data)
        user_profile = UserProfile(
            weight=user_profile_data["weight"],
            goal_protein=user_profile_data["goal_protein"],
            goal_carbohydrates=user_profile_data["goal_carbohydrates"],
            goal_fat=user_profile_data["goal_fat"],
            goal_calories=user_profile_data["goal_calories"]
        )
        nutrition_model = NutritionModel(user_profile)
        nutrition_view_model = NutritionViewModel(user_profile, nutrition_model)

        # Initialize screens
        self.screens = {
            "Home": HomeScreen(self, nutrition_view_model),
            "Ingredients": IngredientScreen(self),
            "Data": DataScreen(self, nutrition_view_model)
        }

        # Add screens to Column 1 and hide them initially
        for screen in self.screens.values():
            screen.grid(row=0, column=1, sticky="nsew")
            screen.grid_remove()  # Hide all screens initially

        # Display the Home screen by default
        self.current_screen = "Home"
        self.screens[self.current_screen].grid()

    def center_window(self, width, height):
        """Center the application window on the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def read_user_profile_from_json(self):
        try:
            with open(USER_CONFIG_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {USER_CONFIG_PATH} not found.")
            return {}

if __name__ == "__main__":
    window = App()
    window.mainloop()