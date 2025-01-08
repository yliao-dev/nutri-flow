import customtkinter as ctk


# Protein: #025d93
# Carbohydrate: #f9d77c
# Calories: #bc4c4c
class CircularProgressBar(ctk.CTkFrame):
    def __init__(self, master, size, progress, thickness, color, bg_color, text_color):
        super().__init__(master, fg_color=bg_color)

        self.size = size
        self.progress = progress
        self.thickness = thickness
        self.color = color
        self.text_color = text_color

        # Create a canvas with transparent background
        self.canvas = ctk.CTkCanvas(self, bg=self._get_color(bg_color), highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")  # Allow resizing with grid

        self.grid_rowconfigure(0, weight=1)  # Allow row to expand with window
        self.grid_columnconfigure(0, weight=1)  # Allow column to expand with window

        # Draw the background circle once
        self.create_circle()

        # Create a placeholder for the progress arc (will be updated later)
        self.arc = None
        # Create a placeholder for the text (will be updated later)
        self.text = None

        # Update the progress immediately to show the initial value
        self.update_progress(self.progress)

    def _get_color(self, color):
        """Convert CustomTkinter colors to standard Tkinter colors."""
        return "systemTransparent" if color == "transparent" else color

    def create_circle(self):
        """Draw the background circle (only once)."""
        self.canvas.create_oval(
            self.thickness,
            self.thickness,
            self.size - self.thickness,
            self.size - self.thickness,
            outline="#443",  # Background circle color
            width=self.thickness
        )

    def update_progress(self, progress):
        """Update the progress arc and the text."""
        self.progress = progress

        # Calculate the angle for the progress arc
        angle = 360 * (progress / 100)

        # Update the progress arc if it already exists, otherwise create it
        if self.arc:
            self.canvas.itemconfig(self.arc, extent=angle)
        else:
            self.arc = self.canvas.create_arc(
                self.thickness,
                self.thickness,
                self.size - self.thickness,
                self.size - self.thickness,
                start=90,  # Start at 12 o'clock (90-degree north)
                extent=angle,
                outline=self.color,
                width=self.thickness,
                style="arc"
            )

        # Update the progress text directly
        self.text = self.canvas.create_text(
                self.size // 2,
                self.size // 2,
                text=f"{int(progress)}%",
                fill=self.text_color,
                font=("Arial", 14, "bold")
            )

    def start_loading(self):
        """Start the loading animation."""
        self.animate_progress(0)

    def animate_progress(self, progress):
        """Animate the progress of the circular bar."""
        if progress <= 100:
            self.update_progress(progress)
            self.after(50, self.animate_progress, progress + 1)  # Update progress every 50ms

# App setup using CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("800x400")  # Adjusted size for horizontal layout
app.title("Circular Progress Bars")

# Frame for the circular progress bars
frame = ctk.CTkFrame(app)  # Set frame background to transparent
frame.pack(pady=20, fill="both", expand=True)

# Circular progress bar instances with custom parameters
progress_bar1 = CircularProgressBar(
    frame, 
    size=150, 
    progress=0, 
    thickness=3, 
    color="#025d93",  # Protein color
    bg_color="transparent",  
    text_color="white"
)
progress_bar1.pack(side="left", padx=10, expand=True)

progress_bar2 = CircularProgressBar(
    frame, 
    size=150, 
    progress=0, 
    thickness=3, 
    color="#f9d77c",  # Carbohydrate color
    bg_color="transparent",  
    text_color="white"
)
progress_bar2.pack(side="left", padx=10, expand=True)

progress_bar3 = CircularProgressBar(
    frame, 
    size=150, 
    progress=0, 
    thickness=3, 
    color="#bc4c4c",  # Calories color
    bg_color="transparent",  
    text_color="white"
)
progress_bar3.pack(side="left", padx=10, expand=True)

# Button to start the loading animation
def start_loading():
    progress_bar1.start_loading()
    progress_bar2.start_loading()
    progress_bar3.start_loading()

button = ctk.CTkButton(app, text="Start Loading", command=start_loading)
button.pack(pady=20)

app.mainloop()