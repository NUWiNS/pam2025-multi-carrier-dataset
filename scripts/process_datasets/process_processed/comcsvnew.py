import pandas as pd
import numpy as np
import argparse

def process_csv_data(csv_file_path, trantype):
    # Read CSV file
    df = pd.read_csv(csv_file_path)

    # Find start and end indices
    start_list = df.index[df['handover_status'] == 'Start'].tolist()
    end_list = df.index[df['handover_status'] == 'End'].tolist()

    # Ensure that the number of start and end markers match
    if len(start_list) != len(end_list):
        print(f"The number of 'start' and 'end' markers in {csv_file_path} do not match.")

    # Extract rows between start and end
    handover_list = []
    for start, end in zip(start_list, end_list):
        handover_list.append(start)
        handover_list.append(end)

    handover_df = df.loc[handover_list].copy()

    # Extract rows where Smart Phone Smart Throughput Mobile Network DL Throughput [Mbps] is not empty
    throughput_df = df[df[f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]'].notna()].copy()

    # Return two processed DataFrames
    return handover_df, throughput_df

def match_timestamps(start_time, timestamps, tolerance=0.5):
    return any(abs(start_time - t) <= tolerance for t in timestamps)

def insert_hd1_adjusted(merged_df, hd1, df1_columns):
    """
    Insert hd1 DataFrame into merged_df.
    Parameters:
    - merged_df: The DataFrame that already contains df1 and df2 data.
    - hd1: The DataFrame to be inserted, corresponding to df1 data.
    - df1_columns: List of column names corresponding to df1 in merged_df.
    
    Returns:
    - Updated DataFrame containing hd1 data.
    """
    # Adjust column names of hd1 to match df1 columns in merged_df
    hd1 = hd1.rename(columns=dict(zip(hd1.columns, df1_columns)))

    start_indices = hd1.index[hd1['handover_status_x'] == 'Start'].tolist()
    end_indices = hd1.index[hd1['handover_status_x'] == 'End'].tolist()

    merged_timestamps = merged_df['TIME_STAMP'].values

    # Find segments to keep
    segments_to_keep_1 = []
    for start, end in zip(start_indices, end_indices):
        start_time = hd1.loc[start, 'TIME_STAMP']
        if match_timestamps(start_time, merged_timestamps):
            segments_to_keep_1.append(start)
            segments_to_keep_1.append(end)

    # Filter segments to keep
    filtered_handover_df = hd1.loc[segments_to_keep_1].copy()

    # Filter rows in hd1 that fall within the merged_df timestamp range
    min_time_stamp = merged_df['TIME_STAMP'].min()
    max_time_stamp = merged_df['TIME_STAMP'].max()
    filtered_handover_df = filtered_handover_df[(filtered_handover_df['TIME_STAMP'] >= min_time_stamp) & (filtered_handover_df['TIME_STAMP'] <= max_time_stamp)]

    # Merge hd1 into merged_df
    combined_df = pd.concat([merged_df, filtered_handover_df]).sort_values('TIME_STAMP', kind='mergesort')
    
    # Fill missing values in df2 columns (assume suffix is '_y')
    df2_columns = [col for col in merged_df.columns if col.endswith('_y') and col != 'handover_status_y']
    combined_df[df2_columns] = combined_df[df2_columns].fillna(method='bfill')
    
    return combined_df

def insert_hd2_adjusted(merged_df, hd2):
    """
    Insert hd2 DataFrame into merged_df.
    Parameters:
    - merged_df: The DataFrame that already contains df1 and df2 data.
    - hd2: The DataFrame to be inserted, corresponding to df2 data.
    
    Returns:
    - Updated DataFrame containing hd2 data.
    """
    # Adjust column names of hd2 to match df2 columns in merged_df
    # Assume that all columns of df2 except the timestamp have '_y' suffix
    hd2_columns = {col: col + '_y' for col in hd2.columns if col != 'TIME_STAMP'}
    hd2_columns['TIME_STAMP'] = 'Original_TIME_STAMP_y'  # Special case for timestamp column
    hd2 = hd2.rename(columns=hd2_columns)

    start_indices = hd2.index[hd2['handover_status_y'] == 'Start'].tolist()
    end_indices = hd2.index[hd2['handover_status_y'] == 'End'].tolist()

    merged_timestamps = merged_df['Original_TIME_STAMP_y'].values

    # Find segments to keep
    segments_to_keep_2 = []
    for start, end in zip(start_indices, end_indices):
        start_time = hd2.loc[start, 'Original_TIME_STAMP_y']
        if match_timestamps(start_time, merged_timestamps):
            segments_to_keep_2.append(start)
            segments_to_keep_2.append(end)

    # Filter segments to keep
    filtered_handover_df = hd2.loc[segments_to_keep_2].copy()

    # Filter rows in hd2 that fall within the merged_df timestamp range
    min_time_stamp = merged_df['Original_TIME_STAMP_y'].min()
    max_time_stamp = merged_df['Original_TIME_STAMP_y'].max()
    filtered_handover_df = filtered_handover_df[(filtered_handover_df['Original_TIME_STAMP_y'] >= min_time_stamp) & (filtered_handover_df['Original_TIME_STAMP_y'] <= max_time_stamp)]

    # Merge hd2 into merged_df
    combined_df = pd.concat([merged_df, filtered_handover_df]).sort_values('Original_TIME_STAMP_y', kind='mergesort')

    # Fill missing values in df1 columns (those without '_y' suffix)
    df1_columns = [col for col in merged_df.columns if not col.endswith('_y') and col != 'TIME_STAMP' and col != 'handover_status_x' and col != 'TIME_STAMP']
    combined_df[df1_columns] = combined_df[df1_columns].fillna(method='bfill')

    return combined_df

def add_new_rows_based_on_end(df, suffix, trantype):
    """
    Create new rows based on 'end' markers in the handover_status column and insert them into the original DataFrame.
    Parameters:
    - df: The original DataFrame.
    - suffix: The suffix for columns (_x or _y).
    - trantype: The transaction type, 'DL' or 'UL'.
    
    Returns:
    - Updated DataFrame containing the newly created rows.
    """
    # Find the appropriate column names
    handover_column = f'handover_status{suffix}'
    timestamp_column = 'TIME_STAMP' if suffix == '_x' else 'Original_TIME_STAMP_y'
    
    # Find rows with 'end' in handover_status column
    end_rows = df[df[handover_column] == 'End']

    # Initialize a list to save new rows
    new_rows = []

    for index, row in end_rows.iterrows():
        # Get the timestamp of the 'end' row
        end_timestamp = row[timestamp_column]
        
        # Calculate new timestamp value
        new_timestamp = np.ceil(end_timestamp * 10) / 10

        # Find the corresponding throughput and modified tech values (next data)
        next_tput = df.loc[index+1:, f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]{suffix}'].values[0] if (index+1) < len(df) else None
        next_tech = df.loc[index+1:, f'modified_tech{suffix}'].values[0] if (index+1) < len(df) else None

        # Create a new row
        new_row = row.to_dict()
        new_row[handover_column] = 'newtput'
        new_row[timestamp_column] = new_timestamp
        new_row[f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]{suffix}'] = next_tput
        new_row[f'modified_tech{suffix}'] = next_tech

        # Keep the same values for all columns except the specified ones
        for col in df.columns:
            if col not in [handover_column, timestamp_column, f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]{suffix}', f'modified_tech{suffix}']:
                new_row[col] = row[col]

        # Add new row to the list
        new_rows.append((index + 1, new_row))

    # Insert new rows into the original DataFrame
    offset = 0
    for new_index, new_row in new_rows:
        actual_index = new_index + offset
        df = pd.concat([df.iloc[:actual_index], pd.DataFrame([new_row]), df.iloc[actual_index:]]).reset_index(drop=True)
        offset += 1

    return df

def calculate_timediff(df):
    """
    Calculate the time difference between TIME_STAMP and Original_TIME_STAMP_y columns and store the result in a new timediff column.
    Parameters:
    - df: The input DataFrame containing TIME_STAMP and Original_TIME_STAMP_y columns.
    
    Returns:
    - Updated DataFrame with the timediff column.
    """
    # Initialize timediff column
    df['timediff'] = None

    # Calculate timediff
    for i in range(len(df) - 1):  # Loop excluding the last row
        t_i, t_i1 = df['TIME_STAMP'].iloc[i], df['TIME_STAMP'].iloc[i + 1]
        T_i, T_i1 = df['Original_TIME_STAMP_y'].iloc[i], df['Original_TIME_STAMP_y'].iloc[i + 1]

        if (pd.isna(t_i) or pd.isna(t_i1)) and pd.notna(T_i):
            # Case where only Original_TIME_STAMP_y has a handover
            df.at[i, 'timediff'] = T_i1 - T_i
        else:
            if pd.notna(t_i) and pd.notna(t_i1):
                df.at[i, 'timediff'] = t_i1 - t_i
    
    return df


def main():
    # Assign values to variables######################################################################################
    trantype = 'DL'
    op1 = 'tmobile'
    op2 = 'verizon'
    runnum = '4'
    csv_file_path1 = rf"D:\base\{op1}\mergedata\{trantype}\{op1}{trantype}{runnum}.csv"
    csv_file_path2 = rf"D:\base\{op2}\mergedata\{trantype}\{op2}{trantype}{runnum}.csv"
    ##################################################################################################################
    # Process the two CSV files
    hd1, df1 = process_csv_data(csv_file_path1, trantype)
    hd2, df2 = process_csv_data(csv_file_path2, trantype)

    # Create a backup of the TIME_STAMP column in df2
    df2['Original_TIME_STAMP_y'] = df2['TIME_STAMP']

    # Use merge_asof to merge the two DataFrames
    df1 = df1.sort_values('TIME_STAMP')
    df2 = df2.sort_values('TIME_STAMP')
    merged_df = pd.merge_asof(df1, df2, on='TIME_STAMP', tolerance=0.5, direction='forward')
    merged_df = merged_df.dropna(subset=[f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]_y'])

    # Call function to insert hd1, passing df1 corresponding column names
    df1_columns = [col for col in merged_df.columns if not col.endswith('_y')]
    merged_with_hd1 = insert_hd1_adjusted(merged_df, hd1, df1_columns)
    merged_with_hd2 = insert_hd2_adjusted(merged_with_hd1, hd2).reset_index()

    '''
        Set Original_TIME_STAMP_y to NaN where another operator performs handover
    '''
    start_indices = merged_with_hd2.index[merged_with_hd2['handover_status_x'] == 'Start'].tolist()
    end_indices = merged_with_hd2.index[merged_with_hd2['handover_status_x'] == 'End'].tolist()

    # Ensure that the number of start and end markers match
    if len(start_indices) != len(end_indices):
        raise ValueError("The number of 'start' and 'end' markers in handover_status_x do not match.")

    # Set values in Original_TIME_STAMP_y to NaN between start and end markers
    for start, end in zip(start_indices, end_indices):
        merged_with_hd2.loc[start:end, 'Original_TIME_STAMP_y'] = pd.NA
        merged_with_hd2.loc[start:end, f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]_x'] = pd.NA

    '''
        Add a row after the end marker to restore throughput at the correct time
    '''
    merged_with_hd2 = merged_with_hd2.reset_index()
    if 'level_0' in merged_with_hd2.columns:
        merged_with_hd2 = merged_with_hd2.drop(columns=['level_0'])
    addrow_df_x = add_new_rows_based_on_end(merged_with_hd2, '_x', trantype)
    addrow_df = add_new_rows_based_on_end(addrow_df_x, '_y', trantype)
    if 'level_0' in addrow_df_x.columns:
        addrow_df_x = addrow_df_x.drop(columns=['level_0'])
    addrow_df = addrow_df.reset_index()

    '''
        Change column names and keep only useful columns
    '''
    addrow_df.rename(columns={'TIME_STAMP': 'TIME_STAMP_x'}, inplace=True)
    addrow_df.rename(columns={'Original_TIME_STAMP_y': 'TIME_STAMP_y'}, inplace=True)
    addrow_df.rename(columns={f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]_x': f'{trantype}tput_x'}, inplace=True)
    addrow_df.rename(columns={f'Smart Phone Smart Throughput Mobile Network {trantype} Throughput [Mbps]_y': f'{trantype}tput_y'}, inplace=True)
    columns_to_save = ['TIME_STAMP_x', f'{trantype}tput_x', 'modified_tech_x', 'handover_status_x','TIME_STAMP_y', f'{trantype}tput_y', 'modified_tech_y','handover_status_y']
    selected_df = addrow_df[columns_to_save]

    # Save the result#################################################################################################
    modified_df_csv_path = rf"D:\base\{op1}_{op2}\{trantype}_{op1}_{op2}_{runnum}.csv"
    ###########################################################################################################
    selected_df.to_csv(modified_df_csv_path, index=False)
    print(f"All CSV files have been merged and saved to: {modified_df_csv_path}")


if __name__ == '__main__':
    main()
