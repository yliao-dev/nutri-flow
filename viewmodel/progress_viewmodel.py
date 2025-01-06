from model.user_profile import NutritionData

class ProgressViewModel:
    """
    A ViewModel for managing nutrition progress.
    """
    def __init__(self, user_profile, progress_model):
        self.user_profile = user_profile
        self.progress_model = progress_model
        
    def increment_values(self, protein, carbs, calories):
        """
        Update consumed nutrition data.
        """
        consumed_data = NutritionData(protein=protein, carbohydrates=carbs, calories=calories)
        self.progress_model.add_progress(consumed_data)