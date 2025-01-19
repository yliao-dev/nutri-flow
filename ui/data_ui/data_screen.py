import os
from tkinter import filedialog
import pandas as pd
import customtkinter as ctk
from datetime import datetime
from config import LOG_PATH
from model.data_manager import load_nutrition_data_from_csv

class DataScreen(ctk.CTkFrame):
    def __init__(self, parent, nutrition_view_model):
        super().__init__(parent)
        self.initialize_ui()
        self.nutrition_view_model = nutrition_view_model
        os.makedirs(LOG_PATH, exist_ok=True)
        
    def initialize_ui(self):
        self.grid_rowconfigure(0, weight=1)  # Dates row
        self.grid_rowconfigure(1, weight=3)  # Data detail row
        self.grid_rowconfigure(2, weight=1)  # Import/Export frame row
        self.grid_columnconfigure(0, weight=1)
        
        self.create_data_load_frame()
        
    def create_data_load_frame(self):
        self.data_load_frame = ctk.CTkFrame(self)
        self.data_load_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.data_load_frame.grid_rowconfigure(0, weight=1)
        self.data_load_frame.grid_columnconfigure(0, weight=1)  
        self.data_load_frame.grid_columnconfigure(1, weight=1)
        self.data_load_frame.grid_columnconfigure(2, weight=1)
        # Create Import Data button
        self.import_button = ctk.CTkButton(self.data_load_frame, text="Import Data", command=self.import_data)
        self.import_button.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Create Export Data button
        self.export_button = ctk.CTkButton(self.data_load_frame, text="Export Data", command=self.export_data)
        self.export_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create New Data button
        self.past_data_button = ctk.CTkButton(self.data_load_frame, text="New Daily Log", command=self.create_new_data)
        self.past_data_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        
    def import_data(self):
        """Allow the user to select and read a CSV file using pandas."""
        file_path = filedialog.askopenfilename(
            title="Select a CSV File",
            initialdir=LOG_PATH,
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not file_path:
            print("No file selected.")
            return        
        load_nutrition_data_from_csv(file_path, self.nutrition_view_model)
    


    def export_data(self):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        csv_data = [
            ["Date", "Weight (kg)"],
            [timestamp, self.nutrition_view_model.user_profile.weight],
            [],
            ["Protein Goal (g)", "Carbohydrates Goal (g)", "Fat Goal (g)", "Calories Goal (kcal)"],
            [
                self.nutrition_view_model.user_profile.goal_protein,
                self.nutrition_view_model.user_profile.goal_carbohydrates,
                self.nutrition_view_model.user_profile.goal_fat,
                self.nutrition_view_model.user_profile.goal_calories,
            ],
            [],
            ["Protein Consumed (g)", "Carbohydrates Consumed (g)", "Fat Consumed (g)", "Calories Consumed (kcal)"],
            [
                self.nutrition_view_model.get_nutrition_data()['protein'],
                self.nutrition_view_model.get_nutrition_data()['carbohydrate'],
                self.nutrition_view_model.get_nutrition_data()['fat'],
                self.nutrition_view_model.get_nutrition_data()['calories'],
            ],
            [],
            ["Protein Percentage (%)", "Carbohydrates Percentage (%)", "Fat Percentage (%)", "Calories Percentage (%)"],
            [
                self.nutrition_view_model.get_nutrition_percentages()['protein'],
                self.nutrition_view_model.get_nutrition_percentages()['carbohydrate'],
                self.nutrition_view_model.get_nutrition_percentages()['fat'],
                self.nutrition_view_model.get_nutrition_percentages()['calories'],
            ],
            [],
            ["Consumed Ingredients", "Consumed Amount (g)"],
        ]

        # Add consumed ingredients data
        consumed_ingredients = self.nutrition_view_model.get_consumed_ingredients()
        print(consumed_ingredients)
        for ingredient, amounts in consumed_ingredients.items():
            formatted_ingredient = ingredient.replace("_", " ").title()
            amounts_str = ",".join(map(str, amounts))            
            csv_data.append([formatted_ingredient, amounts_str])

        # Pass the final data to the `create_new_data` method
        self.create_new_data(csv_data)
    
    def create_new_data(self, data):
        df = pd.DataFrame(data)
        """Create a new daily log CSV file with pandas."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_name = f"nutrition_log_{timestamp}.csv"
        file_path = os.path.join(LOG_PATH, file_name)
        
        counter = 1
        while os.path.exists(file_path):
            file_name = f"nutrition_log_{timestamp}({counter}).csv"
            file_path = os.path.join(LOG_PATH, file_name)
            counter += 1
        
        try:
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False, header=False)
            print(f"New daily log created: {file_path}")
        except Exception as e:
            print(f"Failed to create new log: {e}")