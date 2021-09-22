import requests
import pandas as pd
"""
    This script iterate over the vessels positions dataset rows
    and insert each row using the call of the API endpoint
"""

df = pd.read_csv("data-fs-exercise.csv")
df = df.rename(columns={" received_time_utc": "received_time_utc", " latitude": "latitude", " longitude": "longitude"})
df = df.astype({"received_time_utc": str})
for index, row in df.iterrows():
    vessel_id = row["vessel_id"]
    latitude = row["latitude"]
    longitude = row["longitude"]
    position_time = row["received_time_utc"]

    data = {   
    "latitude": latitude,
    "longitude": longitude,
    "position_time": position_time
    }
    # Insert the row into the database
    try:
        response = requests.post(f"http://127.0.0.1:5000/vessel/{vessel_id}", data = data)
    except:
        print("ignore row")
        pass
