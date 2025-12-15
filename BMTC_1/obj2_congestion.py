import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("--- OBJECTIVE 2: IDENTIFY CONGESTION HOTSPOTS ---")

# 1. LOAD DATA
try:
    df = pd.read_csv('real_bus_cycle.csv')
except FileNotFoundError:
    print("Error: 'real_bus_cycle.csv' not found. Run process_data.py first!")
    exit()

# 2. PREPARE DATA (Fix "Teleporting" Lines)
df['time_gap'] = df['time'].diff()
# Lift the pen (insert NaN) if gap > 10 seconds to avoid fake straight lines
df.loc[df['time_gap'] > 10, 'speed'] = np.nan

# 3. DEFINE CONGESTION
CONGESTION_THRESHOLD = 20 
df['is_congested'] = df['speed'] < CONGESTION_THRESHOLD

# Calculate Percentage (Valid Data Only)
valid_data = df.dropna(subset=['speed'])
congestion_pct = (valid_data['is_congested'].sum() / len(valid_data)) * 100

print(f"Congestion Level: {congestion_pct:.1f}% (Speed < {CONGESTION_THRESHOLD} km/h)")

# 4. GENERATE GRAPH (Clean Version)
plt.figure(figsize=(12, 6))

# A. The Path (Gray Line)
plt.plot(df['time'], df['speed'], color='#bbbbbb', label='Free Flowing Traffic', linewidth=1)

# B. The Clusters (Red Dots) - Visualizing Density
# We only plot points that are NOT NaN
congested_data = df[ (df['is_congested']) & (df['speed'].notna()) ]
plt.scatter(congested_data['time'], congested_data['speed'], 
            color='#D62728', s=10, alpha=0.6, label=f'Congestion (<{CONGESTION_THRESHOLD} km/h)', zorder=5)

# C. The Threshold Line
plt.axhline(y=CONGESTION_THRESHOLD, color='black', linestyle='--', alpha=0.3, linewidth=1)
plt.text(df['time'].min(), CONGESTION_THRESHOLD + 1, '  Congestion Threshold (20 km/h)', 
         fontsize=9, color='black', style='italic', va='bottom')

# D. TITLES & LEGEND
plt.title(f"Congestion Analysis: {congestion_pct:.1f}% of Trip Spent in Heavy Traffic", fontsize=14)
plt.xlabel("Trip Time (seconds)")
plt.ylabel("Bus Speed (km/h)")
plt.legend(loc='upper right', frameon=True)
plt.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.savefig('obj2_congestion_graph.png')
print("Graph saved as 'obj2_congestion_graph.png'.")
plt.show()