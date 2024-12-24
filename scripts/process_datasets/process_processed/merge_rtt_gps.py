import pandas as pd
import glob
import os
import numpy as np

csv_dir = r"C:\Users\ayano\Desktop\gps_verizon\d2"
destination_dir = r"C:\Users\ayano\Desktop\ul_d2\verizon\d2"
csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
df2 = pd.read_csv(r"C:\Users\ayano\Desktop\rtt\verizon\d2\rtt_verizon2.csv")
def datetime_to_timestamp(datetime_str):
    from datetime import datetime
    
    try:
        date, time_all = datetime_str.split()
        temp_date, temp_month, temp_year = date.split("-")
        temp_year = date.split("-")[0]
        temp_month = date.split("-")[1]
        temp_date = date.split("-")[2]
        datetime_string = temp_date + "." + temp_month + "." + temp_year + " " + time_all
        dt_obj = datetime.strptime(datetime_string, '%d.%m.%Y %H:%M:%S.%f')
        sec = int(dt_obj.timestamp() * 1000) #change the data with no decimal part 
        #print(sec)
        return sec
    except ValueError:
        # 在遇到不符合格式的输入时返回None
        return None
     
#df2['Timestamp'] = df2['Timestamp'].apply(datetime_to_timestamp)
for csv_file in csv_files:
    df1 = pd.read_csv(csv_file, low_memory=False)
        # 将当前文件的数据追加到合并后的 DataFrame
    df1['TIME_STAMP'] = df1['TIME_STAMP'].apply(datetime_to_timestamp)
    #df1['TIME_STAMP'] = pd.to_datetime(df1['TIME_STAMP']).dt.strftime('%d.%m.%Y %H:%M:%S.%f').str[:-5]
    #df2['Timestamp'] = pd.to_datetime(df2['Timestamp']).dt.strftime('%d.%m.%Y %H:%M:%S.%f').str[:-5]
    df1['TIME_STAMP'] = df1['TIME_STAMP'].astype('int64')
    df2['Timestamp'] = df2['Timestamp'].astype('int64')
    df1.sort_values('TIME_STAMP', inplace=True)
    df2.sort_values('Timestamp', inplace=True)
    merged_df = pd.merge_asof(df1, df2, left_on='TIME_STAMP', right_on='Timestamp', tolerance=100, direction='forward')
    duplicates = merged_df.duplicated(subset=['Timestamp'], keep="first")
    merged_df.loc[duplicates, ['Timestamp', 'Time (ms)']] = np.nan
    destination_file_path = os.path.join(destination_dir, os.path.basename(csv_file).replace(".csv", "_rtt.csv"))
    merged_df.to_csv(destination_file_path, index=False)