class UserProfile:
    """
    Represents user nutrition goals and profile.
    """
    def __init__(self, weight, goal_protein, goal_carbs, goal_calories):
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbs = goal_carbs
        self.goal_calories = goal_calories


class NutritionData:
    """
    Represents a structured nutrition data set.
    """
    def __init__(self, calories=0, protein=0, carbohydrates=0):
        self.calories = calories
        self.protein = protein
        self.carbohydrates = carbohydrates