class ProgressViewModel:
    """
    A ViewModel for managing nutrition progress.
    """
    def __init__(self, user_profile, progress_model):
        self.user_profile = user_profile
        self.progress_model = progress_model

        # Access the NutritionManager from ProgressModel
        self.nutrition_manager = self.progress_model.nutrition_manager  

    def increment_values(self, protein, carbs, calories):
        """
        Update consumed nutrition data using NutritionManager.
        """
        self.nutrition_manager.update_nutrition({
            'protein': protein,
            'carbs': carbs,
            'calories': calories
        })

    def get_progress(self):
        """
        Get the progress for protein, carbs, and calories.
        :return: A dictionary with progress percentages for 'protein', 'carbs', and 'calories'.
        """
        user_goals = {
            'protein': self.user_profile.goal_protein,
            'carbs': self.user_profile.goal_carbs,
            'calories': self.user_profile.goal_calories
        }

        return self.nutrition_manager.get_progress(user_goals)