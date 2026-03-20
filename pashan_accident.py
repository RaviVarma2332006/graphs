import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pashan_accident_data():
    """Generates monthly synthetic accident data for Pashan/Sutarwadi (Jan 2024 - Mar 2026)."""
    # Using 'ME' (Month End) for modern Pandas compatibility
    dates = pd.date_range(start="2024-01-01", end="2026-03-31", freq="ME")
    
    df = pd.DataFrame({"Date": dates})
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Year"] = df["Date"].dt.strftime('%b %Y')
    
    # Base accident rate (Consistently higher due to city/highway traffic volume)
    # Initialized as floats for safe math operations
    base_accidents = np.random.randint(12, 25, size=len(dates)).astype(float)
    df["Accidents"] = base_accidents
    
    # 1. Monsoon Modifier (June - September)
    # High risk of hydroplaning and high-speed merging collisions
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    df.loc[monsoon_mask, "Accidents"] *= 1.6 
    
    # 2. Winter Smog/Fog Modifier (December - January)
    # Extremely poor visibility for vehicles exiting the Katraj-Dehu Road bypass
    winter_mask = df["Month"].isin([12, 1])
    df.loc[winter_mask, "Accidents"] *= 1.4
    
    # 3. Summer Baseline (April - May)
    # Unlike the university roads, Pashan doesn't drop. IT and highway traffic remains steady.
    # No negative modifier applied here.
    
    # 4. Year-over-Year infrastructure strain (Increasing urbanization)
    df.loc[df["Year"] == 2025, "Accidents"] *= 1.15
    df.loc[df["Year"] == 2026, "Accidents"] *= 1.25
    
    # Finally, round and convert the column to integers at once
    df["Accidents"] = df["Accidents"].round().astype(int)
    
    return df

# 1. Load the Data
df = generate_pashan_accident_data()

# 2. Set up visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(16, 7))

# 3. Create a Bar Plot for monthly accidents
# Using a deep purple to maintain visual consistency with the previous Pashan graphs
ax = sns.barplot(
    data=df, 
    x="Month_Year", 
    y="Accidents", 
    color="#8e44ad", 
    alpha=0.75
)

# 4. Add a Rolling Average Trendline (3-month moving average)
df["Rolling_Avg"] = df["Accidents"].rolling(window=3, min_periods=1).mean()
plt.plot(
    df["Month_Year"], 
    df["Rolling_Avg"], 
    color="#2c3e50", 
    linewidth=3.5, 
    marker="o",
    label="3-Month Rolling Average"
)

# 5. Format the Graph
plt.title("Estimated Traffic Accidents: Pashan / Sutarwadi Gateway (2024 - 2026)", fontsize=16, fontweight="bold")
plt.xlabel("Timeline (Monthly)", fontsize=12)
plt.ylabel("Number of Accidents (Reported & Unreported)", fontsize=12)
plt.xticks(rotation=45, ha='right')

# Highlight the distinct danger zones
for i, row in df.iterrows():
    # Highlight Monsoon (Hydroplaning risk)
    if row["Month"] in [6, 7, 8, 9]:
        ax.patches[i].set_color('#c0392b') # Alert Red
        ax.patches[i].set_edgecolor('black')
    # Highlight Winter Fog (Visibility risk)
    elif row["Month"] in [12, 1]:
        ax.patches[i].set_color('#7f8c8d') # Foggy Grey
        ax.patches[i].set_edgecolor('black')

# Add a custom legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#8e44ad', label='Standard City Traffic'),
    Patch(facecolor='#c0392b', edgecolor='black', label='Monsoon Season Spikes (Jun-Sep)'),
    Patch(facecolor='#7f8c8d', edgecolor='black', label='Winter Fog Visibility Drops (Dec-Jan)'),
    plt.Line2D([0], [0], color='#2c3e50', lw=3.5, marker='o', label='3-Month Rolling Average Trend')
]
plt.legend(handles=legend_elements, loc='upper left')

plt.tight_layout()
plt.show()
