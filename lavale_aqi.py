import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_local_aqi_data():
    """Generates 3 years of synthetic hourly data for Lane-Vehicle Ratio and AQI in Lavale & Nande."""
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    
    # 1. Simulate Lane-Vehicle Ratio (0.0 to 1.0)
    # Lavale handles the main brunt of the traffic
    lavale_ratio = np.random.normal(loc=0.25, scale=0.05, size=len(dates))
    # Nande is quieter, wider relative to its low traffic
    nande_ratio = np.random.normal(loc=0.15, scale=0.03, size=len(dates))
    
    # Apply Commuter Peaks
    morning_peak = df["Hour"].isin([8, 9, 10])
    evening_peak = df["Hour"].isin([17, 18, 19, 20])
    
    lavale_ratio[morning_peak] += np.random.normal(0.45, 0.08, morning_peak.sum())
    lavale_ratio[evening_peak] += np.random.normal(0.35, 0.08, evening_peak.sum())
    
    nande_ratio[morning_peak] += np.random.normal(0.20, 0.05, morning_peak.sum())
    nande_ratio[evening_peak] += np.random.normal(0.15, 0.05, evening_peak.sum())
    
    df["Lavale_Ratio"] = np.clip(lavale_ratio, 0.05, 1.0)
    df["Nande_Ratio"] = np.clip(nande_ratio, 0.05, 1.0)
    
    # 2. Simulate AQI based on Density (Villages have a cleaner baseline than the highway)
    # Base AQI ~60, spikes based on how full the road is
    df["Lavale_AQI"] = 60 + (df["Lavale_Ratio"] * 100)
    df["Nande_AQI"] = 55 + (df["Nande_Ratio"] * 80)
    
    # Apply Rolling Mean to simulate pollution lingering in the air (Accumulation)
    df["Lavale_AQI"] = df["Lavale_AQI"].rolling(window=2, min_periods=1).mean()
    df["Nande_AQI"] = df["Nande_AQI"].rolling(window=2, min_periods=1).mean()
    
    # Apply Morning Inversion Layer (Colder morning air traps exhaust fumes at ground level)
    inversion_mask = df["Hour"].isin([7, 8, 9, 10])
    df.loc[inversion_mask, "Lavale_AQI"] *= 1.25
    df.loc[inversion_mask, "Nande_AQI"] *= 1.20
    
    # Add random environmental noise (wind, dust)
    df["Lavale_AQI"] += np.random.normal(loc=0, scale=8, size=len(dates))
    df["Nande_AQI"] += np.random.normal(loc=0, scale=6, size=len(dates))
    
    return df

# 1. Load Data
df = generate_local_aqi_data()

# 2. Aggregate data by hour for the final 24-hour visualization
hourly_avg = df.groupby("Hour").mean().reset_index()

# 3. Setup the Side-by-Side Dual Axis Figure
sns.set_theme(style="white")
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=False)
fig.suptitle("Lane-Vehicle Ratio vs. AQI: Campus Base Roads (Daily Average)", fontsize=18, fontweight="bold", y=1.02)

color_ratio = '#2980b9' # Blue for Traffic
color_aqi = '#c0392b'   # Red for AQI

# --- PANEL 1: LAVALE VILLAGE ---
ax1 = axes[0]
ax1.set_title("Lavale Village (Primary Route)", fontsize=14, fontweight="bold")
ax1.set_xlabel("Hour of the Day", fontsize=12)
ax1.set_ylabel("Lane-Vehicle Ratio (0.0 - 1.0)", color=color_ratio, fontsize=12, fontweight='bold')
line1 = ax1.plot(hourly_avg["Hour"], hourly_avg["Lavale_Ratio"], color=color_ratio, linewidth=3, marker="o", label="Traffic Density (Ratio)")
ax1.tick_params(axis='y', labelcolor=color_ratio)
ax1.set_ylim(0, 1.1)
ax1.set_xticks(np.arange(0, 24, 2))
ax1.grid(True, linestyle='--', alpha=0.5)

# Secondary Axis for Lavale AQI
ax1_aqi = ax1.twinx()
ax1_aqi.set_ylabel("Air Quality Index (AQI)", color=color_aqi, fontsize=12, fontweight='bold')
line2 = ax1_aqi.plot(hourly_avg["Hour"], hourly_avg["Lavale_AQI"], color=color_aqi, linewidth=3, marker="s", label="AQI")
ax1_aqi.tick_params(axis='y', labelcolor=color_aqi)
ax1_aqi.set_ylim(40, 200)

# Highlight zones
ax1_aqi.axhspan(100, 200, color='red', alpha=0.05, label='Poor Air Quality (>100)')
lines_1 = line1 + line2
labels_1 = [l.get_label() for l in lines_1]
ax1.legend(lines_1, labels_1, loc='upper left', frameon=True)

# --- PANEL 2: NANDE ---
ax2 = axes[1]
ax2.set_title("Nande (Bypass Route)", fontsize=14, fontweight="bold")
ax2.set_xlabel("Hour of the Day", fontsize=12)
ax2.set_ylabel("Lane-Vehicle Ratio (0.0 - 1.0)", color=color_ratio, fontsize=12, fontweight='bold')
line3 = ax2.plot(hourly_avg["Hour"], hourly_avg["Nande_Ratio"], color=color_ratio, linewidth=3, marker="o", label="Traffic Density (Ratio)")
ax2.tick_params(axis='y', labelcolor=color_ratio)
ax2.set_ylim(0, 1.1) # Keeping Y-axis identical to Lavale for true visual comparison
ax2.set_xticks(np.arange(0, 24, 2))
ax2.grid(True, linestyle='--', alpha=0.5)

# Secondary Axis for Nande AQI
ax2_aqi = ax2.twinx()
ax2_aqi.set_ylabel("Air Quality Index (AQI)", color=color_aqi, fontsize=12, fontweight='bold')
line4 = ax2_aqi.plot(hourly_avg["Hour"], hourly_avg["Nande_AQI"], color=color_aqi, linewidth=3, marker="s", label="AQI")
ax2_aqi.tick_params(axis='y', labelcolor=color_aqi)
ax2_aqi.set_ylim(40, 200) # Keeping Y-axis identical to Lavale

# Highlight zones
ax2_aqi.axhspan(100, 200, color='red', alpha=0.05) # No label here to avoid cluttering the second panel
lines_2 = line3 + line4
labels_2 = [l.get_label() for l in lines_2]
ax2.legend(lines_2, labels_2, loc='upper left', frameon=True)

plt.tight_layout()
plt.show()
