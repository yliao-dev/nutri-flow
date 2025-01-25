import customtkinter as ctk
from PIL import Image  # For handling the image
from config import *

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0, sticky="nsew")
        
        # Center the splash screen
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Load the image using CTkImage
        self.image = ctk.CTkImage(
            Image.open(SPLASH_IMG),
            size=(200, 200)  # Adjust the size if needed
        )
        
        # Display the image
        self.image_label = ctk.CTkLabel(self, image=self.image, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

    def hide(self):
        """Hide the splash screen."""
        self.grid_forget()