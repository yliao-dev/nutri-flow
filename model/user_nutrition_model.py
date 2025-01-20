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
        self.log_path = log_path
        
        # Nutrition tracking attributes
        self.nutrition_data = nutrition_data or {
            CONSUMED_PROTEIN: 0.0,
            CONSUMED_CARBOHYDRATE: 0.0,
            CONSUMED_CALORIES: 0.0,
            CONSUMED_FAT: 0.0
        }
        self.consumed_ingredients = consumed_ingredients or {}

    def get_date(self):
        return self.date
    
    def get_weight(self):
        return self.weight
    
    def get_log_path(self):
        return self.log_path
    
    def update_nutrition(self, selected_ingredients):
        """
        Update the nutrition data based on selected ingredients.
        :param selected_ingredients: A list of dictionaries, each containing 'protein', 'carbohydrate', 'fat', and 'calories' for an ingredient.
        """

        for ingredient in selected_ingredients:
            nutrition = ingredient.get("nutrition", {})
            custom_serving_size = ingredient.get("custom_serving_size", 0.0)
            reference_serving_size = ingredient.get("reference_serving_size", 99.0)
            # Calculate the serving ratio
            print(custom_serving_size, reference_serving_size)
            serving_ratio = custom_serving_size / reference_serving_size
            print(serving_ratio)
            # Update nutrition data considering the serving ratio
            self.nutrition_data[CONSUMED_PROTEIN] += nutrition.get("protein", 0.0) * serving_ratio
            self.nutrition_data[CONSUMED_CARBOHYDRATE] += nutrition.get("carbohydrate", 0.0) * serving_ratio
            self.nutrition_data[CONSUMED_CALORIES] += nutrition.get("calories", 0.0) * serving_ratio
            self.nutrition_data[CONSUMED_FAT] += nutrition.get("fat", 0.0) * serving_ratio
            
            name = ingredient.get("name")
            if name in self.consumed_ingredients:
                self.consumed_ingredients[name].append(custom_serving_size)
            else:
                self.consumed_ingredients[name] = [custom_serving_size]
        

    def get_nutrition_data(self):
        """
        Returns the current nutrition data.
        :return: A dictionary containing 'consumed_protein', 'consumed_carbohydrate', 'consumed_fat', and 'consumed_calories'.
        """
        return {
            CONSUMED_PROTEIN: round(float(self.nutrition_data.get(CONSUMED_PROTEIN, 0)), 2),
            CONSUMED_CARBOHYDRATE: round(float(self.nutrition_data.get(CONSUMED_CARBOHYDRATE, 0)), 2),
            CONSUMED_FAT: round(float(self.nutrition_data.get(CONSUMED_FAT, 0)), 2),
            CONSUMED_CALORIES: round(float(self.nutrition_data.get(CONSUMED_CALORIES, 0)), 2)
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
            CONSUMED_PROTEIN: self._calculate_percentage(self.nutrition_data[CONSUMED_PROTEIN], self.goal_protein),
            CONSUMED_CARBOHYDRATE: self._calculate_percentage(self.nutrition_data[CONSUMED_CARBOHYDRATE], self.goal_carbohydrate),
            CONSUMED_FAT: self._calculate_percentage(self.nutrition_data[CONSUMED_FAT], self.goal_fat),
            CONSUMED_CALORIES: self._calculate_percentage(self.nutrition_data[CONSUMED_CALORIES], self.goal_calories)
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