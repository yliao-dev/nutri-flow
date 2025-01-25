from datetime import datetime
import pandas as pd
import json
from config import *
import sys
from tkinter import filedialog



def restart_app():
        print("Restarting the application...")
        os.execv(sys.executable, [sys.executable, "app.py"])

def get_unique_filename(file_name):
    file_path = os.path.join(LOG_PATH, file_name)
    base_name, ext = os.path.splitext(file_name)
    version = 1

    while os.path.exists(file_path):
        file_name = f"{base_name}({version}){ext}"
        file_path = os.path.join(LOG_PATH, file_name)
        version += 1

    return file_name

def create_new_log_file(data, file_name):
    file_path = filedialog.asksaveasfilename(
        title="Save Nutrition Log As",
        initialfile=file_name,
        defaultextension=".csv",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )

    if not file_path:
        print("No new file created.")
        return False

    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False, header=False)
        print(f"New nutrition log created: {file_path}")
        return True
    except Exception as e:
        print(f"Failed to create new nutrition log: {e}")
        return False



def load_from_ingredients_json():
    with open(INGREDIENTS_JSON_PATH, "r") as file:
        data = json.load(file)
    ingredients = []
    for ingredient_name, details in data.items():
        ingredient_details = details.copy()
        ingredient_details["name"] = ingredient_name
        ingredient_details["frequency_of_use"] = details.get("frequency_of_use", 0)
        ingredient_details["last_used_date"] = details.get("last_used_date", None)
        ingredients.append(ingredient_details)
    return ingredients

def sort_ingredients(ingredients, criteria="frequency_of_use", descending=True):
    if criteria in ["protein", "carbohydrate"]:
        return sorted(
            ingredients, 
            key=lambda x: x["nutrition"].get(criteria, 0), 
            reverse=descending
        )
    return sorted(
        ingredients, 
        key=lambda x: x.get(criteria, 0), 
        reverse=descending
    )
def write_to_ingredients_json(selected_ingredients):
    try:
        with open(INGREDIENTS_JSON_PATH, 'r+') as file:
            data = json.load(file)            
            df = pd.DataFrame.from_dict(data, orient='index')
            for ingredient in selected_ingredients:
                ingredient_name = ingredient.get("name")
                
                if ingredient_name in df.index:
                    if "frequency_of_use" in df.columns:
                        df.at[ingredient_name, "frequency_of_use"] = df.at[ingredient_name, "frequency_of_use"] + 1
                    
                    if "last_used_date" in df.columns:
                        df.at[ingredient_name, "last_used_date"] = datetime.now().isoformat()
                    
                    if "custom_serving_size" in ingredient:
                        df.at[ingredient_name, "custom_serving_size"] = ingredient["custom_serving_size"]
                else:
                    print(f"Ingredient {ingredient_name} not found in data.")
            
            df.to_json(INGREDIENTS_JSON_PATH, orient='index', indent=4)
            # print("ingredient.json updated successfully.")

    except Exception as e:
        print(f"Error updating ingredient.json: {e}")

def write_to_user_config(nutrition_view_model):
    """
    Update the user_config.json with consumed ingredients and nutrition data.
    """
    try:
        # Load the user configuration data
        with open(USER_CONFIG_PATH, 'r') as file:
            data = json.load(file)
        data["date"] = nutrition_view_model.get_date()
        data["weight"] = nutrition_view_model.get_weight()
        data["log_path"] = nutrition_view_model.get_log_path()
        
        nutrition_data = nutrition_view_model.get_nutrition_data()
        data["nutrition_data"].update({
            CONSUMED_PROTEIN: float(nutrition_data.get(CONSUMED_PROTEIN, 0.0)),
            CONSUMED_CARBOHYDRATE: float(nutrition_data.get(CONSUMED_CARBOHYDRATE, 0.0)),
            CONSUMED_CALORIES: float(nutrition_data.get(CONSUMED_CALORIES, 0.0)),
            CONSUMED_FAT: float(nutrition_data.get(CONSUMED_FAT, 0.0)),
        })
        data["consumed_ingredients"] = nutrition_view_model.get_consumed_ingredients()

        # Write updated data back to the user config file
        with open(USER_CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        # print("user_config.json updated successfully.")
    except Exception as e:
        print(f"Error updating user_config.json: {e}")

def import_nutrition_data_from_file(nutrition_view_model):
    file_path = filedialog.askopenfilename(
            title="Please Select a Valid CSV File",
            initialdir=LOG_PATH,
            filetypes=(("CSV Files", "*.csv"),)
    )
    if not file_path:
        print("No file selected.")
        return False
    try:
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)

        # Access the user_nutrition_model from the nutrition_view_model
        user_nutrition_model = nutrition_view_model.user_nutrition_model

        # Manually extract the relevant data from specific rows and columns
        # Extracting date and weight
        user_nutrition_model.date = df.iloc[1, 0]
        user_nutrition_model.weight = df.iloc[1, 1]
        user_nutrition_model.log_path = os.path.basename(file_path)

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
        consumed_amount = [json.loads(ingredient) for ingredient in ingredients_df.iloc[:, 1]]
        user_nutrition_model.consumed_ingredients = dict(zip(ingredients_df[0], consumed_amount))

        # print(f"User Profile updated: {user_nutrition_model.__dict__}\n")
        return True
    except Exception as e:
        print(f"Error updating user profile from CSV: {e}")
        return False
        
        
def export_nutrition_data_to_file(nutrition_view_model):
    csv_data = [
            ["Date", "Weight (kg)", "File name"],
            [datetime.now().strftime("%Y-%m-%d"), nutrition_view_model.user_nutrition_model.weight, nutrition_view_model.user_nutrition_model.log_path],
            [],
            ["Protein Goal (g)", "Carbohydrate Goal (g)", "Fat Goal (g)", "Calories Goal (kcal)"],
            [
                nutrition_view_model.user_nutrition_model.goal_protein,
                nutrition_view_model.user_nutrition_model.goal_carbohydrate,
                nutrition_view_model.user_nutrition_model.goal_fat,
                nutrition_view_model.user_nutrition_model.goal_calories,
            ],
            [],
            ["Protein Consumed (g)", "Carbohydrate Consumed (g)", "Fat Consumed (g)", "Calories Consumed (kcal)"],
            [
                nutrition_view_model.get_nutrition_data()[CONSUMED_PROTEIN],
                nutrition_view_model.get_nutrition_data()[CONSUMED_CARBOHYDRATE],
                nutrition_view_model.get_nutrition_data()[CONSUMED_FAT],
                nutrition_view_model.get_nutrition_data()[CONSUMED_CALORIES],
            ],
            [],
            ["Protein Percentage (%)", "Carbohydrate Percentage (%)", "Fat Percentage (%)", "Calories Percentage (%)"],
            [
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_PROTEIN],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_CARBOHYDRATE],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_FAT],
                nutrition_view_model.get_nutrition_percentages()[CONSUMED_CALORIES],
            ],
            [],
            ["Consumed Ingredients", "Consumed Amount (g)"],
        ]

        # Add consumed ingredients data
    consumed_ingredients = nutrition_view_model.get_consumed_ingredients()
    for ingredient, consumed_amounts in consumed_ingredients.items():
        csv_data.append([ingredient, consumed_amounts])
    return create_new_log_file(csv_data, nutrition_view_model.get_log_path())
    
def fresh_user_config(nutrition_view_model, new_file_name):
    try:
        with open(USER_CONFIG_PATH, 'r') as file:
            data = json.load(file)
        timestamp = datetime.now().strftime("%Y-%m-%d")
        data["date"] = timestamp
        data["weight"] = nutrition_view_model.get_weight()
        data["log_path"] = new_file_name        
        data["nutrition_data"].update({
            CONSUMED_PROTEIN: 0.0,
            CONSUMED_CARBOHYDRATE: 0.0,
            CONSUMED_CALORIES: 0.0,
            CONSUMED_FAT: 0.0,
        })
        data["consumed_ingredients"] = {}

        # Write updated data back to the user config file
        with open(USER_CONFIG_PATH, 'w') as file:
            json.dump(data, file, indent=4)

        print("user_config.json refreshed successfully.")
    except Exception as e:
        print(f"Error refreshing user_config.json: {e}")
    