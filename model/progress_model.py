from model.user_profile import NutritionData

class ProgressModel:
    """
    Tracks nutrition data progress and calculates completion percentages.
    """
    def __init__(self, user_profile):
        self.nutrition_data = NutritionData()
        self.user_profile = user_profile  # Store the user profile to calculate percentages

    def add_progress(self, data: NutritionData):
        """
        Adds nutrition data to the current progress (consumed data).
        """
        self.nutrition_data.calories += data.calories
        self.nutrition_data.protein += data.protein
        self.nutrition_data.carbohydrates += data.carbohydrates

    def get_progress(self):
        """
        Returns the current nutrition data.
        """
        return self.nutrition_data

    def calculate_percentage(self):
        """
        Calculates the percentage of the nutrition data completed based on the user's goals.
        Returns a dictionary with the percentage of calories, protein, and carbohydrates.
        """
        percentage = {
            "calories": self._calculate_single_percentage(self.nutrition_data.calories, self.user_profile.goal_calories),
            "protein": self._calculate_single_percentage(self.nutrition_data.protein, self.user_profile.goal_protein),
            "carbohydrates": self._calculate_single_percentage(self.nutrition_data.carbohydrates, self.user_profile.goal_carbs)
        }
        return percentage

    def _calculate_single_percentage(self, current_value, goal_value):
        """
        Helper function to calculate percentage for a single nutritional element.
        Returns the percentage value or 0 if the goal is 0.
        """
        return (current_value / goal_value) * 100 if goal_value > 0 else 0