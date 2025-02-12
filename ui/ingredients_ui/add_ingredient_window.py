import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

from config import *

class AddIngredientWindow(ctk.CTkToplevel):
    def __init__(self, master, on_confirm_callback):
        super().__init__(master)
        self.title("Add Ingredient")
        self.center_window(ADD_INGREDIENT_WIDTH, ADD_INGREDIENT_HEIGHT)
        self.resizable(False, False)

        self.on_confirm_callback = on_confirm_callback
        self.selected_image_path = None

        # UI Elements
        self.create_widgets()

    def center_window(self, width, height):
            """Center the application window on the screen."""
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            self.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """Create UI elements for the pop-up window."""
        self.grid_rowconfigure(1, weight=1)  # Allow main content to expand
        self.grid_columnconfigure(0, weight=1)  # Make it stretch horizontally

        # Image Selection (Fixed Size)
        self.image_label = ctk.CTkLabel(
            self, text="No Image Selected",
            fg_color="gray",
            width=128, height=128
        )
        self.image_label.pack(pady=10)  # No expand, keeps fixed size

        self.select_image_button = ctk.CTkButton(self, text="Select Image", command=self.select_image)
        self.select_image_button.pack(pady=5, padx=20, fill="x")  # Full width

        # Nutrition Inputs
        self.nutrition_inputs = {}
        fields = ["Carbohydrates (g)", "Protein (g)", "Fat (g)", "Calories (kcal)"]
        nutrition_frame = ctk.CTkFrame(self)
        nutrition_frame.pack(pady=10, padx=20, expand=True, fill="both")  # Takes full space

        for field in fields:
            frame = ctk.CTkFrame(nutrition_frame)
            frame.pack(pady=5, padx=20, fill="x")

            label = ctk.CTkLabel(frame, text=field, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(frame)
            entry.pack(side="right", expand=True, padx=5, fill="x")  # Entry fields stretch
            self.nutrition_inputs[field] = entry

        # Buttons (Confirm & Cancel) at the bottom, equal space
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(side="bottom", pady=10, padx=20, fill="x")

        button_frame.grid_columnconfigure(0, weight=1) 
        button_frame.grid_columnconfigure(1, weight=1)

        self.confirm_button = ctk.CTkButton(button_frame, text="Confirm", command=self.confirm)
        self.confirm_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5) 

        self.cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", command=self.destroy, fg_color="red", hover_color="dark red"
        )
        self.cancel_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
    def select_image(self):
        """Open file dialog to select an image."""
        file_path = filedialog.askopenfilename(
            initialdir=IMG_FOLDER_PATH,
            filetypes=[("Image Files", ("*.png", "*.jpg", "*.jpeg"))]  # Use a tuple inside
        )
        if not file_path:
            print("No new image selected.")
            return None  # Return None if no file is created

        self.selected_image_path = file_path
        img = Image.open(file_path)
        self.after(100, lambda: self.set_image(img))

    def set_image(self, img):
        """Update the image label to fit without resizing."""
        width, height = self.image_label.winfo_width(), self.image_label.winfo_height()
        
        if width > 0 and height > 0:  # Ensure valid dimensions
            img_ctk = ctk.CTkImage(img, size=(width, height))
            self.image_label.configure(image=img_ctk, text="")
            self.image_label.image = img_ctk  # Prevent garbage collection
            
    def confirm(self):
        """Collect input data and pass it back to the main screen."""
        # ingredient_data = {
        #     "image": self.selected_image_path,
        #     "nutrition": {field: self.nutrition_inputs[field].get() for field in self.nutrition_inputs}
        # }
        # self.on_confirm_callback(ingredient_data)
        print("todo")
        self.destroy()