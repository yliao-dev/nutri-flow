import customtkinter as ctk

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

    def animate_progress(self, target_progress):
        """Animate the progress of the circular bar."""
        # If the target progress is 100% or more, set it to 100% and stop the animation
        if target_progress >= 100:
            target_progress = 100
            self.update_progress(target_progress)
            return  # Stop animation once it reaches or exceeds 100%

        current_progress = self.progress
        step = 1  # Progress increment per animation step

        # Animate towards the target progress
        def animate():
            nonlocal current_progress
            if current_progress < target_progress:
                # Move forward with increments, but stop when reaching the target
                if current_progress + step > target_progress:
                    current_progress = target_progress
                else:
                    current_progress += step
                self.update_progress(current_progress)
                if current_progress < target_progress:
                    self.after(50, animate)
            elif current_progress > target_progress:
                # Move backward with increments, but stop when reaching the target
                if current_progress - step < target_progress:
                    current_progress = target_progress
                else:
                    current_progress -= step
                self.update_progress(current_progress)
                if current_progress > target_progress:
                    self.after(50, animate)

        animate()