from modal.progress_modal import ProgressModal, NutritionData

class ProgressViewModal:
    """
    Manages the logic and data flow between the ProgressModel and the view.
    """
    def __init__(self, user_profile):
        self.modal = ProgressModal(user_profile)
    
    def get_progress_data(self) -> NutritionData:
        return self.modal.get_progress()
    
    def add_progress(self, data: NutritionData):
        self.modal.add_progress(data)

    def calculate_percentage(self):
        return self.modal.calculate_percentage()