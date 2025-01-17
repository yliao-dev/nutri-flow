import customtkinter as ctk

class DataScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize_ui()
        
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
        
        # Create Past Data button
        self.past_data_button = ctk.CTkButton(self.data_load_frame, text="Past Data", command=self.show_past_data)
        self.past_data_button.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        
    def import_data(self):
        print("Import Data button clicked")

    def export_data(self):
        print("Export Data button clicked")

    def show_past_data(self):
        print("Past Data button clicked")