import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, tabs):
        super().__init__(parent)
        self.parent = parent
        self.tabs = tabs

        # Sidebar Frame layout configuration
        self.grid_columnconfigure(0, weight=1)
        
        # Add TabView to Sidebar
        self.tabview = ctk.CTkTabview(self, width=140)
        self.tabview.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        
        for tab in self.tabs:
            self.tabview.add(tab)

        # Bind the tabview to switch screens on tab change using the local method
        self.tabview.configure(command=self.switch_screen)

        # Appearance Mode Selector
        self.appearance_mode_label = ctk.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(
            self, 
            values=["Light", "Dark", "System"], 
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.grid(row=2, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionmenu.set("Dark")

    def switch_screen(self):
        """Switch between screens based on selected tab."""
        selected_tab = self.tabview.get()
        self.parent.screens[self.parent.current_screen].grid_remove()
        self.parent.current_screen = selected_tab
        self.parent.screens[self.parent.current_screen].grid()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change the appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode)