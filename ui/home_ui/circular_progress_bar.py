import customtkinter as ctk
import tkinter as tk

class CircularProgressBar(ctk.CTkFrame):
    def __init__(self, master, size, progress, thickness, color, text_color="black"):
        super().__init__(master)

        self.size = size
        self.progress = progress
        self.thickness = thickness
        self.color = color
        self.text_color = text_color

        # Create a canvas with transparent background and set size explicitly
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, width=self.size, height=self.size)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create the label for the percentage text outside the canvas
        self.progress_label = tk.Label(self, text=f"{int(self.progress)}%", font=("Arial", 14, "bold"), fg=self.text_color)
        self.progress_label.place(relx=0.5, rely=0.5, anchor="center")

        # Center the canvas within the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Draw the background circle once
        self.create_circle()

        # Create placeholders for progress arc and text
        self.arc = None

        # Update the progress immediately to show the initial value
        self.update_progress(self.progress)

    def create_circle(self):
        """Draw the background circle (only once)."""
        self.canvas.create_oval(
            self.thickness, self.thickness,
            self.size - self.thickness, self.size - self.thickness,
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

        # Only create the arc once, if not already created
        if self.arc is None:
            self.arc = self.canvas.create_arc(
                self.thickness, self.thickness,
                self.size - self.thickness, self.size - self.thickness,
                start=90,  # Start at 12 o'clock (90-degree north)
                extent=angle,
                outline=self.color,
                width=self.thickness,
                style="arc"
            )
        else:
            # Update the arc extent if it's already created
            if self.progress >= 100:
                self.canvas.itemconfig(self.arc, extent=359.99)  # Fill the circle
            else:
                self.canvas.itemconfig(self.arc, extent=angle)  # Update progress

        # Update the percentage text in the label
        self.progress_label.config(text=f"{int(self.progress)}%")

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