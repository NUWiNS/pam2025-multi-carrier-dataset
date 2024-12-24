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
#####################################################
# The duration that one operator's tput is greater than the other
# need change these parameters before using it
# plot_path (output) threshold
#####################################################
if not sys.warnoptions:
    warnings.simplefilter("ignore")

arfcn_freq_dict = {'177020' : 885.100, '2083329' : 28249.800, '2071667' : 27550.080, '648672' : 3730.080, '2078331' : 27949.920, '2073333' : 27650.040, '177000' : 885.000, '174800' : 874.000, '175000' : 875.000, '650004' : 3750.060, '2239999' : 37650.000, '125400' : 627.000, '125900' : 629.500, '126400' : 632.000, '126490' :632.450, '126510' : 632.550, '126530' : 632.650, '126900' : 634.500, '506280' : 2531.400, '508296' : 2541.480, '509202' : 2546.010, '514056' : 2570.280, '520020' : 2600.100, '525204' :2626.020, '526002' : 2630.010, '526404' : 2632.020, '527202' : 2636.010, '528000' : 2640.000, '528696' : 2643.480, '529998' : 2649.990, '530700' : 2653.500}

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

base = r"D:\MPTCP\code\code\plots\dl_d2"
plot_path = r"D:\base\newlogplots\9.30"
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
    
    operator_df = operator_df.sort_values(by=["GPS Time"])
    #print(operator_df.columns)
    operator_df.to_csv(f'operator_df_{operator}_{data_type}.csv', index=False)

    return operator_df

def data_cdf_plot(data_type, tranname):
    threshold = 10
    op_time_stamp = {"verizon": [], "tmobile": [], "atnt": []}
    op_tput = {"verizon": [], "tmobile": [], "atnt": []}

    # Processing data for each provider
    vz_df = data_data_process("verizon", data_type)
    op_time_stamp["verizon"].extend(list(vz_df["GPS Time"]))
    op_tput["verizon"].extend(list(vz_df[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]"]))

    tmobile_df = data_data_process("tmobile", data_type)
    op_time_stamp["tmobile"].extend(list(tmobile_df["GPS Time"]))
    op_tput["tmobile"].extend(list(tmobile_df[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]"]))

    atnt_df = data_data_process("atnt", data_type)
    op_time_stamp["atnt"].extend(list(atnt_df["GPS Time"]))
    op_tput["atnt"].extend(list(atnt_df[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]"]))

    # Setup plot
    fig, ax = plt.subplots(figsize=(7, 6), sharey=True, constrained_layout=True)
    get_diff_list = []
    comparison_dict = {}

    pairs = [
        (vz_df, tmobile_df, "Verizon", "T-Mobile"),
        (tmobile_df, atnt_df, "T-Mobile", "AT&T"),
        (atnt_df, vz_df, "AT&T", "Verizon")
    ]

    
    color_dict = {
        "Verizon-T-Mobile": "red",
        "T-Mobile-AT&T": "magenta",
        "AT&T-Verizon": "blue"
    }

    for i, pair in enumerate(pairs):
        op1, op2, name1, name2 = pair
        pair_key = f"{name1}-{name2}"
        if pair_key not in comparison_dict:
            comparison_dict[pair_key] = []
        
        df_merged = pd.merge_asof(op1, op2, on="GPS Time", direction="forward", tolerance=0) ################change here
        
        df_merged = df_merged[['GPS Time', 'Lat_x', 'Lon_x', 'Lat_y', 'Lon_y', f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_x", f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_y", 'modified_tech_x', 'modified_tech_y']].dropna()
        get_diff_list.append(list(df_merged[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_x"] - df_merged[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_y"]))

        # Calculate mid-point lat, lon and throughput difference
        df_merged['Throughput_diff'] = df_merged[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_x"] - df_merged[f"Smart Phone Smart Throughput Mobile Network {data_type.upper()} Throughput [Mbps]_y"]

        # Calculate GPS Time difference and group by significant changes
        df_merged['GPS_Time_Diff'] = df_merged['GPS Time'].diff()
        df_merged['diff_abs_gt_threshold'] = abs(df_merged['Throughput_diff']) > threshold
        df_merged['diff_sign'] = np.sign(df_merged['Throughput_diff'])
        df_merged['new_group_gps_diff'] = df_merged['GPS_Time_Diff'] > 2
        df_merged['diff_sign_change'] = df_merged['diff_sign'] != df_merged['diff_sign'].shift()
        df_merged['threshold_status_change'] = df_merged['diff_abs_gt_threshold'] != df_merged['diff_abs_gt_threshold'].shift()
        df_merged['group'] = ((df_merged['new_group_gps_diff'] | df_merged['diff_sign_change'] | df_merged['threshold_status_change'])).cumsum()

        df_filtered = df_merged[df_merged['diff_abs_gt_threshold']]
        durations = df_filtered.groupby('group').agg(start_GPSTIME=('GPS Time', 'min'), end_GPSTIME=('GPS Time', 'max'))
        durations['duration'] = durations['end_GPSTIME'] - durations['start_GPSTIME']

        # Map durations back to the merged DataFrame
        df_merged['duration'] = df_merged['group'].map(durations['duration'].to_dict())
        df_merged['duration'] = df_merged.apply(lambda x: x['duration'] if x['diff_abs_gt_threshold'] else 0, axis=1)

        max_duration = df_merged['duration'].max()
        #df_merged.to_csv(f'df_merged_abs_{name1}-{name2}_{data_type}.csv', index=False)
        length = len(df_merged)
        print(length)

        # Calculate and plot CDF
        cdf_duration = df_merged['duration'].values
        bins = np.linspace(0, max_duration, 100)
        hist, bin_edges = np.histogram(cdf_duration, bins=bins, density=True)
        hist_df = pd.DataFrame({'bin_edges': bin_edges[:-1], 'hist': hist})
        #hist_df.to_csv(f'histogram_{name1}-{name2}_{data_type}.csv', index=False)
        cdf = np.cumsum(hist) * np.diff(bin_edges)
        cdf_df = pd.DataFrame({'bin_edges': bin_edges[:-1], 'cdf': np.cumsum(hist) * np.diff(bin_edges)})
        cdf_df.to_csv(f'cdf_{name1}-{name2}_{data_type}_{threshold}.csv', index=False)
        colorkey = color_dict.get(pair_key)
        ax.plot(bin_edges[1:], cdf, linewidth=2, color = colorkey,  label=f'{name1}-{name2}')

    ax.set_xlim(0, max_duration)
    ax.set_ylim(0, 1)
    ax.set_title(f'{tranname} (Threshold: {threshold}Mbps)', fontweight='bold', fontsize = 18)
    ax.set_xlabel("Duration (s)")
    ax.set_ylabel("CDF")
    plt.legend()
    plt.grid()
    plt.savefig(f'{plot_path}/conti_time_{threshold}_{data_type}.png')
    #plt.show()
    return

    

def main_function():

    data_cdf_plot("dl",'Downlink')
    data_cdf_plot("ul", 'Uplink')

    
        

if __name__ == "__main__":
    main_function()




