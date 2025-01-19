from config import *
class UserNutritionModel:
    """
    Represents the user profile, manages nutrition data, and tracks progress.
    """
    def __init__(self, date, weight, goal_protein, goal_carbohydrate, goal_fat, goal_calories, log_path,
                 nutrition_data=None, consumed_ingredients=None):
        # User profile attributes
        self.date = date
        self.weight = weight
        self.goal_protein = goal_protein
        self.goal_carbohydrate = goal_carbohydrate
        self.goal_fat = goal_fat
        self.goal_calories = goal_calories
        self.log_path = log_path or ""

        # Nutrition tracking attributes
        self.nutrition_data = nutrition_data or {
            CONSUMED_PROTEIN: 0.0,
            CONSUMED_CARBOHYDRATE: 0.0,
            CONSUMED_CALORIES: 0.0,
            CONSUMED_FAT: 0.0
        }
        self.consumed_ingredients = consumed_ingredients or {}

    def update_nutrition(self, selected_ingredients):
        """
        Update the nutrition data based on selected ingredients.
        :param selected_ingredients: A list of dictionaries, each containing 'protein', 'carbohydrate', 'fat', and 'calories' for an ingredient.
        """

        for ingredient in selected_ingredients:
            nutrition = ingredient.get("nutrition", {})
            self.nutrition_data[CONSUMED_PROTEIN] += nutrition.get("protein", 0.0)
            self.nutrition_data[CONSUMED_CARBOHYDRATE] += nutrition.get("carbohydrate", 0.0)
            self.nutrition_data[CONSUMED_CALORIES] += nutrition.get("calories", 0.0)
            self.nutrition_data[CONSUMED_FAT] += nutrition.get("fat", 0.0)
            name = ingredient.get("name")
            amount = ingredient.get("custom_serving_size", 0.0)  # Amount consumed in grams

            # Update the total amount consumed in the consumed_ingredients dictionary
            if name in self.consumed_ingredients:
                self.consumed_ingredients[name].append(amount)
            else:
                self.consumed_ingredients[name] = [amount]
        

    def get_nutrition_data(self):
        """
        Returns the current nutrition data.
        :return: A dictionary containing 'consumed_protein', 'consumed_carbohydrate', 'consumed_fat', and 'consumed_calories'.
        """
        return {
            CONSUMED_PROTEIN: round(self.nutrition_data[CONSUMED_PROTEIN], 2),
            CONSUMED_CARBOHYDRATE: round(self.nutrition_data[CONSUMED_CARBOHYDRATE], 2),
            CONSUMED_FAT: round(self.nutrition_data[CONSUMED_FAT], 2),
            CONSUMED_CALORIES: round(self.nutrition_data[CONSUMED_CALORIES], 2)
        }

    def get_consumed_ingredients(self):
        """
        Returns the consumed ingredients with the total amounts consumed in grams.
        :return: A dictionary with ingredient names as keys and a list of consumed amounts as values.
        """
        return self.consumed_ingredients

    def get_nutrition_percentages(self):
        """
        Calculates the percentage of each nutritional element (protein, carbs, fat, calories) based on the user's goals.
        :return: A dictionary with 'protein', 'carbohydrate', 'fat', and 'calories' percentages.
        """
        return {
            "protein": self._calculate_percentage(self.nutrition_data[CONSUMED_PROTEIN], self.goal_protein),
            "carbohydrate": self._calculate_percentage(self.nutrition_data[CONSUMED_CARBOHYDRATE], self.goal_carbohydrate),
            "fat": self._calculate_percentage(self.nutrition_data[CONSUMED_FAT], self.goal_fat),
            "calories": self._calculate_percentage(self.nutrition_data[CONSUMED_CALORIES], self.goal_calories)
        }

    def _calculate_percentage(self, current_value, goal_value):
        """
        Helper function to calculate the percentage progress towards a goal.
        :param current_value: The current consumed value of the nutrient.
        :param goal_value: The target goal for the nutrient.
        :return: The percentage progress towards the goal.
        """
        if goal_value <= 0:
            return 0.0
        return round((current_value / goal_value) * 100, 2)

    def __repr__(self):
        return (f"UserNutritionModel(date={self.date}, weight={self.weight}, goal_protein={self.goal_protein}, "
                f"goal_carbohydrate={self.goal_carbohydrate}, goal_fat={self.goal_fat}, "
                f"goal_calories={self.goal_calories}, log_path={self.log_path}, "
                f"nutrition_data={self.get_nutrition_data()}, "
                f"consumed_ingredients={self.consumed_ingredients})")