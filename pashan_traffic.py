import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pashan_traffic_data():
    """Generates 3 years of synthetic hourly traffic for Pashan (Sutarwadi area)."""
    # Using lowercase 'h' for modern Pandas compatibility
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    df["Year"] = df["Datetime"].dt.year
    df["DayOfWeek"] = df["Datetime"].dt.dayofweek
    
    # Base traffic volume for a major city connector
    traffic_volume = np.random.normal(loc=800, scale=150, size=len(dates))
    df["Traffic_Volume"] = traffic_volume
    
    # Apply Massive Commuter Peaks (Weekdays)
    # Pashan handles IT workers, university students, and general city commuters
    morning_peak = (df["Hour"].isin([8, 9, 10, 11])) & (df["DayOfWeek"] < 5)
    df.loc[morning_peak, "Traffic_Volume"] += np.random.normal(1200, 200, size=morning_peak.sum())
    
    # Evening peak is wider as highway traffic mixes with returning city traffic
    evening_peak = (df["Hour"].isin([17, 18, 19, 20, 21])) & (df["DayOfWeek"] < 5)
    df.loc[evening_peak, "Traffic_Volume"] += np.random.normal(1400, 250, size=evening_peak.sum())
    
    # Apply Year-over-Year Growth (Reflecting the rapid urbanization of Pune West)
    df.loc[df["Year"] == 2024, "Traffic_Volume"] *= 1.18
    df.loc[df["Year"] == 2025, "Traffic_Volume"] *= 1.40
    
    # Ensure no negative or unrealistically low traffic for a major road
    df["Traffic_Volume"] = df["Traffic_Volume"].clip(lower=150)
    
    return df

# 1. Load the Data
df = generate_pashan_traffic_data()

# 2. Set up visualization style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 7))

# 3. Create a Line Plot comparing the hours, split by Year
ax = sns.lineplot(
    data=df, 
    x="Hour", 
    y="Traffic_Volume", 
    hue="Year", 
    palette="magma", # Using a bold palette for high-volume city traffic
    linewidth=3,
    marker="o",
    errorbar=None # Clean lines for presentation
)

# 4. Formatting the Graph
plt.title("Daily Timing vs. Traffic Volume: Pashan / Sutarwadi (2023-2025)", fontsize=16, fontweight="bold")
plt.xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
plt.ylabel("Average Hourly Traffic Volume (Vehicles)", fontsize=12)
plt.xticks(np.arange(0, 24, 1)) 

# Highlight the massive city/highway commuter choke points
plt.axvspan(8, 11, color='gray', alpha=0.15, label='Morning Highway/City Merge')
plt.axvspan(17, 21, color='gray', alpha=0.15, label='Evening Highway/City Merge')

# Fix legend
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, labels=labels, loc='upper left', title="Traffic Year")

plt.tight_layout()
plt.show()