import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_local_traffic_data():
    """Generates 3 years of synthetic hourly traffic for Lavale Village and Nande."""
    # Using lowercase 'h' for strict Pandas compatibility
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    
    # 1. Base Volumes (Lavale is the primary base, Nande is the bypass)
    lavale_vol = np.random.normal(loc=250, scale=50, size=len(dates))
    nande_vol = np.random.normal(loc=150, scale=30, size=len(dates))
    
    # 2. Apply Commuter Peaks
    morning_peak = df["Hour"].isin([8, 9, 10])
    evening_peak = df["Hour"].isin([17, 18, 19, 20])
    
    # Lavale gets a sharp morning peak (Students rushing to base of the hill for early lectures)
    lavale_vol[morning_peak] += np.random.normal(400, 60, morning_peak.sum())
    lavale_vol[evening_peak] += np.random.normal(250, 50, evening_peak.sum())
    
    # Nande gets moderate overflow traffic as an alternative route
    nande_vol[morning_peak] += np.random.normal(200, 40, morning_peak.sum())
    nande_vol[evening_peak] += np.random.normal(150, 30, evening_peak.sum())
    
    # 3. Add YoY Inflation to simulate worsening congestion over the 3 years
    df["Year"] = df["Datetime"].dt.year
    for year, multiplier in zip([2024, 2025], [1.15, 1.35]):
        mask = df["Year"] == year
        lavale_vol[mask] *= multiplier
        nande_vol[mask] *= multiplier

    # 4. Assign to DataFrame and clip negatives
    df["Lavale Village"] = np.clip(lavale_vol, 30, None)
    df["Nande"] = np.clip(nande_vol, 20, None)
    
    return df

# 1. Load the Data
df = generate_local_traffic_data()

# 2. Melt the DataFrame to make it easy for Seaborn to plot the two lines
df_melted = df.melt(
    id_vars=["Hour"], 
    value_vars=["Lavale Village", "Nande"],
    var_name="Region", 
    value_name="Traffic Volume"
)

# 3. Set up the visualization
plt.figure(figsize=(14, 7))
sns.set_theme(style="whitegrid")

# 4. Create the Line Plot 
ax = sns.lineplot(
    data=df_melted,
    x="Hour",
    y="Traffic Volume",
    hue="Region",
    palette=["#f39c12", "#2980b9"], # Orange for Lavale, Blue for Nande
    linewidth=3,
    marker="o",
    errorbar=None # Turning off shaded variance for a cleaner view
)

# 5. Format the Graph
plt.title("Daily Traffic Volume: Lavale Village vs. Nande (2023-2025 Avg)", fontsize=16, fontweight="bold")
plt.xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
plt.ylabel("Average Hourly Traffic Volume (Vehicles)", fontsize=12)

# Ensure all 24 hours are shown on the X-axis
plt.xticks(np.arange(0, 24, 1))

# Highlight the commuter choke points
plt.axvspan(8, 10, color='gray', alpha=0.1, label='Morning Rush (Classes Start)')
plt.axvspan(17, 20, color='gray', alpha=0.1, label='Evening Rush (Campus Exit)')

# Fix legend to avoid duplicate "Region" title and background spans
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, labels=labels, loc='upper left', title="Local Zones")

plt.tight_layout()
plt.show()
