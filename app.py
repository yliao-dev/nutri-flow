import customtkinter as ctk
from ui.progress_screen import ProgressScreen
from ui.ingredient_screen import IngredientScreen
from viewmodel.progress_viewmodal import ProgressViewModel
from model.user_profile import UserProfile
from model.progress_model import ProgressModel  # Correct import

ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

class App(ctk.CTk):
    """
    The main application window for NutriFlow.
    """
    def __init__(self):
        super().__init__()

        self.title("NutriFlow")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (2 columns: TabView + Screen)
        self.grid_columnconfigure(0, weight=0)  # Fixed width for TabView
        self.grid_columnconfigure(1, weight=1)  # Expandable screen area
        self.grid_rowconfigure(0, weight=1)  # Expandable row

        # Side TabView with vertical tabs
        self.tabview = ctk.CTkTabview(self, width=150)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Home")
        self.tabview.add("Ingredients")
        # self.tabview.add("Data")

        # Create the UserProfile instance
        user_profile = UserProfile(weight=70, goal_protein=150, goal_carbs=200, goal_calories=2500)
        
        # Create the ProgressModel instance with the user profile
        progress_model = ProgressModel(user_profile)
        
        # Create the ProgressViewModel with both user_profile and progress_model
        progress_view_model = ProgressViewModel(user_profile, progress_model)

        # Initialize screens with ProgressViewModel passed as argument
        self.screens = {
            "Home": ProgressScreen(self, progress_view_model),
            "Ingredients": IngredientScreen(self),
        }

        # Add screens to Column 1 and hide them initially
        for screen in self.screens.values():
            screen.grid(row=0, column=1, sticky="nsew")
            screen.grid_remove()  # Hide all screens initially

        # Display the Home screen by default
        self.current_screen = "Home"
        self.screens[self.current_screen].grid()

        # Bind the tabview to switch screens on tab change using a function
        self.tabview.configure(command=self.switch_screen)

    def switch_screen(self, selected_tab):
        """Switch between screens based on selected tab."""
        # Hide the current screen
        self.screens[self.current_screen].grid_remove()

        # Show the selected screen
        self.current_screen = selected_tab
        self.screens[self.current_screen].grid()

if __name__ == "__main__":
    window = App()
    window.mainloop()