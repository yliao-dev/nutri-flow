class NutritionManager:
    """
    A manager class for handling nutrition data.
    It stores and updates protein, carbs, and calories data.
    """
    def __init__(self):
        self.nutrition_data = {
            'protein': 0.0,  # In grams
            'carbs': 0.0,    # In grams
            'calories': 0.0  # In calories
        }

    def update_nutrition(self, nutrition_values):
        """
        Update the nutrition data with new values.
        :param nutrition_values: A dictionary containing 'protein', 'carbs', and 'calories' to be updated.
        """
        for key, value in nutrition_values.items():
            if key in self.nutrition_data:
                self.nutrition_data[key] += value
            else:
                raise ValueError(f"Invalid nutrition key: {key}")
    
    def get_nutrition_data(self):
        """
        Returns the current nutrition data.
        :return: A dictionary containing 'protein', 'carbs', and 'calories'.
        """
        return self.nutrition_data
    
    def calculate_percentage(self, goal, current_value):
        """
        Calculate the percentage progress towards a goal.
        :param goal: The target goal for the nutrient (e.g., user goal for protein).
        :param current_value: The current consumed value of the nutrient.
        :return: The percentage progress towards the goal.
        """
        if goal == 0:
            return 0.0
        return (current_value / goal) * 100

    def get_progress(self, user_goals):
        """
        Get the progress (in percentage) for protein, carbs, and calories.
        :param user_goals: A dictionary containing the user goals for protein, carbs, and calories.
        :return: A dictionary containing the progress percentages for 'protein', 'carbs', and 'calories'.
        """
        progress = {}
        for nutrient, goal in user_goals.items():
            progress[nutrient] = self.calculate_percentage(goal, self.nutrition_data[nutrient])
        return progress