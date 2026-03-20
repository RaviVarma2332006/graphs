import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pashan_aqi_data():
    """Generates 3 years of synthetic hourly data for Lane-Vehicle Ratio and AQI in Pashan."""
    # Using lowercase 'h' for modern Pandas compatibility
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    
    # 1. Simulate Lane-Vehicle Ratio (0.0 to 1.0)
    # Pashan has a high baseline because of continuous city and highway transit
    base_ratio = np.random.normal(loc=0.45, scale=0.08, size=len(dates))
    df["Lane_Vehicle_Ratio"] = base_ratio
    
    # Massive, wide Morning Peak (8 AM - 11 AM)
    morning_peak = df["Hour"].isin([8, 9, 10, 11])
    df.loc[morning_peak, "Lane_Vehicle_Ratio"] += np.random.normal(loc=0.40, scale=0.1, size=morning_peak.sum())
    
    # Massive, wide Evening Peak (5 PM - 9 PM)
    evening_peak = df["Hour"].isin([17, 18, 19, 20, 21])
    df.loc[evening_peak, "Lane_Vehicle_Ratio"] += np.random.normal(loc=0.45, scale=0.1, size=evening_peak.sum())
    
    # Cap the ratio at 1.0 (Gridlock)
    df["Lane_Vehicle_Ratio"] = df["Lane_Vehicle_Ratio"].clip(0.1, 1.0)
    
    # 2. Simulate AQI based on Traffic Density
    # Base AQI for Pashan is higher than villages (~85) due to constant highway proximity
    df["AQI"] = 85 + (df["Lane_Vehicle_Ratio"] * 130)
    
    # Add a 3-hour rolling mean to simulate severe 'Accumulation'
    # Wide traffic peaks mean exhaust fumes build up significantly over time
    df["AQI"] = df["AQI"].rolling(window=3, min_periods=1).mean()
    
    # Add Morning Inversion Layer effect (Cold morning air traps heavy highway exhaust)
    inversion_mask = df["Hour"].isin([7, 8, 9, 10, 11])
    df.loc[inversion_mask, "AQI"] *= 1.30 
    
    # Add minor random environmental noise
    df["AQI"] += np.random.normal(loc=0, scale=12, size=len(dates))
    
    return df

# 1. Load Data
df = generate_pashan_aqi_data()

# 2. Aggregate data by hour of the day
hourly_avg = df.groupby("Hour")[["Lane_Vehicle_Ratio", "AQI"]].mean().reset_index()

# 3. Visualization Setup (Dual Axis)
sns.set_theme(style="white")
fig, ax1 = plt.subplots(figsize=(15, 7))

# 4. Plot Lane-Vehicle Ratio on the primary Y-axis
color1 = '#8e44ad' # Purple for Pashan Traffic
ax1.set_xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
ax1.set_ylabel("Lane-Vehicle Ratio (0.0 - 1.0)", color=color1, fontsize=12, fontweight='bold')
line1 = ax1.plot(hourly_avg["Hour"], hourly_avg["Lane_Vehicle_Ratio"], color=color1, linewidth=3.5, marker="o", label="Traffic Density (Ratio)")
ax1.tick_params(axis='y', labelcolor=color1)
ax1.set_ylim(0, 1.1)
ax1.set_xticks(np.arange(0, 24, 1))

# 5. Create a secondary Y-axis for AQI
ax2 = ax1.twinx()  
color2 = '#c0392b' # Alert Red for AQI
ax2.set_ylabel("Air Quality Index (AQI)", color=color2, fontsize=12, fontweight='bold')
line2 = ax2.plot(hourly_avg["Hour"], hourly_avg["AQI"], color=color2, linewidth=3.5, marker="s", label="AQI")
ax2.tick_params(axis='y', labelcolor=color2)
ax2.set_ylim(50, 300)

# Highlight Hazardous Zones
ax2.axhspan(150, 300, color='red', alpha=0.08, label='Unhealthy AQI Zone (>150)')

# 6. Formatting
plt.title("Lane-Vehicle Ratio vs. Accumulating AQI: Pashan / Sutarwadi (Daily Average)", fontsize=16, fontweight="bold")

# Combine legends from both axes seamlessly
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', frameon=True)

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
