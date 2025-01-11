import customtkinter as ctk

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

        # Appearance Mode Selector
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=len(self.tabs) + 1, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self, 
            values=["Light", "Dark", "System"], 
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.grid(row=len(self.tabs) + 2, column=0, padx=20, pady=(10, 20), sticky="ew")
        self.appearance_mode_optionmenu.set("Dark")

    def switch_screen(self, selected_tab):
        """Switch between screens based on selected tab."""
        if selected_tab != self.parent.current_screen:
            self.parent.screens[self.parent.current_screen].grid_remove()
            self.parent.current_screen = selected_tab
            self.parent.screens[self.parent.current_screen].grid()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode)