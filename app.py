import customtkinter as ctk
from ui.progress_screen import ProgressScreen
from viewmodal.progress_viewmodal import ProgressViewModal
from modal.user_profile import UserProfile


class App(ctk.CTk):
    """
    The main application window for NutriFlow.
    """
    def __init__(self):
        super().__init__()

        self.title("NutriFlow")
        self.geometry(f"{1100}x{580}")

        user_profile = UserProfile(weight=70, goal_protein=150, goal_carbs=200, goal_calories=2500)
        progress_view_modal = ProgressViewModal(user_profile)

        self.progress_screen = ProgressScreen(self, progress_view_modal)
        self.progress_screen.pack(expand=True, fill="both")


if __name__ == "__main__":
    window = App()
    window.mainloop()