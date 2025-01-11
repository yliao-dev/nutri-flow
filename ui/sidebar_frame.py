import customtkinter as ctk
from PIL import Image

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, tabs):
        super().__init__(parent)
        self.parent = parent
        self.tabs = tabs

        # Sidebar Frame layout configuration
        self.grid_columnconfigure(0, weight=1)  # Sidebar column takes full width

        # Configure rows to share space equally
        for i in range(len(self.tabs)):
            self.grid_rowconfigure(i, weight=1)  # Each row for the buttons gets equal weight

        # Create vertical buttons for each tab
        self.tab_buttons = []
        for i, tab in enumerate(self.tabs):
            tab_button = ctk.CTkButton(self, text=tab, command=lambda tab=tab: self.switch_screen(tab))
            tab_button.grid(row=i, column=0, padx=20, pady=5, sticky="ewns")  # Stretched vertically and horizontally
            self.tab_buttons.append(tab_button)

        # Add separator (black line) between sidebar and main frame
        self.separator = ctk.CTkCanvas(self, width=2)
        self.separator.grid(row=0, column=1, rowspan=len(self.tabs) + 1, padx=10, pady=0, sticky="ns")  # Vertical separator

        # Appearance Mode Selector (using a single image)
        self.mode_img = ctk.CTkImage(light_image=Image.open("data/dark-mode.png"), size=(40, 40))  # Using only the dark mode image

        # Use CTkButton for the mode toggle, not CTkLabel
        self.mode_button = ctk.CTkButton(
                self, 
                text="", 
                image=self.mode_img, 
                cursor="hand2", 
                command=self.toggle_appearance_mode, 
                fg_color="transparent",  # Transparent background
                border_width=0,           # No border
                hover_color=None,         # No hover effect
                state="normal"
        )
        self.mode_button.grid(row=len(self.tabs) + 2, column=0, padx=20, pady=(10, 20), sticky="ew")

    def switch_screen(self, selected_tab):
        """Switch between screens based on selected tab."""
        if selected_tab != self.parent.current_screen:
            self.parent.screens[self.parent.current_screen].grid_remove()
            self.parent.current_screen = selected_tab
            self.parent.screens[self.parent.current_screen].grid()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode)

    def toggle_appearance_mode(self):
        """Toggle between light and dark mode when clicked."""
        current_mode = ctk.get_appearance_mode()

        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")  # Switch to light mode
        else:
            ctk.set_appearance_mode("Dark")  # Switch to dark mode