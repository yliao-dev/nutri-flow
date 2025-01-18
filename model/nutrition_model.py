class NutritionModel:
    """
    A class for managing nutrition data, tracking progress, and calculating percentages.
    """
    def __init__(self, user_profile):
        self.user_profile = user_profile  # Store the UserProfile object
        self.nutrition_data = {
            'protein': 0.0,  # In grams
            'carbohydrate': 0.0,    # In grams
            'calories': 0.0,  # In calories
            'fat': 0.0,
        }
        self.consumed_ingredients = {}

    def update_nutrition(self, selected_ingredients):
        """
        Update the nutrition data based on selected ingredients.
        :param selected_ingredients: A list of dictionaries, each containing 'protein', 'carbohydrate', and 'calories' for an ingredient.
        """
        for ingredient in selected_ingredients:
            self.nutrition_data['protein'] += ingredient['nutrition'].get('protein', 0)
            self.nutrition_data['carbohydrate'] += ingredient['nutrition'].get('carbohydrates', 0)
            self.nutrition_data['calories'] += ingredient['nutrition'].get('calories', 0)
            self.nutrition_data['fat'] += ingredient['nutrition'].get('fat', 0)
                
            name = ingredient.get('name')
            amount = ingredient.get('amount', 0)  # The amount consumed in grams

            # Update the total amount consumed in the consumed_ingredients dictionary
            if name in self.consumed_ingredients:
                self.consumed_ingredients[name].append(amount)
            else:
                self.consumed_ingredients[name] = [amount]


    def get_nutrition_data(self):
        """
        Returns the current nutrition data.
        :return: A dictionary containing 'protein', 'carbohydrate', and 'calories'.
        """
        return self.nutrition_data
    
    def get_consumed_ingredients(self):
        """
        Returns the consumed ingredients with the amount consumed in grams.
        :return: A dictionary containing the name of each consumed ingredient and the amount consumed in grams.
        """
        return self.consumed_ingredients

    def get_nutrition_percentages(self):
        """
        Calculates the percentage of each nutritional element (protein, carbs, calories) based on the user's goals.
        :return: A dictionary with 'protein', 'carbohydrates', and 'calories' percentages.
        """
        percentages = {
            'protein': self._calculate_percentage(self.nutrition_data['protein'], self.user_profile.goal_protein),
            'carbohydrate': self._calculate_percentage(self.nutrition_data['carbohydrate'], self.user_profile.goal_carbohydrates),
            'calories': self._calculate_percentage(self.nutrition_data['calories'], self.user_profile.goal_calories)
        }
        return percentages

    def _calculate_percentage(self, current_value, goal_value):
        """
        Helper function to calculate the percentage progress towards a goal.
        :param current_value: The current consumed value of the nutrient.
        :param goal_value: The target goal for the nutrient.
        :return: The percentage progress towards the goal.
        """
        if goal_value == 0:
            return 0.0
        return (current_value / goal_value) * 100