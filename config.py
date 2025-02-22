import os
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
WIDTH = 1200
HEIGHT = 800
ADD_INGREDIENT_WIDTH=256
ADD_INGREDIENT_HEIGHT=512

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_PATH, "nutrition_logs")
IMG_FOLDER_PATH = os.path.join(ROOT_PATH, "data", "image")
USER_CONFIG_PATH = os.path.join(ROOT_PATH, "data", "user_config.json")
INGREDIENTS_JSON_PATH = os.path.join(ROOT_PATH, "data", "ingredients.json")
DARK_MODE_IMG = "data/image/dark-mode.png"
ADD_INGREDIENT_IMG = "data/image/add-ingredient.png"

SPLASH_IMG = "data/image/loading-bar.png"

# Global constants for nutrition data keys
CONSUMED_PROTEIN = "consumed_protein"
CONSUMED_CARBOHYDRATE = "consumed_carbohydrate"
CONSUMED_FAT = "consumed_fat"
CONSUMED_CALORIES = "consumed_calories"
LOADING_TIME = 300