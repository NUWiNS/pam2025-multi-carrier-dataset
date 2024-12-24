import pandas as pd
import pickle
import os
import glob

with open(r"C:\Users\ayano\Desktop\gps_time\downlink_start_end_times.pkl", 'rb') as f:
     ul_time_ranges = pickle.load(f)['T-Mobile'] 
# Define the source and destination directories
source_dir = r"C:\Users\ayano\Desktop\gps_tmobile"
destination_dir = r"C:\Users\ayano\Desktop\gps_dl"
# Make sure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)
# Load the CSV file
csv_files = glob.glob(os.path.join(source_dir, "*.csv"))

# Process each CSV file
for csv_file in csv_files:
    # Read the CSV file
    df = pd.read_csv(csv_file, low_memory=False)

    def datetime_to_timestamp(datetime_str):
        from datetime import datetime
        #try:
        date, time_all = datetime_str.split()
        temp_date, temp_month, temp_year = date.split("/")
        temp_year = date.split("/")[0]
        temp_month = date.split("/")[1]
        temp_date = date.split("/")[2]
        datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
        dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S')
        sec = dt_obj.timestamp() 
        return sec
    #except ValueError:
        # 在遇到不符合格式的输入时返回None
    #    return None

    ul_data = pd.DataFrame()


    df['GPS Time'] = df['GPS Time'].apply(datetime_to_timestamp)
    print(df['GPS Time'])
    for start_time, end_time in ul_time_ranges:

        filtered_records = df[(df['GPS Time'] >= start_time) & (df['GPS Time'] <= end_time)]
        ul_data = pd.concat([ul_data, filtered_records])

    columns_to_save = [
        'TIME_STAMP', 'Lat', 'Lon', 'GPS Time',
        "Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps]", 
        "Smart Phone Smart Throughput Mobile Network UL Throughput [Mbps]", 
        'Event 5G-NR/LTE Events', 
        "5G KPI PCell RF Frequency [MHz]", 
        "5G KPI PCell RF Serving PCI", 
        "LTE KPI PCell Serving EARFCN(DL)"
    ]
    
    #filtered_df = df.loc[:, columns_to_save]
    
# Generate the destination file path
    destination_file_path = os.path.join(destination_dir, os.path.basename(csv_file).replace(".csv", "_dl.csv"))
    
# Save the filtered data to a new CSV file in the destination directory
    #filtered_df.to_csv(destination_file_path, index=False, float_format='%.6f')
    ul_data.loc[:, columns_to_save].to_csv(destination_file_path, index=False, float_format='%.6f')
#ul_data.loc[:, columns_to_save].to_csv(r"C:\Users\ayano\Desktop\separate_ul\dl_d2_verizon_4.csv", mode='a', header=False, index=False, float_format='%.6f')
