import tkinter as tk
from tkinter import ttk
import json

class Interface(tk.Tk):
    def __init__(self, floor_files, update_interval=5000):
        super().__init__()
        self.title("Sensor Interface")
        self.configure(bg="lightgray")  # Set background color

        self.floor_files = floor_files  # Store the file paths for each floor's data
        self.update_interval = update_interval  # Time interval in milliseconds for updating data

        self.floor_labels = ["Floor 1", "Floor 2", "Floor 3"]  # Labels for the floors

        # Initialize StringVar variables for sensor data
        self.current_values = [tk.StringVar() for _ in range(3)]
        self.voltage_values = [tk.StringVar() for _ in range(3)]
        self.power_values = [tk.StringVar() for _ in range(3)]
        self.smoke_values = [tk.StringVar() for _ in range(3)]
        self.temperature_values = [tk.StringVar() for _ in range(3)]
        self.humidity_values = [tk.StringVar() for _ in range(3)] 

        # Define fonts for labels and values
        label_font = ('Helvetica', 12)  # Font for labels
        value_font = ('Helvetica', 12, 'bold')  # Font for values
        floor_label_font = ('Helvetica', 14, 'bold')  # Font for floor labels

        # Create and place labels and value fields for each floor
        for i, floor_label in enumerate(self.floor_labels):
            row_offset = i * 8  # Increase row offset to accommodate new humidity label

            # Floor label
            tk.Label(self, text=f"{floor_label}", font=floor_label_font, bg="lightgray").grid(row=row_offset, column=0, padx=10, pady=5, sticky='w')

            # Sensor data labels and values
            tk.Label(self, text="Current (A): ", font=label_font, bg="lightgray").grid(row=row_offset+1, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.current_values[i], font=value_font, bg="lightgray").grid(row=row_offset+1, column=1, padx=10, pady=5, sticky='w')

            tk.Label(self, text="Voltage (V): ", font=label_font, bg="lightgray").grid(row=row_offset+2, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.voltage_values[i], font=value_font, bg="lightgray").grid(row=row_offset+2, column=1, padx=10, pady=5, sticky='w')

            tk.Label(self, text="Power (W): ", font=label_font, bg="lightgray").grid(row=row_offset+3, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.power_values[i], font=value_font, bg="lightgray").grid(row=row_offset+3, column=1, padx=10, pady=5, sticky='w')

            tk.Label(self, text="Smoke Level: ", font=label_font, bg="lightgray").grid(row=row_offset+4, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.smoke_values[i], font=value_font, bg="lightgray").grid(row=row_offset+4, column=1, padx=10, pady=5, sticky='w')

            tk.Label(self, text="Temperature (Celsius): ", font=label_font, bg="lightgray").grid(row=row_offset+5, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.temperature_values[i], font=value_font, bg="lightgray").grid(row=row_offset+5, column=1, padx=10, pady=5, sticky='w')

            tk.Label(self, text="Humidity (%): ", font=label_font, bg="lightgray").grid(row=row_offset+6, column=0, padx=10, pady=5, sticky='w')
            tk.Label(self, textvariable=self.humidity_values[i], font=value_font, bg="lightgray").grid(row=row_offset+6, column=1, padx=10, pady=5, sticky='w')

            # Add a separator between floors, but not after the last one
            if i < 2:
                separator = ttk.Separator(self, orient='horizontal')
                separator.grid(row=row_offset+7, column=0, columnspan=2, pady=10, sticky='ew')

        # Initial load and schedule periodic updates
        self.load_and_update_data()
        self.schedule_updates()

    def load_and_update_data(self):
        """Load data from JSON files and update the displayed values."""
        for i in range(3):
            self.update_value(self.current_values[i], self.floor_files[i][0], 'current_rms')
            self.update_value(self.voltage_values[i], self.floor_files[i][4], 'voltage_rms')
            self.update_value(self.power_values[i], self.floor_files[i][1], 'average_power')
            self.update_value(self.smoke_values[i], self.floor_files[i][2], 'smoke_level')
            self.update_value(self.temperature_values[i], self.floor_files[i][3], 'temperature')
            self.update_value(self.humidity_values[i], self.floor_files[i][3], 'humidity')  # Update humidity

    def update_value(self, variable, json_file, key):
        """Update a StringVar with data from a JSON file."""
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            value = data.get(key, 'N/A')
            variable.set(f"{value:.2f}")  # Round to 2 decimal places
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            variable.set('N/A')

    def schedule_updates(self):
        """Schedule periodic updates of the sensor data."""
        self.load_and_update_data()
        self.after(self.update_interval, self.schedule_updates)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 16:
        print("Usage: python interface2.py <floor_1_current_file> <floor_1_power_file> <floor_1_smoke_file> <floor_1_temperature_file> <floor_1_voltage_file> <floor_2_current_file> <floor_2_power_file> <floor_2_smoke_file> <floor_2_temperature_file> <floor_2_voltage_file> <floor_3_current_file> <floor_3_power_file> <floor_3_smoke_file> <floor_3_temperature_file> <floor_3_voltage_file>")
        sys.exit(1)
    
    # Organize file paths for each floor
    floor_files = [
        sys.argv[1:6],   # Files for Floor 1
        sys.argv[6:11],  # Files for Floor 2
        sys.argv[11:16]  # Files for Floor 3
    ]

    # Create and run the application
    app = Interface(floor_files)
    app.mainloop()
