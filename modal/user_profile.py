class UserProfile:
    """
    Represents the user's personal data and goals.
    """
    def __init__(self, weight, goal_protein, goal_carbs, goal_calories):
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbs = goal_carbs
        self.goal_calories = goal_calories

    def __str__(self):
        return (f"User Profile:\n"
                f"Weight: {self.weight} kg\n"
                f"Goal Protein: {self.goal_protein} g\n"
                f"Goal Carbs: {self.goal_carbs} g\n"
                f"Goal Calories: {self.goal_calories} kcal")