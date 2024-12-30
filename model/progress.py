
class NutritionData:
    """
    Represents a structured nutrition data set.
    """
    def __init__(self, calories=0, protein=0, carbohydrates=0):
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates

class ProgressModel:
    """
    Represents the nutrition data for the application.
    """
    def __init__(self):
        self.nutrition_data = NutritionData()
        
    def add_progress(self, data: NutritionData):
        self.nutrition_data.calories += data.calories
        self.nutrition_data.protein += data.protein
        self.nutrition_data.carbohydrates += data.carbohydrates
        