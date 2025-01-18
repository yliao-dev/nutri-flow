import os
import customtkinter as ctk

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_PATH, "nutrition_logs")
USER_CONFIG_PATH = os.path.join(ROOT_PATH, "data", "user_config.json")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")
WIDTH = 1200
HEIGHT = 800