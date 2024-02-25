"""
Get NYC Trip Data

"""

import pyarrow.parquet as pq
import pandas as pd

green_nov_data = pq.read_table('data/green_tripdata_2023-11.parquet')
green_nov_df: pd.DataFrame = green_nov_data.to_pandas()

# green_nov_df.to_csv("test.csv")

# print(green_nov_df.columns)

## columns
# 'VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime',
#        'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID',
#        'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
#        'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge',
#        'total_amount', 'payment_type', 'trip_type', 'congestion_surcharge']

## 0. Data Ingestion (maybe implement fetch from DB or web)

## 1. Data Cleaning

## 2. Feature Engineering

## 3. Data Aggregation and Summary Statistics

## 4. Data Visualizations

## 5. Data Filtering & Subsetting

## 6. Data Joining and Merging

## TODO merge wtih Merge with external datasets: Enrich the taxi trip data by merging it
## with external datasets, such as weather data or demographic data, to analyze
# the impact of external factors on taxi usage.