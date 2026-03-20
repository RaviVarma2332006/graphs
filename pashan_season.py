import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

def generate_pashan_seasonal_data():
    """Generates 3 years of synthetic traffic data with seasonal modifiers for Pashan."""
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Month"] = df["Datetime"].dt.month
    df["Year"] = df["Datetime"].dt.year
    
    # 1. Base Volume (Pashan handles heavy city and highway traffic)
    traffic = np.random.normal(loc=800, scale=120, size=len(dates))
    
    # 2. Apply Seasonal Modifiers
    # Summer (April - May): Only a minor dip. College/school traffic drops, but IT/Highway remains steady.
    summer_mask = df["Month"].isin([4, 5])
    traffic[summer_mask] *= 0.90  
    
    # Monsoon Season (June - Sept): Severe gridlock. Potholes and slow merging from the highway.
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    traffic[monsoon_mask] *= 1.35 
    
    # Festive & Winter Season (Oct - Dec): High volume due to city shopping and intercity travel
    festive_mask = df["Month"].isin([10, 11, 12])
    traffic[festive_mask] *= 1.10
    
    df["Traffic_Volume"] = traffic
    
    # 3. Add YoY Inflation to simulate rapid urbanization in West Pune
    df.loc[df["Year"] == 2024, "Traffic_Volume"] *= 1.18
    df.loc[df["Year"] == 2025, "Traffic_Volume"] *= 1.40
        
    df["Traffic_Volume"] = df["Traffic_Volume"].clip(lower=200)
    
    return df

# 1. Load and Aggregate Data
df = generate_pashan_seasonal_data()

# Calculate the monthly average for each year
monthly_avg = df.groupby(["Year", "Month"])["Traffic_Volume"].mean().reset_index()
monthly_avg["Month_Name"] = monthly_avg["Month"].apply(lambda x: calendar.month_abbr[x])

# 2. Set up the visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 8))

# 3. Create the Line Plot
# Using a bold 'magma' palette for the high-volume city data
ax = sns.lineplot(
    data=monthly_avg, 
    x="Month_Name", 
    y="Traffic_Volume", 
    hue="Year", 
    style="Year", 
    palette="magma", 
    linewidth=3,
    marker="s", # Square markers for distinction
    markersize=9
)

# 4. Format the Graph
plt.title("Seasonal Traffic Impact: Pashan / Sutarwadi (2023-2025)", fontsize=16, fontweight="bold")
plt.xlabel("Month of the Year", fontsize=12)
plt.ylabel("Average Hourly Traffic Volume (Vehicles)", fontsize=12)

# Highlight the distinct seasonal zones
# x-axis is zero-indexed based on the month names array (Jan=0, Apr=3, Jun=5, Oct=9)
plt.axvspan(3, 4, color='orange', alpha=0.1, label='Summer Break (Minor Drop)')
plt.axvspan(5, 8, color='blue', alpha=0.1, label='Monsoon Season (Severe Gridlock)')
plt.axvspan(9, 11, color='purple', alpha=0.05, label='Festive/Winter (High Volume)')

# Clean up the legend and move it outside the plot
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

plt.tight_layout()
plt.show()
