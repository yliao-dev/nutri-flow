import tkinter as tk
import time

class CircularProgressBar(tk.Frame):
    def __init__(self, master, size, thickness, color, bg_color, text_color):
        super().__init__(master, bg=bg_color)
        self.size = size
        self.thickness = thickness
        self.color = color
        self.bg_color = bg_color
        self.text_color = text_color

        self.canvas = tk.Canvas(self, width=self.size, height=self.size, bg=self.bg_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Draw background circle once
        self.create_circle()

        # Create the text label for percentage outside the canvas
        self.progress_label = tk.Label(self, text="0%", font=("Arial", 14, "bold"), fg=self.text_color, bg=bg_color)
        self.progress_label.place(relx=0.5, rely=0.5, anchor="center")

        # Animate the progress
        self.animate_progress(100)

    def create_circle(self):
        """Draw the background circle."""
        self.canvas.create_oval(
            self.thickness, self.thickness,
            self.size - self.thickness, self.size - self.thickness,
            outline="#443",  # Background circle color
            width=self.thickness
        )

    def animate_progress(self, target_progress):
        """Animate the progress to the target value."""
        current_progress = 0
        step = 1  # Progress increment per animation step

        def update_progress():
            nonlocal current_progress

            if current_progress <= target_progress:
                # Update the canvas with progress
                self.canvas.delete("progress_arc")  # Remove previous arc
                angle = 360 * (current_progress / 100)
                self.canvas.create_arc(
                    self.thickness, self.thickness,
                    self.size - self.thickness, self.size - self.thickness,
                    start=90,  # Start at 12 o'clock (90-degree north)
                    extent=angle,
                    outline=self.color,
                    width=self.thickness,
                    style="arc",
                    tags="progress_arc"
                )

                # Update the text label
                self.progress_label.config(text=f"{current_progress}%")

                # Increment progress and call the update again after a short delay
                current_progress += step
                self.after(50, update_progress)  # Repeat after 50 ms

        # Start the animation
        update_progress()


# Testing the Circular Progress Bar
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")  # Set window size

    progress_bar = CircularProgressBar(root, size=200, thickness=10, color="blue", bg_color="white", text_color="black")
    progress_bar.pack(padx=20, pady=20)

    root.mainloop()