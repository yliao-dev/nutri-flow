import customtkinter as ctk

class CircularProgressBar(ctk.CTkFrame):
    def __init__(self, master, size, progress, thickness, color, bg_color, text_color):
        super().__init__(master, fg_color=bg_color)

        self.size = size
        self.progress = progress
        self.thickness = thickness
        self.color = color
        self.text_color = text_color

        # Create a canvas with transparent background and set size explicitly
        self.canvas = ctk.CTkCanvas(self, bg=self._get_color(bg_color), highlightthickness=0, width=self.size, height=self.size)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Center the canvas within the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Draw the background circle once
        self.create_circle()

        # Create placeholders for progress arc and text
        self.arc = None
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
        # Store the actual progress
        self.progress = round(progress, 2)

        # Calculate the angle for the progress arc
        visible_progress = min(progress, 100)  # Cap visible progress at 100%
        angle = 360 * (visible_progress / 100)

        # Update or create the progress arc
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

        # Update the progress text to show actual progress (even if >100%)
        self.canvas.delete(self.text)  # Clear previous text
        self.text = self.canvas.create_text(
            self.size // 2,
            self.size // 2,
            text=f"{int(progress)}%",  # Show actual progress
            fill=self.text_color,
            font=("Arial", 14, "bold")
        )

    def animate_progress(self, target_progress):
        """Animate the progress of the circular bar."""
        current_progress = self.progress
        step = 1  # Progress increment per animation step

        # Precalculate the visible target percentage (cap at 100 for the visual bar)
        visible_target_progress = min(target_progress, 100)

        def animate():
            nonlocal current_progress

            # Increment the progress
            current_progress += step

            # If current progress reaches or exceeds the visible target
            if current_progress >= visible_target_progress:
                self.update_progress(visible_target_progress)  # Ensure bar is visually full
                self.progress = target_progress  # Store the actual value (even >100%)
                return  # Stop animation here

            # Update the progress and schedule the next step
            self.update_progress(current_progress)
            self.after(50, animate)

        # Start the animation if the current progress is below the visible target
        if current_progress < visible_target_progress:
            animate()
        else:
            # If already full, update the text to reflect the actual target progress
            self.update_progress(target_progress)