class UserProfile:
    """
    Represents user nutrition goals and profile.
    """
    def __init__(self, weight, goal_protein, goal_carbs, goal_calories):
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbs = goal_carbs
        self.goal_calories = goal_calories
