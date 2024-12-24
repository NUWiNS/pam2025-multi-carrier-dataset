import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

pairlist = ['atnt_tmobile', 'tmobile_verizon', 'atnt_verizon']
plot_path = r"D:\base\newlogplots\9.27"

def time_diff_csv_process(trantype):
    all_diff_data = {}
    dataframes = []
    all_result_dfs = []
    # Iterate through each option in pairlist
    for oppair in pairlist:
        csv_folder = rf"D:\base\{oppair}\{oppair}\{trantype}_timediff"
        csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))

        grouped_rows = []

        for file in csv_files:

            df = pd.read_csv(file)

            current_group = []
            current_group_type = None  # Track the current group type ('a' or 'b')

            for index, row in df.iterrows():
                row = row.copy() 
                group_df = []

                if 'Start' in str(row['handover_status_x']):
                    if current_group_type == 'b' or current_group_type is None:
                        if current_group:
                            # If there are accumulated rows in the current group, save them
                            group_df = pd.DataFrame(current_group)
                            group_df['groupnumber'] = len(dataframes)  # Add group number
                            dataframes.append(group_df)
                        # Start a new 'a' group
                        current_group = [row]
                        current_group_type = 'a'
                    else:
                        # If the current group is also 'a', discard the previous 'a' group and start fresh
                        current_group = [row]

                # Check if handover_status_y contains 'Start'
                elif 'Start' in str(row['handover_status_y']):
                    if current_group_type == 'a' or current_group_type is None:
                        # If the previous group was 'a', save it
                        if current_group:
                            # If there are accumulated rows in the current group, save them
                            group_df = pd.DataFrame(current_group)
                            group_df['groupnumber'] = len(dataframes)  # Add group number
                            dataframes.append(group_df)
                        # Start a new 'b' group
                        current_group = [row]
                        current_group_type = 'b'
                    else:
                        # If the current group is also 'b', start fresh
                        current_group = [row]

                # If the current row does not contain 'Start' in handover_status_x or handover_status_y, continue adding to the current group
                else:
                    if current_group_type is not None:
                        current_group.append(row)
            
            current_group = []
            current_group_type = None 
        
        time_diffs = []

        # Iterate through each group
        for i, group_df in enumerate(dataframes):
            # Ensure the group has data and contains at least two rows
            if len(group_df) >= 2:

                # Calculate the time difference based on group type
                if current_group_type == 'a':
                    time_diff = abs(group_df['TIME_STAMP_y'].iloc[-1] - group_df['TIME_STAMP_x'].iloc[0])
                elif current_group_type == 'b':
                    time_diff = abs(group_df['TIME_STAMP_x'].iloc[-1] - group_df['TIME_STAMP_y'].iloc[0])


                time_diffs.append(time_diff)

        # Calculate the sum of the time difference list
        sum_list = sum(time_diffs)
        print(f"{len(time_diffs)}")
        # Calculate the proportion of each time difference
        proportions = [x / sum_list for x in time_diffs]

        # Create a DataFrame containing time differences and proportions
        result_df = pd.DataFrame({
            'time_diff': time_diffs,
            'proportion': proportions
        })

        #all_result_dfs.append(result_df)
        result_df.to_csv(f"{oppair}_proportion_Result_{trantype}.csv", index=False)


def main_fuction():
    time_diff_csv_process("UL")
    time_diff_csv_process("DL")


if __name__ == '__main__':
    main_fuction()

