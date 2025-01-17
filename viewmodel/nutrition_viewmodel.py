class NutritionViewModel:
    """
    A ViewModel for managing nutrition progress and providing data for display.
    This class connects user actions with the NutritionModel.
    """
    def __init__(self, user_profile, nutrition_model):
        self.user_profile = user_profile
        self.nutrition_model = nutrition_model  # NutritionModel instance for handling data

    def increment_values(self, protein, carbs, calories):
        """
        Update the consumed nutrition data in NutritionModel.
        :param protein: The amount of protein consumed.
        :param carbs: The amount of carbohydrates consumed.
        :param calories: The amount of calories consumed.
        """
        selected_ingredients = [{
            'protein': protein,
            'carbohydrates': carbs,
            'calories': calories
        }]
        self.nutrition_model.update_nutrition(selected_ingredients)

    def get_progress(self):
        """
        Returns the current nutrition progress as a percentage.
        :return: A dictionary with the progress percentages for protein, carbs, and calories.
        """
        return self.nutrition_model.get_nutrition_percentages()

    def get_current_nutrition_data(self):
        """
        Returns the current nutrition data (protein, carbs, calories).
        :return: A dictionary with the current nutrition data.
        """
        return self.nutrition_model.get_nutrition_data()