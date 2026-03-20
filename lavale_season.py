import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

def generate_local_seasonal_data():
    """Generates 3 years of synthetic traffic data with seasonal modifiers for Lavale & Nande."""
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Month"] = df["Datetime"].dt.month
    df["Year"] = df["Datetime"].dt.year
    
    # 1. Base Volumes
    lavale = np.random.normal(loc=300, scale=50, size=len(dates))
    nande = np.random.normal(loc=150, scale=30, size=len(dates))
    
    # 2. Apply Seasonal Modifiers
    # Summer Break (April - May): Massive drop for Lavale as students leave
    summer_mask = df["Month"].isin([4, 5])
    lavale[summer_mask] *= 0.55  # 45% drop in volume
    nande[summer_mask] *= 0.85   # Only a 15% drop (locals still use it)
    
    # Monsoon Season (June - Sept): Slow moving traffic, localized waterlogging
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    lavale[monsoon_mask] *= 1.40 
    nande[monsoon_mask] *= 1.30  
    
    # 3. Add YoY Inflation (Infrastructure strain)
    for year, multiplier in zip([2024, 2025], [1.12, 1.28]):
        mask = df["Year"] == year
        lavale[mask] *= multiplier
        nande[mask] *= multiplier
        
    df["Lavale Village"] = np.clip(lavale, 50, None)
    df["Nande"] = np.clip(nande, 30, None)
    
    return df

# 1. Load and Aggregate Data
df = generate_local_seasonal_data()

# Calculate the monthly average for each year
monthly_avg = df.groupby(["Year", "Month"])[["Lavale Village", "Nande"]].mean().reset_index()
monthly_avg["Month_Name"] = monthly_avg["Month"].apply(lambda x: calendar.month_abbr[x])

# 2. Melt the DataFrame so Seaborn can easily plot it
df_melted = monthly_avg.melt(
    id_vars=["Year", "Month", "Month_Name"], 
    value_vars=["Lavale Village", "Nande"],
    var_name="Region", 
    value_name="Traffic Volume"
)

# 3. Set up the visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 8))

# 4. Create the Line Plot
# Using 'style' to give each year a different line type (solid, dashed, dotted)
ax = sns.lineplot(
    data=df_melted, 
    x="Month_Name", 
    y="Traffic Volume", 
    hue="Region", 
    style="Year", 
    palette=["#f39c12", "#2980b9"], # Orange for Lavale, Blue for Nande
    linewidth=2.5,
    marker="o",
    markersize=8
)

# 5. Format the Graph
plt.title("Seasonal Traffic Impact: Lavale Village vs. Nande (2023-2025)", fontsize=16, fontweight="bold")
plt.xlabel("Month of the Year", fontsize=12)
plt.ylabel("Average Hourly Traffic Volume", fontsize=12)

# Highlight the distinct seasonal zones
# Note: x-axis is zero-indexed based on the month names array (Jan=0, Apr=3, Jun=5)
plt.axvspan(3, 4, color='orange', alpha=0.1, label='Summer Break (Low Volume)')
plt.axvspan(5, 8, color='blue', alpha=0.1, label='Monsoon Season (High Congestion)')

# Clean up the legend and move it outside the plot so it doesn't block data
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)

plt.tight_layout()
plt.show()
