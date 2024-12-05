# Datasets
## Dataset strcture

We have organized the dataset into different sub-folders based on the raw data and the processed data we extracted:

| Data Collection Method | Raw Datasets Subfolder |
| :--- | :---: |
| XCAL | [xcal_raw](./xcal_raw) |
| ICMPbased_PING | [rtt](./rtt) |
*Note: ICMP-based_PING only contains data from Drive2 and Drive3.

| Type | Intermidiate Datasets Subfolder | Details |
| :--- | :---: | :---: |
| Extracted XCAL datasets | [xcal_processed](./xcal_processed) | Extracted the essential data needed for analysis, categorized into uplink and downlink. |
| RTT aligned with different cellular technologies | [rtt_aligned](./rtt_aligned) | Aligned RTT data with the cellular technology in use at the corresponding timestamp. |

