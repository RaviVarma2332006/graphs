import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_local_accident_data():
    """Generates monthly synthetic accident data for Lavale & Nande (Jan 2024 - Mar 2026)."""
    # Using 'ME' (Month End) for modern Pandas compatibility
    dates = pd.date_range(start="2024-01-01", end="2026-03-31", freq="ME")
    
    df = pd.DataFrame({"Date": dates})
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Year"] = df["Date"].dt.strftime('%b %Y')
    
    # Base accident rates initialized as floats to avoid strict assignment errors
    # Lavale handles much higher volume, hence a higher baseline risk
    lavale_acc = np.random.randint(2, 7, size=len(dates)).astype(float)
    # Nande is narrower but sees far less aggressive commuter traffic
    nande_acc = np.random.randint(0, 3, size=len(dates)).astype(float)
    
    # 1. Monsoon Modifier (June - September)
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    lavale_acc[monsoon_mask] *= 2.2  # Heavy skidding risk with student rush
    nande_acc[monsoon_mask] *= 1.5   # Pothole hazards, but less vehicle density
    
    # 2. Summer Drop (April - May)
    summer_mask = df["Month"].isin([4, 5])
    lavale_acc[summer_mask] *= 0.4   # Massive drop as students vacate PGs/Hostels
    nande_acc[summer_mask] *= 0.8    # Slight drop, local traffic remains
    
    # 3. Winter Smog/Fog Modifier (December - January)
    winter_mask = df["Month"].isin([12, 1])
    lavale_acc[winter_mask] *= 1.3
    nande_acc[winter_mask] *= 1.2
    
    # 4. Year-over-Year infrastructure strain
    for year, multiplier in zip([2025, 2026], [1.15, 1.25]):
        mask = df["Year"] == year
        lavale_acc[mask] *= multiplier
        nande_acc[mask] *= (multiplier - 0.05) # Nande degrading slightly slower
    
    # Round and convert to integers
    df["Lavale Village"] = np.round(lavale_acc).astype(int)
    df["Nande"] = np.round(nande_acc).astype(int)
    
    return df

# 1. Load the Data
df = generate_local_accident_data()

# 2. Melt the DataFrame so Seaborn can group the bars side-by-side
df_melted = df.melt(
    id_vars=["Date", "Month_Year", "Month"], 
    value_vars=["Lavale Village", "Nande"],
    var_name="Region", 
    value_name="Number of Accidents"
)

# 3. Set up visualization
plt.figure(figsize=(16, 7))
sns.set_theme(style="whitegrid")

# 4. Create a Grouped Bar Chart
ax = sns.barplot(
    data=df_melted,
    x="Month_Year",
    y="Number of Accidents",
    hue="Region",
    palette=["#f39c12", "#2980b9"], # Orange for Lavale, Blue for Nande
    alpha=0.85
)

# 5. Format the Graph
plt.title("Traffic-Related Accidents: Lavale Village vs. Nande (2024 - 2026)", fontsize=16, fontweight="bold")
plt.xlabel("Timeline (Monthly)", fontsize=12)
plt.ylabel("Reported & Unreported Incidents", fontsize=12)
plt.xticks(rotation=45, ha='right')

# Highlight Monsoon Months on the X-Axis in Red to show the correlation
for label in ax.get_xticklabels():
    month_str = label.get_text()
    month_num = pd.to_datetime(month_str, format='%b %Y').month
    if month_num in [6, 7, 8, 9]:
        label.set_color('#c0392b')
        label.set_fontweight('bold')

# Customize Legend
plt.legend(title="Local Zone", loc='upper left')
plt.tight_layout()
plt.show()
