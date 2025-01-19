class UserProfile:
    """
    Represents user nutrition goals and profile.
    """
    def __init__(self, weight, goal_protein, goal_carbohydrates, goal_fat, goal_calories, log_path,
                 nutrition_data=None, consumed_ingredients=None):
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbohydrates = goal_carbohydrates
        self.goal_fat = goal_fat
        self.goal_calories = goal_calories
        self.log_path = log_path or ""
        self.nutrition_data = nutrition_data or {
            "consumed_protein": 0,
            "consumed_carbohydrate": 0,
            "consumed_calories": 0,
            "consumed_fat": 0
        }
        self.consumed_ingredients = consumed_ingredients or {}

    def __repr__(self):
        return (f"UserProfile(weight={self.weight}, goal_protein={self.goal_protein}, "
                f"goal_carbohydrates={self.goal_carbohydrates}, goal_fat={self.goal_fat}, "
                f"goal_calories={self.goal_calories}, nutrition_data={self.nutrition_data}, "
                f"consumed_ingredients={self.consumed_ingredients})")