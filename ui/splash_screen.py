import customtkinter as ctk

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        
        # Center the splash screen using place()
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Add a label with a loading message
        self.loading_label = ctk.CTkLabel(self, text="Loading...", font=("Arial", 20))
        self.loading_label.place(relx=0.5, rely=0.4, anchor="center")

        # Add a progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.place(relx=0.5, rely=0.6, anchor="center")
        self.progress_bar.start()

    def hide(self):
        """Hide the splash screen."""
        self.grid_forget()