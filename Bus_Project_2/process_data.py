import json
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from datetime import datetime

print("--- 1. READING RAW DATA ---")

# LOAD THE FILE
# Your file format is a list of JSON objects. We read it carefully.
try:
    with open('trip_data.json', 'r') as f:
        content = f.read()
        # If the file is just a list of objects like {...},{...} without brackets, we wrap it.
        if not content.strip().startswith("["):
            content = "[" + content + "]"
        data = json.loads(content)
    print(f"Success: Loaded {len(data)} GPS points.")
except Exception as e:
    print(f"Error reading file: {e}")
    print("Tip: Make sure the file is named 'trip_data.json'")
    exit()

# CONVERT TO TABLE
df = pd.DataFrame(data)

# FIX DATES
# Your file uses format: "8 Jan 2018 07:41:43"
print("--- 2. CALCULATING SPEED & PHYSICS ---")
df['datetime'] = pd.to_datetime(df['Time'], format='%d %b %Y %H:%M:%S')
df = df.sort_values('datetime').reset_index(drop=True)

# CALCULATE SPEED
# We have Latitude/Longitude. We need Speed (Distance / Time).
distances = [0]
time_deltas = [0]
lats = df['Latitude'].astype(float).values
lons = df['Longitude'].astype(float).values
times = df['datetime'].values

for i in range(1, len(df)):
    # Time diff in seconds
    t_diff = (times[i] - times[i-1]) / np.timedelta64(1, 's')
    
    # Distance in meters (Geodesic formula)
    try:
        dist = geodesic((lats[i-1], lons[i-1]), (lats[i], lons[i])).meters
    except:
        dist = 0
        
    distances.append(dist)
    time_deltas.append(t_diff)

df['time_delta'] = time_deltas
df['dist_meters'] = distances

# Speed = Distance / Time
# Use numpy to handle division safely
df['speed_mps'] = np.where(np.array(time_deltas) > 0, np.array(distances) / np.array(time_deltas), 0)
df['speed_kmph'] = df['speed_mps'] * 3.6

# FILTER NOISE (Real GPS data is jumpy)
# Remove speeds > 90 km/h (Impossible for a city bus)
clean_df = df[(df['speed_kmph'] >= 0) & (df['speed_kmph'] < 90)].copy()

# Smooth the data (Moving Average) to look like a real cycle
clean_df['speed_smooth'] = clean_df['speed_kmph'].rolling(window=5, min_periods=1).mean()

# SAVE CLEAN DATA
# We only need Time (relative to start) and Speed
clean_df['time_rel'] = (clean_df['datetime'] - clean_df['datetime'].iloc[0]).dt.total_seconds()
final_df = clean_df[['time_rel', 'speed_smooth']].rename(columns={'time_rel': 'time', 'speed_smooth': 'speed'})

final_df.to_csv('real_bus_cycle.csv', index=False)
print("--- SUCCESS ---")
print(f"File 'real_bus_cycle.csv' created.")
print(f"Trip Duration: {final_df['time'].max()/60:.1f} minutes.")