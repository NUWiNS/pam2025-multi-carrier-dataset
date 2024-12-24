import glob
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
import sys
import warnings

#### Add start and end of handover based on the conditions

base = r"D:\base"
#output_dir = r"C:\Users\isomer\Desktop\base\atnt\d2_addtechtest\atnt"
lte_only = False

def check_and_remove_rows(df, df_ho, df_short_tput):
    # Define the events to check
    events_to_check = [
        "Handover Success", "NR SCG Addition Success", "NR SCG Modification Success",
        "PRACH: Msg4", "PRACH: Msg2", "Handover Attempt",
        "NR SCG Addition Attempt", "NR SCG Modification Attempt"
    ]

    # Combine conditions for events to check
    conditions = df_ho['Event 5G-NR/LTE Events'].str.contains('|'.join(events_to_check))

    # Get the indices of the valid events
    valid_events_indices = df_ho.index[conditions]

    # Determine the rows to remove from tput
    indices_to_remove = []
    for index in df_short_tput.index:
        # Check if the event exists in the previous or next row
        if index - 1 in valid_events_indices or index + 1 in valid_events_indices:
            indices_to_remove.append(index)

    # Remove these rows
    df_short_tput = df_short_tput.drop(indices_to_remove)

    return df_short_tput

def process_handover(df, type):
    df_ho = df[df['Event 5G-NR/LTE Events'].notna()]
    df_ho['Event 5G-NR/LTE Events'] = df_ho['Event 5G-NR/LTE Events'].astype(str)

    # Filter rows containing specified events
    df_short_ho = df_ho[
        df_ho['Event 5G-NR/LTE Events'].str.contains("Handover Success") |
        df_ho['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Success") |
        df_ho['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Success") |
        df_ho['Event 5G-NR/LTE Events'].str.contains('PRACH: Msg4') |
        df_ho['Event 5G-NR/LTE Events'].str.contains('PRACH: Msg2') |
        df_ho['Event 5G-NR/LTE Events'].str.contains("Handover Attempt") |
        df_ho['Event 5G-NR/LTE Events'].str.contains("NR SCG Addition Attempt") |
        df_ho['Event 5G-NR/LTE Events'].str.contains("NR SCG Modification Attempt")
    ]
    #print(df_short_ho['Event 5G-NR/LTE Events'])
    df_short_tput = df[df[f"Smart Phone Smart Throughput Mobile Network {type} Throughput [Mbps]"].notna()]

    df_short_tput_cleaned = check_and_remove_rows(df, df_ho, df_short_tput)

    df_merged = pd.concat([df_short_tput_cleaned, df_short_ho]).sort_values(by=["TIME_STAMP"]).reset_index(drop=True)

    #break_ho_events_list = [] ### handover events list
    event = -99
    start_flag = 0
    temp_ho_events_break = []

    for index, row in df_merged.iterrows(): ## iterating over a list
        if start_flag == 0: ### not start yet
                    # first entry
                    # check if event is empty or not
            if pd.isnull(row['Event 5G-NR/LTE Events']): #### the row of event is nan or not
                event = 0
                start_flag = 1 ### even the event is empty, the processing is starting
            else:
                #first entry is event
                event = 1 #### find event
                start_flag = 1 
                temp_ho_events_break.append((row['Event 5G-NR/LTE Events'],index)) ### save event and timestamp
                continue
        else:
            if event == 0 and pd.notnull(row['Event 5G-NR/LTE Events']): #### find a event
                # set event to 1 : new event started
                event = 1
                        # add truncated df to break list
                        #add new event to event list
                temp_ho_events_break.append((row['Event 5G-NR/LTE Events'],index)) ####
                continue
                #df_merged.at[index, 'handover_status'] = 'handover'
            elif event == 1 and pd.notnull(row['Event 5G-NR/LTE Events']): #### if started and event not ended, continue storing event
                        # continue with event
                temp_ho_events_break.append((row['Event 5G-NR/LTE Events'],index)) 
                continue
            elif event == 1 and pd.isnull(row['Event 5G-NR/LTE Events']):
                event = 0
                event_gap = 99
                start_flag = 0

                attempt_message = 0
                success_message = 0
                msg2 = 0
                msg4 = 0
                attempt_index_list = []
                msg2_index_list = []
                msg4_index_list = []

                for events, event_idx in temp_ho_events_break:
                    if "Attempt" in events:
                        attempt_message += 1
                        attempt_index_list.append(event_idx)
                    if "Success" in events:
                        success_message += 1
                    if "Msg2" in events:
                        msg2 += 1
                        msg2_index_list.append(event_idx)
                    if "Msg4" in events:
                        msg4 += 1
                        msg4_index_list.append(event_idx)
                        #print(events)msg4 pass in there
                #print(f"Attempt Messages: {attempt_message}, Success Messages: {success_message}, Msg4 Count: {msg4}")
                #print(f"Attempt Index List: {attempt_index_list}")
                #print(f"Msg4 Index List: {msg4_index_list}")

                if attempt_message > 0 and success_message > 0:
                    if msg4 > 0:
                        df_merged.at[attempt_index_list[0], 'handover_status'] = 'Start'
                        df_merged.at[msg4_index_list[-1], 'handover_status'] = 'End'
                        msg4 = 0
                    elif msg2 > 0:
                        df_merged.at[attempt_index_list[0], 'handover_status'] = 'Start'
                        df_merged.at[msg2_index_list[-1], 'handover_status'] = 'End'
                        msg2 = 0
                temp_ho_events_break = []
                continue

    remaining_data_df = df[~df['TIME_STAMP'].isin(df_merged['TIME_STAMP'])]
    #remaining_data_df[f"Smart Phone Smart Throughput Mobile Network {type} Throughput [Mbps]"] = 0
    
    handover_df = pd.concat([df_merged, remaining_data_df])
    handover_df = handover_df[~handover_df['TIME_STAMP'].apply(lambda x: isinstance(x, str))]
    # Drop rows where 'TIME_STAMP' could not be converted
    handover_df = handover_df.sort_values(by=['TIME_STAMP']).reset_index(drop=True)

    return handover_df

operator_df = pd.DataFrame()
#csv_directory_list = glob.glob(f"{base}\\atnt\\dl\\*.csv") # Execute operation on pre-run files
#Assign values to variables##############################################################################
type = "DL"
operator = "tmobile"
csv_directory_list = glob.glob(f"{base}\\{operator}\\addtech\\{type}\\*.csv")
output_dir = rf"D:\base\{operator}\addho_notput\{type}"
##########################################################################################################
for csv_file in csv_directory_list:
    all_data_df = pd.read_csv(csv_file)
    file_name = os.path.basename(csv_file)
    base_file_name = os.path.splitext(file_name)[0]
    all_data_df['handover_status'] = None

    handover_df = process_handover(all_data_df, f"{type}")
    start_indices = handover_df[handover_df['handover_status'] == 'Start'].index.tolist()
    end_indices = handover_df[handover_df['handover_status'] == 'End'].index.tolist()

    assert len(start_indices) == len(end_indices)
    for start, end in zip(start_indices, end_indices):
        handover_df.loc[start:end, f'Smart Phone Smart Throughput Mobile Network {type} Throughput [Mbps]'] = np.nan

    file_path = os.path.join(output_dir, f'{base_file_name}_addhont.csv')
    handover_df.to_csv(file_path, index=False)
