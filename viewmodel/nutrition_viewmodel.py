class NutritionViewModel:
    """
    A ViewModel for managing nutrition progress and providing data for display.
    This class connects user actions with the NutritionModel.
    """
    def __init__(self, user_nutrition_model):
        self.user_nutrition_model = user_nutrition_model

    def update_nutrition(self, selected_ingredients):  
        self.user_nutrition_model.update_nutrition(selected_ingredients)

    def get_date(self):
        return self.user_nutrition_model.get_date()
    
    def get_weight(self):
        return self.user_nutrition_model.get_weight()
    
    def get_log_path(self):
        return self.user_nutrition_model.get_log_path()
    
    def get_nutrition_data(self):
        """
        Returns the current nutrition data (protein, carbs, calories).
        :return: A dictionary with the current nutrition data.
        """
        return self.user_nutrition_model.get_nutrition_data()
    
    def get_nutrition_percentages(self):
        """
        Returns the current nutrition progress as a percentage.
        :return: A dictionary with the progress percentages for protein, carbs, and calories.
        """
        return self.user_nutrition_model.get_nutrition_percentages()

    def get_consumed_ingredients(self):
        return self.user_nutrition_model.get_consumed_ingredients()
    