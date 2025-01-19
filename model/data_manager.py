import pandas as pd
import json
from config import INGREDIENTS_JSON_PATH, USER_CONFIG_PATH


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

        # Get consumed ingredients and update
        consumed_ingredients = nutrition_view_model.get_consumed_ingredients()
        data["consumed_ingredients"] = consumed_ingredients

        # Get nutrition data and update
        nutrition_data = nutrition_view_model.get_nutrition_data()
        data["nutrition_data"].update({
            "consumed_protein": nutrition_data["protein"],
            "consumed_carbohydrate": nutrition_data["carbohydrate"],
            "consumed_calories": nutrition_data["calories"],
            "consumed_fat": nutrition_data["fat"],
        })

        # Write updated data back to the user config file
        with open(USER_CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        print("user_config.json updated successfully.")
    except Exception as e:
        print(f"Error updating user_config.json: {e}")