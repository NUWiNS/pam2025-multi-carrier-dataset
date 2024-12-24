import pandas as pd
import pickle

import os
import glob

# Define the source and destination directories
source_dir = r"C:\Users\ayano\Desktop\ul_d2\atnt\d2"
destination_dir = r"C:\Users\ayano\Desktop\ul_d3\atnt\d2"

# Make sure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)
# Load the CSV file
csv_files = glob.glob(os.path.join(source_dir, "*.csv"))

# Process each CSV file
for csv_file in csv_files:
    # Read the CSV file
    df = pd.read_csv(csv_file, low_memory=False)
#df = pd.read_csv(r"C:\Users\ayano\Desktop\drive_2\tmobile_day_1.csv",low_memory=False)

# Ensure that 'GPS Time' has at least one non-null value to begin with
    if df['GPS Time'].first_valid_index() is not None:
    # Forward fill the 'GPS Time' column to fill the blanks with the previous non-null value
        df['GPS Time'] = df['GPS Time'].ffill()
        df.dropna(subset=['GPS Time'], inplace=True)
    # Subtract one hour from 'Combined Timestamp'
    #def subtract_one_hour(time_str):
    #    from datetime import datetime
    #    if pd.isnull(time_str):
     #       return None
    # Now using strptime to parse just the time without date
     #   try:
      #      time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
    # Subtracting one hour
       #     time_with_subtracted_hour = (datetime.combine(datetime.today(), time_obj) - pd.Timedelta(hours=1)).time()
        #    return time_with_subtracted_hour
        #except ValueError:
        #    return None
#'GPS Time' column - 1 hour
#df['GPS Time'] = df['GPS Time'].apply(subtract_one_hour)
    df.dropna(subset=['GPS Time'], inplace=True)
#print(df['GPS Time'])
    df['TIME_STAMP'] = pd.to_datetime(df['TIME_STAMP'], errors='coerce')
    df = df.dropna(subset=['TIME_STAMP'])
#print(df['TIME_STAMP'])
#combine GPS Time with TIME_STAMP date
    df['GPS Time'] = df['GPS Time'].astype(str)
    df['Date'] = df['TIME_STAMP'].dt.strftime('%Y/%m/%d')
    df['GPS Time'] = df['Date'] + ' ' + df['GPS Time']
#print(df['GPS Time'])
#delete date
    df.drop('Date', axis=1, inplace=True)

    columns_to_save = [
        'TIME_STAMP', 'GPS Time', 'Lat', 'Lon', 
        "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]", 
        "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]", 
        'Event 5G-NR/LTE Events', 
        "5G KPI PCell RF Frequency [MHz]", 
        "5G KPI PCell RF Serving PCI", 
        "LTE KPI PCell Serving EARFCN(DL)"
        "Time (ms)"
        "Timestamp"
    ]

    filtered_df = df.loc[:, columns_to_save]
    
# Generate the destination file path
    destination_file_path = os.path.join(destination_dir, os.path.basename(csv_file).replace(".csv", "_processed.csv"))
    
# Save the filtered data to a new CSV file in the destination directory
    filtered_df.to_csv(destination_file_path, index=False, float_format='%.6f')

#df.loc[:, columns_to_save].to_csv(r"C:\Users\ayano\Desktop\gps_time\d2_tmobile_1_minus.csv", index=False, float_format='%.6f')