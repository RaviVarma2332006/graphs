import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_accident_data():
    """Generates monthly synthetic accident data for Sus-Pashan (Jan 2024 - Mar 2026)."""
    # Using 'ME' (Month End) for modern Pandas compatibility
    dates = pd.date_range(start="2024-01-01", end="2026-03-31", freq="ME")
    
    df = pd.DataFrame({"Date": dates})
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    
    # Base accident rate initialized as floats to avoid strict assignment errors later
    df["Accidents"] = np.random.randint(5, 12, size=len(dates)).astype(float)
    
    # Pune Monsoon Modifier (June - September): High risk of skidding and potholes
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    df.loc[monsoon_mask, "Accidents"] *= 1.8
    
    # Winter Smog/Fog Modifier (December - January): Low visibility
    winter_mask = df["Month"].isin([12, 1])
    df.loc[winter_mask, "Accidents"] *= 1.3
    
    # Year-over-Year infrastructure strain
    df.loc[df["Year"] == 2025, "Accidents"] *= 1.1
    df.loc[df["Year"] == 2026, "Accidents"] *= 1.2
    
    # Finally, round the decimals and convert the whole column to integers at once
    df["Accidents"] = df["Accidents"].round().astype(int)
    
    return df

# 1. Load the Data
df = generate_accident_data()
df["Month_Year"] = df["Date"].dt.strftime('%b %Y')

# 2. Set up visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(16, 7))

# 3. Create a Bar Plot for monthly accidents
ax = sns.barplot(
    data=df, 
    x="Month_Year", 
    y="Accidents", 
    color="#e74c3c", # Alert red color for accidents
    alpha=0.7
)

# 4. Add a Rolling Average Trendline (3-month moving average)
df["Rolling_Avg"] = df["Accidents"].rolling(window=3, min_periods=1).mean()
plt.plot(
    df["Month_Year"], 
    df["Rolling_Avg"], 
    color="#2c3e50", 
    linewidth=3, 
    marker="o",
    label="3-Month Rolling Average"
)

# 5. Format the Graph
plt.title("Estimated Traffic Accidents: Sus-Gaon & Sus-Pashan Road (2024 - 2026)", fontsize=16, fontweight="bold")
plt.xlabel("Timeline", fontsize=12)
plt.ylabel("Number of Accidents (Reported & Unreported)", fontsize=12)
plt.xticks(rotation=45, ha='right')

# Highlight the Monsoon Danger Zones
for i, row in df.iterrows():
    if row["Month"] in [6, 7, 8, 9]:
        ax.patches[i].set_color('#c0392b') 
        ax.patches[i].set_edgecolor('black')

# Add a custom legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#c0392b', edgecolor='black', label='Monsoon Season Spikes (Jun-Sep)'),
    plt.Line2D([0], [0], color='#2c3e50', lw=3, marker='o', label='3-Month Rolling Average Trend')
]
plt.legend(handles=legend_elements, loc='upper left')

plt.tight_layout()
plt.show()