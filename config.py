import os
import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
WIDTH = 1200
HEIGHT = 800

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_PATH, "nutrition_logs")
USER_CONFIG_PATH = os.path.join(ROOT_PATH, "data", "user_config.json")
INGREDIENTS_JSON_PATH = os.path.join(ROOT_PATH, "data", "ingredients.json")
DARK_MODE_IMG = "data/dark-mode.png"

# Global constants for nutrition data keys
CONSUMED_PROTEIN = "consumed_protein"
CONSUMED_CARBOHYDRATE = "consumed_carbohydrate"
CONSUMED_FAT = "consumed_fat"
CONSUMED_CALORIES = "consumed_calories"
LOADING_TIME = 300