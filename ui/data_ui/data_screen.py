import os
from tkinter import filedialog
import pandas as pd
import customtkinter as ctk
from datetime import datetime
from config import ROOT_PATH, LOG_PATH
from viewmodel.nutrition_viewmodel import NutritionViewModel

class DataScreen(ctk.CTkFrame):
    def __init__(self, parent, nutrition_view_model):
        super().__init__(parent)
        self.initialize_ui()
        self.nutrition_view_model = nutrition_view_model
        self.daily_logs_path = os.path.join(ROOT_PATH, LOG_PATH)  # Path to root/daily_logs
        os.makedirs(self.daily_logs_path, exist_ok=True)
        
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
            initialdir=self.daily_logs_path,
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )
        
        if not file_path:
            print("No file selected.")
            return
        
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            print(f"File Path: {file_path}")
            print("Content:")
            print(df.head())  # Display the first few rows of the DataFrame
        except Exception as e:
            print(f"Failed to read file: {e}")


    def export_data(self):
        """Export data."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        csv_data = [
            ["Date"],  # Header for the date section
            [timestamp],  # Actual date
            [],  # Empty row
            ["Protein Goal (g)", "Carbohydrates Goal (g)", "Calories Goal (kcal)"],  # Goal headers
            [
                self.nutrition_view_model.user_profile.goal_protein,
                self.nutrition_view_model.user_profile.goal_carbs,
                self.nutrition_view_model.user_profile.goal_calories,
            ],
            [],  # Empty row
            ["Protein Consumed (g)", "Carbohydrates Consumed (g)", "Calories Consumed (kcal)"],  # Consumed headers
            [
                self.nutrition_view_model.get_nutrition_data()['protein'],
                self.nutrition_view_model.get_nutrition_data()['carbohydrate'],
                self.nutrition_view_model.get_nutrition_data()['calories'],
            ],
            [],  # Empty row
            ["Protein Percentage (%)", "Carbohydrates Percentage (%)", "Calories Percentage (%)"],  # Percentage headers
            [
                self.nutrition_view_model.get_nutrition_percentages()['protein'],
                self.nutrition_view_model.get_nutrition_percentages()['carbohydrate'],
                self.nutrition_view_model.get_nutrition_percentages()['calories'],
            ]
        ]
        self.create_new_data(csv_data)
        
        
    def create_new_data(self, data):
        df = pd.DataFrame(data)
        """Create a new daily log CSV file with pandas."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        file_name = f"nutrition_log_{timestamp}.csv"
        file_path = os.path.join(self.daily_logs_path, file_name)
        
        counter = 1
        while os.path.exists(file_path):
            file_name = f"nutrition_log_{timestamp}({counter}).csv"
            file_path = os.path.join(self.daily_logs_path, file_name)
            counter += 1
        
        try:
            # Save the DataFrame to a CSV file
            df.to_csv(file_path, index=False, header=False)
            print(f"New daily log created: {file_path}")
        except Exception as e:
            print(f"Failed to create new log: {e}")