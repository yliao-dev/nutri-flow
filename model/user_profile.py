class UserProfile:
    """
    Represents user nutrition goals and profile.
    """
    def __init__(self, weight, goal_protein, goal_carbohydrates, goal_fat, goal_calories):
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbohydrates = goal_carbohydrates
        self.goal_fat = goal_fat
        self.goal_calories = goal_calories
