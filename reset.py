import json
from datetime import datetime
from config import INGREDIENTS_JSON_PATH

# Function to reset the 'frequency_of_use' or 'last_used_date' for all ingredients
def reset_all_data(reset_type, data):
    for item in data.values():  # Iterate through the values (ingredient data)
        if reset_type == "frequency_of_use":
            item["frequency_of_use"] = 0
            print(f"Frequency of use for {item['name']} has been reset.")
        elif reset_type == "last_used_date":
            item["last_used_date"] = datetime.now().isoformat()  # Reset date to current time in ISO format
            print(f"Last used date for {item['name']} has been reset.")
        else:
            print("Invalid reset type. Please choose 'frequency_of_use' or 'last_used_date'.")
    return data

# Load the data from your JSON file
with open(INGREDIENTS_JSON_PATH, 'r') as f:
    data = json.load(f)

# Example usage: Reset 'frequency_of_use' or 'last_used_date' for all ingredients
data = reset_all_data("frequency_of_use", data)  # To reset frequency_of_use for all ingredients
data = reset_all_data("last_used_date", data)    # To reset last_used_date for all ingredients

# Optionally, save the updated data back to the file
with open(INGREDIENTS_JSON_PATH, 'w') as f:
    json.dump(data, f, indent=4)