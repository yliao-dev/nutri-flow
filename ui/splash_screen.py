import customtkinter as ctk
import time

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.master = master
        
        # Configure the window to allow centering
        self.grid(row=0, column=0, sticky="nsew")
        
        # Optionally, center the splash screen using the place() method
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Add a label with a loading message
        self.loading_label = ctk.CTkLabel(self, text="Loading...", font=("Arial", 20))
        self.loading_label.grid(row=0, column=0, padx=10, pady=10)

        # Optionally, you can add a progress bar or spinner
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=10)
        self.progress_bar.start()

        # Ensure the row and column weights are configured to expand and center the content
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def hide(self):
        """Hide the splash screen."""
        self.grid_forget()