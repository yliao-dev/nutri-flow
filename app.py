import customtkinter as ctk
from ui.progress_screen import ProgressScreen
from ui.ingredient_screen import IngredientScreen
from viewmodal.progress_viewmodal import ProgressViewModal
from modal.user_profile import UserProfile

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

        # Bind the tabview to switch screens on tab change using a lambda function
        self.tabview.configure(command=lambda: self.switch_screen(self.tabview.get()))

        # Initialize screens
        self.screens = {
            "Home": ProgressScreen(self, ProgressViewModal(UserProfile(70, 150, 200, 2500))),
            "Ingredients": IngredientScreen(self),
        }

        # Add screens to Column 1 and hide them initially
        for screen in self.screens.values():
            screen.grid(row=0, column=1, sticky="nsew")
            screen.grid_remove()  # Hide all screens initially

        # Display the Home screen by default
        self.current_screen = "Home"
        self.screens[self.current_screen].grid()

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