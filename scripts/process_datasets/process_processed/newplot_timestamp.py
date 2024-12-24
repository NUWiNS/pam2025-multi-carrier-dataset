import glob
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from datetime import datetime
import datetime
from datetime import timezone, timedelta
import pickle
import plotly.express as px
import plotly.graph_objects as go
import time
from collections import OrderedDict
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000, '125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

# earfcn_freq_dict = {'1004' : 1970.40, '1076' : 1977.60, '2425' : 871.5, '804' : 1950.40, '854' : 1955.40, '954' : 1965.40, '1000' : 1970.00, '1001' : 1970.10, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00, '1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '132122' : 1747.5, '67061' : 2172.50}
earfcn_freq_dict = {'1004' : 1970.40, '1076' : 1977.60, '2425' : 871.5, '804' : 1950.40, '854' : 1955.40, '954' : 1965.40, '1000' : 1970.00, '1001' : 1970.10, '1025' :  1972.50, '1050' : 1975, '1075' : 1977.50, '1125' : 1982.50 , '2100' : 2125.00, '2450' : 874.0, '2460' : 875.0, '2559' : 884.90, '2560' : 885.00, '2561' : 885.10, '2600' : 889.00, '5230' : 751.00, '5780' : 739.00, '66486' : 2115.00, '66536' : 2120.00, '66561' : 2122.50, '66586' : 2125.00, '66611' : 2127.50, '66636' : 2130.0, '66686' : 2135.00, '66711' : 2137.50, '66761' : 2142.50, '66786' : 2145.00, '66811' : 2147.50, '66836' : 2150.00, '66911' : 2157.50, '66936' : 2160.00, '66986' : 2165.00, '67011' : 2167.50, '67086' : 2175.00, '750' : 1945.00, '775' : 1947.50, '825' : 1952.50, '925' : 1962.50, '950' : 1965.00, '975' : 1967.50, '800' : 1950, '1025' :  1972.50, '1075' : 1977.50, '1100' : 1980.00, '1125' : 1982.50, '1150' : 1985.00, '2175' : 2132.50, '41094' : 2640.40, '41490' : 2680.00, '5035' : 731.50, '5090' : 737.00, '5110' : 739.00, '5145' : 742.50, '5330' : 763.00, '625' : 1932.50, '650' : 1935.00, '66461' : 2112.50, '66486' : 2115.00, '66511' : 2117.50, '66611' : 2127.50, '66661' : 2132.50, '66686' : 2135.00, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66936' : 2160.00, '66985' : 2164.90, '66986' : 2165.00, '67086' : 2175.00, '675' : 1937.50, '700' : 1940.00, '800' : 1950.00, '850' : 1955.00, '875' : 1957.50, '900' : 1960.00, '925' : 1962.50, '950' : 1965, '9820' : 765.00, '1099' : 1979.90, '1100' : 1980.00, '1123' : 1982.30, '1125' : 1982.50, '1126' : 1982.60, '1148' : 1984.80, '1150' : 1985.00, '2000' : 2115.00, '2050' : 2120.00, '2125' : 2127.50, '2175' : 2132.50, '2200' : 2135.00, '2225' : 2137.50, '2300' : 2145.00, '2325' : 2147.50, '2460': 875.0,  '39750' : 2506.00, '39907' : 2521.70, '39948' : 2525.80, '40072' : 2538.20, '40384' : 2569.40, '40770' : 2608.00, '40810' : 2612.00, '41176' : 2648.60, '41238' : 2654.80, '41490' : 2680.00, '5035' : 731.50, '5090' : 737, '5095' : 737.50, '5110' : 739.00, '5330' : 763.00, '5780' : 739, '5815': 742.5, '66486': 2115.00, '66487' : 2115.10, '66536' : 2120.00, '66561' : 2122.5, '66586' : 2125, '66661' : 2132.50, '66686' : 2135, '66711' : 2137.50, '66736' : 2140.00, '66786' : 2145.00, '66811': 2147.5, '66836': 2150, '66886': 2150, '66911': 2150, '66961': 2150, '66986' : 2165.00, '67011': 2167.5, '675' : 1937.50, '676': 1937.6, '677': 1937.7, '68611': 619.5, '68636': 622, '68661': 624.5, '68686': 627, '68786': 637, '68836': 637, '68861': 637, '68886': 637, '68911': 649.5, '700' : 1940.00, '725': 1942.5, '750': 1942.5, '775': 1942.5, '801': 1950.1, '8115': 1937.5, '825': 1952.5, '8264': 1952.4, '8290': 1952.4, '8315': 1952.4, '8465': 1972.5, '850' : 1955.00, '851': 1955.1, '852': 1955.1, '8539': 1979.9, '8562': 1982.2, '8640': 1982.2, '8665': 1992.5, '875' : 1957.50, '876': 1957.6, '8763': 866.3, '877': 1957.7, '8950': 885, '901': 1960.1, '925' : 1962.50, '41305' : 2661.50, '66761' : 2142.50, '132122' : 1747.5, '67061' : 2172.50, '40680' : 2599, '40490' : 2580, '1175' : 1987.5}
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
        sec = dt_obj.timestamp() 
        return sec
    except ValueError:
        # 在遇到不符合格式的输入时返回None
        return None

def get_technology_df(tput_df, lte_only=False):
    modified_tech = None
    if lte_only == False and (len(list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())) > 0 or len(list(tput_df["5G KPI PCell RF Serving PCI"].dropna()))) > 0:
        # it is a 5G run 
        # get type of 5G 
        # max(set(freq_list), key=freq_list.count)
        freq_list = list(tput_df["5G KPI PCell RF Frequency [MHz]"].dropna())
        ffreq = float(max(set(freq_list), key=freq_list.count))
        # tput_tech_dict = {"LTE" : [], "LTE-A" : [], "low" : [], "high" : [], "high" : [], "high" : []}
        if int(ffreq) < 1000:
            modified_tech = "low"
        elif int(ffreq) > 1000 and int(ffreq) < 7000:
            modified_tech = "high"
        elif int(ffreq) > 7000 and int(ffreq) < 35000:
            modified_tech = "high"
        elif int(ffreq) > 35000:
            modified_tech = "high"
    else:
        try:
            earfcn_list = list(tput_df["LTE KPI PCell Serving EARFCN(DL)"].dropna())
        except:
            earfcn_list = list(tput_df["LTE KPI PCell Serving EARFCN(DL)"].dropna())
        if len(earfcn_list) == 0:
            pass
        else:
            lfreq = str(int(max(set(earfcn_list), key=earfcn_list.count)))
            if lfreq not in earfcn_freq_dict.keys():
                print("EARFCN not present in dict. Need to add." + str(lfreq))
                sys.exit(1)
            else:
                lfreq = earfcn_freq_dict[lfreq]
            if int(lfreq) < 1000:
                modified_tech = "low"
            elif int(lfreq) > 1000:
                modified_tech = "low"
    # if modified_tech == None:
    #     print()
    return modified_tech

base = r"D:\MPTCP\code\dl_d2"
plot_path = r"D:\base\newlogplots\9.27\d2&d3"
lte_only = False

def data_data_process(operator, data_type, lte_only=False):
    operator_df = pd.DataFrame()
    csv_directory_list = glob.glob(f"{base}\\{operator}\\{data_type}\\*.csv")
    for csv_file in csv_directory_list:
        df_short = pd.read_csv(csv_file)

        df_short_tput = df_short[df_short[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]"].notna()]
        df_short_ho = df_short[df_short['Event 5G-NR/LTE Events'].notna()]
        if len(df_short_ho) != 0:
            df_short_ho = df_short_ho[df_short_ho['Event 5G-NR/LTE Events'].str.contains("Handover Success|NR SCG Addition Success|NR SCG Modification Success")]
        
        df_merged = pd.concat([df_short_tput, df_short_ho]).sort_values(by=["GPS Time"]).reset_index(drop=True)
        if df_merged.empty:
            continue
        break_list = []
        event = -99
        start_flag = 0
        tech_list_all = []
        for index, row in df_merged.iterrows():
            if start_flag == 0:
                # first entry
                # check if event is empty or not
                if pd.isnull(row['Event 5G-NR/LTE Events']):
                    event = 0
                    start_flag = 1
                    start_index_count = 0 
                    end_index_count = 0 
                else:
                    #first entry is event
                    event = 1
                    start_flag = 1
            else:
                #row scan in progress 
                if event == 0 and pd.isnull(row['Event 5G-NR/LTE Events']):
                    #keep increasing index count
                    end_index_count+=1
                elif event == 0 and pd.notnull(row['Event 5G-NR/LTE Events']):
                    # set event to 1 : new event started
                    event = 1
                    # add truncated df to break list
                    break_list.append(df_merged[start_index_count:end_index_count+1])
                elif event == 1 and pd.notnull(row['Event 5G-NR/LTE Events']):
                    # continue with event
                    continue
                elif event == 1 and pd.isnull(row['Event 5G-NR/LTE Events']):
                    # event stopped and throughput started
                    # set event to 0
                    # set start and end index count to current index + 1
                    event = 0
                    start_index_count = index
                    end_index_count = index
        
        if event == 0:
            # add the last throughput value
            break_list.append(df_merged[start_index_count:end_index_count+1])

        mod_df_break_list = []
        for tput_df in break_list:
            tech_list = [get_technology_df(tput_df, lte_only)] * len(tput_df)
            tput_df['modified_tech'] = tech_list
            mod_df_break_list.append(tput_df)
        if len(mod_df_break_list) == 0:
            continue
        operator_df = pd.concat([operator_df, pd.concat(mod_df_break_list)])
    
    # operator_df = operator_df.sort_values(by=["GPS Time"])
    operator_df['TIME_STAMP'] = operator_df['TIME_STAMP'].apply(datetime_to_timestamp)
    operator_df = operator_df.sort_values(by=["TIME_STAMP"])
    print(operator_df.head())
    # operator_df.to_csv(f'D:/7398project/test1/class3_{operator}_{data_type}.csv', index=False)

    return operator_df

def data_cdf_plot(data_type):
    original_val_len = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_time_stamp = {"verizon" : [], "tmobile" : [], "atnt" : []}
    op_tput = {"verizon" : [], "tmobile" : [], "atnt" : []}
    color_dict = {"Verizon" : "red", "T-Mobile" : "magenta", "AT&T" : "blue"}

    vz_df = data_data_process("verizon", data_type)
    vz_df = vz_df.rename(columns={f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]": f"Verizon {data_type.upper()} Throughput"})
    vz_df = vz_df.rename(columns={"modified_tech": 'Verizon modified_tech'})
    vz_df.to_csv(f"{plot_path}/verizon_{data_type}_cdf_data.csv", index=False)  # Save data for plotting
    op_time_stamp["verizon"].extend(list(vz_df["GPS Time"]))
    op_tput["verizon"].extend(list(vz_df[f'Verizon {data_type.upper()} Throughput']))
    original_val_len["verizon"] = len(vz_df)

    tmobile_df = data_data_process("tmobile", data_type)
    tmobile_df = tmobile_df.rename(columns={f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]": f'T-Mobile {data_type.upper()} Throughput'})
    tmobile_df = tmobile_df.rename(columns={"modified_tech": 'T-Mobile modified_tech'})
    tmobile_df.to_csv(f"{plot_path}/tmobile_{data_type}_cdf_data.csv", index=False)  # Save data for plotting
    op_time_stamp["tmobile"].extend(list(tmobile_df["GPS Time"]))
    op_tput["tmobile"].extend(list(tmobile_df[f'T-Mobile {data_type.upper()} Throughput']))
    original_val_len["tmobile"] = len(tmobile_df)

    atnt_df = data_data_process("atnt", data_type)
    atnt_df = atnt_df.rename(columns={f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]": f'AT&T {data_type.upper()} Throughput'})
    atnt_df = atnt_df.rename(columns={"modified_tech": 'AT&T modified_tech'})
    atnt_df.to_csv(f"{plot_path}/atnt_{data_type}_cdf_data.csv", index=False)  # Save data for plotting
    op_time_stamp["atnt"].extend(list(atnt_df["GPS Time"]))
    op_tput["atnt"].extend(list(atnt_df[f'AT&T {data_type.upper()} Throughput']))

    fig, ax = plt.subplots(1, 3, figsize=(11, 4.5), sharey=True, constrained_layout=True)
    count = 0
    linestyle_dict = {"high-high" : 'solid', "high-low" : 'dotted', "low-low" : 'dashed', "low-high" : "dashdot"}
    color_dict = {"high-high" : "green", "high-low" : "orange", "low-high" : "red", "low-low" : "darkred"}
    label_dict = {"high-high" : 'HT - HT', "high-low" : 'HT - LT', "low-low" : 'LT - LT', "low-high" : "LT - HT"}
    get_diff_list = []
    comparison_dict = {}
    vz_df.name = "Verizon"
    tmobile_df.name = "TMobile"
    atnt_df.name = "AT&T"
    for pair in [(vz_df, tmobile_df), (tmobile_df, atnt_df), (atnt_df, vz_df)]:
        print("***************************************")
        pair_key = f"{pair[0].name}-{pair[1].name}"
        if pair_key not in comparison_dict:
            comparison_dict[pair_key] = []
        op1, op2 = pair
        # print(op1)
        op2['TIME_STAMP_CHECK'] = op2['TIME_STAMP']
        df_merged = pd.merge_asof(op1, op2, on="TIME_STAMP", direction="forward", tolerance=0)
        # df_merged.to_csv(f'D:/7398project/test1/{pair_key}_{data_type}.csv', index=False)
        vz_list = f"Verizon {data_type.upper()} Throughput"
        tmobile_list = f"T-Mobile {data_type.upper()} Throughput"
        atnt_list = f"AT&T {data_type.upper()} Throughput"
        if count == 0:
            df_merged = df_merged[[vz_list, tmobile_list, 'Verizon modified_tech', 'T-Mobile modified_tech']].dropna()
            diff_values = list(df_merged[vz_list] - df_merged[tmobile_list])
            get_diff_list.append(diff_values)
            pd.DataFrame(diff_values, columns=["Throughput Difference"]).to_csv(f"{plot_path}/verizon_tmobile_diff.csv", index=False)
            grouped = df_merged.groupby(['Verizon modified_tech', 'T-Mobile modified_tech'])
            title = "Verizon - T-Mobile"
        elif count == 1:
            df_merged = df_merged[[tmobile_list, atnt_list, 'T-Mobile modified_tech', 'AT&T modified_tech']].dropna()
            diff_values = list(df_merged[tmobile_list] - df_merged[atnt_list])
            get_diff_list.append(diff_values)
            # Save difference list to CSV for count == 1
            pd.DataFrame(diff_values, columns=["Throughput Difference"]).to_csv(f"{plot_path}/tmobile_atnt_diff.csv", index=False)
            grouped = df_merged.groupby(['T-Mobile modified_tech', 'AT&T modified_tech'])
            title = "T-Mobile - AT&T"
        else:
            df_merged = df_merged[[atnt_list, vz_list, 'AT&T modified_tech', 'Verizon modified_tech']].dropna()
            diff_values = list(df_merged[atnt_list] - df_merged[vz_list])
            get_diff_list.append(diff_values)
            # Save difference list to CSV for count == 2
            pd.DataFrame(diff_values, columns=["Throughput Difference"]).to_csv(f"{plot_path}/atnt_verizon_diff.csv", index=False)
            grouped = df_merged.groupby(['AT&T modified_tech', 'Verizon modified_tech'])
            title = "AT&T - Verizon"
        
        grouped_dataframes = [group for name, group in grouped]
        print(f"Comparison {data_type.upper()} == " + title)
        for grouped_dataframe in grouped_dataframes:
            group_filtered_columns = [col for col in grouped_dataframe.columns if "modified_tech" in col]
            group_filtered_df = grouped_dataframe[group_filtered_columns]
            group_type = group_filtered_df.iloc[:, 0].iloc[0] + "-" + group_filtered_df.iloc[:, 1].iloc[0]
            filtered_columns = [col for col in grouped_dataframe.columns if "Throughput" in col]
            # Create a new DataFrame with the filtered columns
            filtered_df = grouped_dataframe[filtered_columns]
            diff_list = []
            for first_val, second_val in zip(list(filtered_df.iloc[:, 0]), list(filtered_df.iloc[:, 1])):
                diff_list.append(first_val - second_val)
            diff_list_sorted = np.sort(diff_list)
            if len(diff_list_sorted) > 20:
                ax[count].plot(diff_list_sorted, np.linspace(0, 1, diff_list_sorted.size), linewidth=4,  label=label_dict[group_type], color=color_dict[group_type])
                comparison_length = str(len(diff_list_sorted))
                print(label_dict[group_type] + " == " + comparison_length)
                comparison_dict[pair_key].append(comparison_length)
            else:
                comparison_length = str(len(diff_list_sorted))
                print(label_dict[group_type] + " == " + comparison_length)
                comparison_dict[pair_key].append(comparison_length)

        if count == 0:
            ax[count].set_ylabel("CDF", fontsize=25)
        if count == 2:
            ax[count].legend(loc='upper left', fontsize=14.5)

        fig.text(0.5, 0.02, 'Throughput Difference (Mbps)', ha='center', fontsize=25, fontweight='bold')
        plt.subplots_adjust(bottom=0.5)
        ax[count].axvline(0, linewidth=2, linestyle='--', color="gray")
        ax[count].axhline(0.5, linewidth=2, linestyle='--', color="gray")
        ax[count].set_ylim(ymin=0, ymax= 1)
        
        if data_type == "dl":
            ax[count].set_xlim(-200, 200)
            save_name = "fig_6_c_d2&d3"
        else:
            ax[count].set_xlim(-50, 50)
            save_name = "fig_6_d_d2&d3"    
        ax[count].set_title(title, fontweight='bold', fontsize=20)
        count+=1
    plt.tick_params(axis='both', labelsize=15)
    plt.savefig(f"{plot_path}/{save_name}.pdf")
    
    return get_diff_list, comparison_dict


def main_function():

    dl_diff_list, dl_comparison_dict= data_cdf_plot("dl")
    ul_diff_list, ul_comparison_dict= data_cdf_plot("ul")

    dl_comparison_df = pd.DataFrame.from_dict(dl_comparison_dict, orient='index').transpose()
    dl_comparison_df.to_csv(f"{plot_path}/dl_comparison_dict.csv", index=False)

    ul_comparison_df = pd.DataFrame.from_dict(ul_comparison_dict, orient='index').transpose()
    ul_comparison_df.to_csv(f"{plot_path}/ul_comparison_dict.csv", index=False)

    # combined cdf
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    count = 0
    new_color_dict = {0 : 'red', 1 : 'magenta', 2 : 'blue'}
    label_dict = {0 : "(Verizon - T-Mobile)", 1 : "(T-Mobile - AT&T)", 2 : "(AT&T - Verizon)"}
    while count < 3:
        ax[0].plot(np.sort(dl_diff_list[count]), np.linspace(0, 1, len(np.sort(dl_diff_list[count]))), linewidth=4, label=label_dict[count], color=new_color_dict[count])
        count+=1
    while count < 6:
        ax[1].plot(np.sort(ul_diff_list[count%3]), np.linspace(0, 1, len(np.sort(ul_diff_list[count%3]))), linewidth=4, label=label_dict[count%3], color=new_color_dict[count%3])
        count+=1
    ax[0].set_ylabel("CDF",fontsize = 25)
    ax[0].set_xlabel("Downlink\nThroughput Difference (Mbps)", fontsize=18)
    ax[1].set_xlabel("Uplink\nThroughput Difference (Mbps)", fontsize=18)
    ax[1].legend(loc='best', fontsize=13)
    ax[0].axvline(0, linewidth=2.5, linestyle='--', color="black")
    ax[1].axvline(0, linewidth=2.5, linestyle='--', color="black")
    ax[0].axhline(0.5, linewidth=2.5, linestyle='--', color="black")
    ax[1].axhline(0.5, linewidth=2.5, linestyle='--', color="black")
    ax[0].set_ylim(ymin=0)
    ax[0].set_xlim(-200, 200)
    ax[1].set_xlim(-50, 50)
    ax[0].set_xticks([-200, -100, 0, 100, 200])
    ax[1].set_ylim(ymin=0)
    plt.tick_params(axis='both', labelsize=15)
    plt.tight_layout()
    plt.savefig(plot_path + r"\\fig_6a_d2&d3.pdf")
    plt.close()
    
    
    # pi chart 

    labels = ["HT - HT", "HT - LT", "LT - HT", "LT - LT"]
    color_dict = {"high-high" : "green", "high-low" : "orange", "low-high" : "red", "low-low" : "darkred"}
    colors = color_dict.values()
    fig, ax = plt.subplots(2, 3, figsize=(8, 4.5))
    count = 0
    print(dl_comparison_dict)
    
    for key in dl_comparison_dict.keys():
        print(f"Data for key {key}: {dl_comparison_dict[key]}")
        print(f"Labels: {labels}")
        print(f"Length of data: {len(dl_comparison_dict[key])}, Length of labels: {len(labels)}")
        ax[0][count].pie(dl_comparison_dict[key], colors=colors, labels=labels)
        ax[0][count].set_title(key, fontsize=14, fontweight='bold')
        count+=1
    ax[0][0].set_ylabel("DL", rotation=0)
    count = 0
    for key in ul_comparison_dict.keys():
        ax[1][count].pie(ul_comparison_dict[key], colors=colors, labels=labels)
        count+=1
    ax[1][0].set_ylabel("UL", rotation=0)

    ax[0, -1].legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=13)
    # plt.legend(labels=labels, bbox_to_anchor = (1.1, 1.1), loc='center right', ncols=4, fontsize=13)
    plt.tight_layout()
    plt.savefig(plot_path + r"\\fig_6b_d2&d3.pdf")
    plt.close()
        

if __name__ == "__main__":
    main_function()




