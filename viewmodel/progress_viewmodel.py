from model.progress import ProgressModel, NutritionData

class ProgressViewModel:
    """
    Manages the logic and data flow between the NutritionModel and the view.
    """
    def __init__(self):
        self.model = ProgressModel()
    
    def get_progress_data(self) -> NutritionData:
        return self.model.nutrition_data
    
    def add_progress(self, data: NutritionData):
        self.model.add_progress(data)
