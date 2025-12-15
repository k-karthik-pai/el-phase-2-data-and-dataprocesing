import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("--- STARTING PHASE 3: STATISTICAL VALIDATION (FINAL) ---")

# 1. PREP DATA
try:
    df = pd.read_csv('real_bus_cycle.csv')
except FileNotFoundError:
    print("Error: Run process_data.py first!")
    exit()

df['time_gap'] = df['time'].diff()
df.loc[df['time_gap'] > 5, 'speed'] = np.nan
clean_series = df['speed'].interpolate(method='linear')

# 2. RUN OPTIMIZATION (MATCHING MAIN 1 & 2)
# Window = 12 (Smoother), Cap = 70 (Faster)
ant_path = clean_series.rolling(window=12, min_periods=1).mean()
optimized_cycle = np.where(ant_path > 70, 70, ant_path)
optimized_cycle[df['speed'].isna()] = np.nan

# 3. METRICS
mask = ~np.isnan(df['speed'])
real_clean = df.loc[mask, 'speed']
opt_clean = optimized_cycle[mask]

# RMSE
mse = np.mean((real_clean - opt_clean) ** 2)
rmse = np.sqrt(mse)

# Efficiency
raw_energy = np.sum(real_clean ** 2)
opt_energy = np.sum(opt_clean ** 2)
improvement = ((raw_energy - opt_energy) / raw_energy) * 100

print(f"\n>>> VALIDATION REPORT <<<")
print(f"1. RMSE Score: {rmse:.2f} (Indicates degree of optimization correction)")
print(f"2. Efficiency Gain: {improvement:.2f}%")

# 4. PLOTS
plt.figure(figsize=(12, 5))

# Plot A: Histogram
plt.subplot(1, 2, 1)
plt.hist(real_clean, bins=40, alpha=0.5, color='gray', label='Raw Data', density=True)
plt.hist(opt_clean, bins=40, alpha=0.5, color='green', label='AI Optimized (Max 70)', density=True)
plt.title("Speed Distribution Probability")
plt.xlabel("Speed (km/h)")
plt.ylabel("Probability Density") # More professional than "Frequency"
plt.legend()

# Plot B: Scatter
plt.subplot(1, 2, 2)
plt.scatter(real_clean, opt_clean, alpha=0.1, color='black', s=5)

# *** UPDATED NAME HERE ***
plt.plot([0, 80], [0, 80], 'r--', label='Identity Line (y=x)') 

plt.title(f"Correlation Check (RMSE={rmse:.2f})")
plt.xlabel("Real Speed (km/h)")
plt.ylabel("AI Optimized Speed (km/h)")
plt.legend()

plt.tight_layout()
plt.savefig('phase3_validation_final.png')
print("Validation saved as 'phase3_validation_final.png'.")
plt.show()