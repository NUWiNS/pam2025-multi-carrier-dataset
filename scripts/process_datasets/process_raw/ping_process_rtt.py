import pandas as pd
import os
from datetime import datetime,timedelta
#read the file
def process_out_file(file_path, output_csv_path):
    timestamps = [] 
    times_ms = []
    
    with open(file_path, 'r') as file:
        line = file.readline() 

        while not line.startswith("Start time:"):
            line = file.readline()
        start_time_ms = int(line.strip().split(": ")[1])
        for line in file:
            if "time=" in line:
                try:
                    time_ms_str = line.split("time=")[1].split(" ")[0]
                    timestamp = start_time_ms
                    time_ms = float(time_ms_str)
                    timestamps.append(timestamp)
                    times_ms.append(time_ms)
                except Exception as e:
                    print(f"error in:{e}，content：{line}")

    
    if timestamps:
        interval = 200
        selected_timestamps = [timestamps[0]]
        selected_times = [times_ms[0]]

        current_expected_timestamp = timestamps[0] + interval
    
        for i in range(1, len(timestamps)):
            # If the current timestamp is greater than or equal to the expected timestamp, select this time point
                selected_timestamps.append(current_expected_timestamp)
                selected_times.append(times_ms[i])
                current_expected_timestamp = current_expected_timestamp + 200
        
        # Save in DataFrame
        df_selected_final = pd.DataFrame({"Timestamp": selected_timestamps, "Time (ms)": selected_times})
        
        # Save the csv
        df_selected_final.to_csv(output_csv_path, index=False)
        
        print(f"Data is saved to {output_csv_path}")
    else:
        print("No valid time data found.")

root_dir = r"C:\Users\ayano\Desktop\ping_app_layer_data\ping_data_drive_trip_2\05_16_2023_2\app\verizon"
output_dir = r"C:\Users\ayano\Desktop\rtt_verizon2"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".out"):
            file_path = os.path.join(subdir, file)
            output_csv_name = os.path.splitext(file)[0] + "_processed.csv"
            output_csv_path = os.path.join(output_dir, output_csv_name)
            process_out_file(file_path, output_csv_path)
            print(f"the results are saved in：{output_csv_path}")
