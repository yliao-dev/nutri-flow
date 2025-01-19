import pandas as pd
import json
from config import *

def update_custom_serving_sizes_in_json(selected_ingredients):
    """
    Update the 'custom_serving_size' field in ingredient.json based on selected ingredients.
    """
    try:
        # Load the ingredients data
        with open(INGREDIENTS_JSON_PATH, 'r') as file:
            data = json.load(file)
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame.from_dict(data, orient='index')

        # Update custom serving sizes
        for ingredient in selected_ingredients:
            ingredient_name = ingredient["name"]
            if ingredient_name in df.index:
                df.at[ingredient_name, "custom_serving_size"] = ingredient["custom_serving_size"]
        
        # Save back to JSON
        df.to_json(INGREDIENTS_JSON_PATH, orient='index', indent=4)
        print("ingredient.json updated successfully.")
    except Exception as e:
        print(f"Error updating ingredient.json: {e}")


def update_user_config(nutrition_view_model):
    """
    Update the user_config.json with consumed ingredients and nutrition data.
    """
    try:
        # Load the user configuration data
        with open(USER_CONFIG_PATH, 'r') as file:
            data = json.load(file)

        consumed_ingredients = nutrition_view_model.get_consumed_ingredients()

        data["consumed_ingredients"] = consumed_ingredients
        nutrition_data = nutrition_view_model.get_nutrition_data()
        
        # Use the global constants for updating nutrition data
        data["nutrition_data"].update({
            CONSUMED_PROTEIN: float(nutrition_data.get(CONSUMED_PROTEIN, 0.0)),
            CONSUMED_CARBOHYDRATE: float(nutrition_data.get(CONSUMED_CARBOHYDRATE, 0.0)),
            CONSUMED_CALORIES: float(nutrition_data.get(CONSUMED_CALORIES, 0.0)),
            CONSUMED_FAT: float(nutrition_data.get(CONSUMED_FAT, 0.0)),
        })

        # Write updated data back to the user config file
        with open(USER_CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        print("user_config.json updated successfully.")
    except Exception as e:
        print(f"Error updating user_config.json: {e}")

def load_nutrition_data_from_csv(csv_path, nutrition_view_model):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_path, header=None)

        # Access the user_nutrition_model from the nutrition_view_model
        user_nutrition_model = nutrition_view_model.user_nutrition_model

        # Manually extract the relevant data from specific rows and columns
        # Extracting date and weight
        user_nutrition_model.date = df.iloc[1, 0]
        user_nutrition_model.weight = df.iloc[1, 1]

        # Extracting goals data
        user_nutrition_model.goal_protein = df.iloc[4, 0]
        user_nutrition_model.goal_carbohydrate = df.iloc[4, 1]
        user_nutrition_model.goal_fat = df.iloc[4, 2]
        user_nutrition_model.goal_calories = df.iloc[4, 3]

        # Extracting consumed data
        user_nutrition_model.nutrition_data[CONSUMED_PROTEIN] = df.iloc[7, 0]
        user_nutrition_model.nutrition_data[CONSUMED_CARBOHYDRATE] = df.iloc[7, 1]
        user_nutrition_model.nutrition_data[CONSUMED_FAT] = df.iloc[7, 2]
        user_nutrition_model.nutrition_data[CONSUMED_CALORIES] = df.iloc[7, 3]

        # Extracting consumed ingredients
        ingredients_df = df.iloc[13:, :2]
        user_nutrition_model.consumed_ingredients = dict(zip(ingredients_df[0], ingredients_df[1]))

        print(f"User Profile updated: {user_nutrition_model.__dict__}")

    except Exception as e:
        print(f"Error updating user profile from CSV: {e}")