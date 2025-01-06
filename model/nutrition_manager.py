class NutritionManager:
    """
    A manager class for handling nutrition data.
    It stores and updates protein, carbohydrate, and calories data.
    """
    def __init__(self):
        self.nutrition_data = {
            'protein': 0.0,  # In grams
            'carbohydrate': 0.0,    # In grams
            'calories': 0.0  # In calories
        }

    def update_nutrition(self, selected_ingredients):
        """
        Update the nutrition data based on selected ingredients.
        :param selected_ingredients: A list of dictionaries, each containing 'protein', 'carbohydrate', and 'calories' for an ingredient.
        """
        # Accumulate nutrition values from each ingredient
        for ingredient in selected_ingredients:
            self.nutrition_data['protein'] += ingredient.get('protein', 0)
            self.nutrition_data['carbohydrate'] += ingredient.get('carbohydrates', 0)
            self.nutrition_data['calories'] += ingredient.get('calories', 0)

    def get_nutrition_data(self):
        """
        Returns the current nutrition data.
        :return: A dictionary containing 'protein', 'carbohydrate', and 'calories'.
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