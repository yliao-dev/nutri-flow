import customtkinter as ctk
from ui.sidebar_frame import Sidebar
from ui.home_ui.home_screen import HomeScreen
from ui.ingredients_ui.ingredient_screen import IngredientScreen
from ui.data_ui.data_screen import DataScreen
from viewmodel.progress_viewmodel import ProgressViewModel
from model.user_profile import UserProfile
from model.progress_model import ProgressModel


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
WIDTH = 1200
HEIGHT = 800

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

        # Create the UserProfile and other components...
        user_profile = UserProfile(weight=75, goal_protein=150, goal_carbs=375, goal_calories=2500)
        progress_model = ProgressModel(user_profile)
        progress_view_model = ProgressViewModel(user_profile, progress_model)

        # Initialize screens
        self.screens = {
            "Home": HomeScreen(self, progress_view_model),
            "Ingredients": IngredientScreen(self),
            "Data": DataScreen(self)
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

if __name__ == "__main__":
    window = App()
    window.mainloop()