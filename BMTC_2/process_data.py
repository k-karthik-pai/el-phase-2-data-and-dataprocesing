import pandas as pd
import numpy as np

print("--- 1. READING REAL-WORLD BMTC DATA (FIXING TIME FORMAT) ---")

# 1. READ THE FILE
try:
    df = pd.read_csv('new_data.txt')
    print(f"Success: Loaded {len(df)} data points.")
except FileNotFoundError:
    print("Error: Could not find 'new_data.txt'. Please rename your file and try again.")
    exit()

# 2. CONVERT TIME TO "SECONDS FROM START"
# This fixes the error! The other scripts want numbers (0, 1, 2...), not dates.
df['datetime'] = pd.to_datetime(df['date time'])
start_time = df['datetime'].iloc[0]

# Calculate seconds elapsed since the first point
df['time_seconds'] = (df['datetime'] - start_time).dt.total_seconds()

# 3. GET SPEED
# Convert m/s to km/h
df['speed_kmph'] = df['speed(m/s)'] * 3.6

print("--- 2. CLEANING DATA ---")

# 4. FILTER NOISE
# If speed is tiny (< 1 km/h), mark it as stopped (0)
df.loc[df['speed_kmph'] < 1, 'speed_kmph'] = 0

# Remove errors (speed > 90 km/h)
clean_df = df[(df['speed_kmph'] >= 0) & (df['speed_kmph'] < 90)].copy()

# 5. SAVE STANDARD FORMAT (Time in Seconds, Speed in km/h)
final_output = pd.DataFrame()
final_output['time'] = clean_df['time_seconds']  # <--- NOW IT IS SECONDS (0, 1.0, 2.0...)
final_output['speed'] = clean_df['speed_kmph']

final_output.to_csv('real_bus_cycle.csv', index=False)

print("Done! Created 'real_bus_cycle.csv' with corrected TIME format.")
print("Now your main1.py, main2.py, and obj scripts will work perfectly.")