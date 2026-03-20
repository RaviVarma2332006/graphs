import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_hourly_accident_data():
    """Generates an aggregated hourly breakdown of accidents over a 2-year period."""
    hours = np.arange(24)
    
    # Simulated baseline distribution of accidents by hour for the last 2 years
    # General route: Peaks steadily with standard city commuter traffic
    general_base = [5, 3, 2, 2, 4, 10, 20, 35, 45, 50, 35, 25, 22, 20, 25, 35, 45, 55, 60, 45, 30, 20, 15, 8]
    
    # Steep Patch (Sunny's World): Sharper peaks during college rush hours, 
    # and a disproportionate bump late at night due to dark, steep descents
    steep_base = [8, 6, 4, 2, 3, 8, 15, 30, 65, 70, 25, 15, 12, 12, 15, 25, 40, 50, 45, 35, 25, 20, 18, 12]
    
    # Add slight organic variance to the synthetic data
    np.random.seed(42) # Keeps the random noise consistent each time you run it
    general = np.array(general_base) + np.random.randint(-4, 5, size=24)
    steep_patch = np.array(steep_base) + np.random.randint(-4, 5, size=24)
    
    # Ensure no negative numbers just in case
    general = np.clip(general, 0, None)
    steep_patch = np.clip(steep_patch, 0, None)

    # Build the DataFrame
    df = pd.DataFrame({
        "Hour": hours,
        "General Route (Flatter Terrain)": general,
        "Sunny's World to SIT (Steep Patch)": steep_patch
    })
    return df

# 1. Load the Data
df = generate_hourly_accident_data()

# 2. Melt the DataFrame so Seaborn can plot two lines easily
df_melted = df.melt(
    id_vars=["Hour"], 
    value_vars=["General Route (Flatter Terrain)", "Sunny's World to SIT (Steep Patch)"],
    var_name="Road Zone", 
    value_name="Total Accidents (2-Year Aggregate)"
)

# 3. Set up the visualization
plt.figure(figsize=(15, 7))
sns.set_theme(style="whitegrid")

# 4. Create a Line Plot with shaded areas
ax = sns.lineplot(
    data=df_melted,
    x="Hour",
    y="Total Accidents (2-Year Aggregate)",
    hue="Road Zone",
    palette=["#7f8c8d", "#c0392b"], # Grey for general, Alert Red for the dangerous patch
    linewidth=3,
    marker="o",
    markersize=8
)

# Fill the area under the steep patch line to emphasize the danger volume
steep_data = df["Sunny's World to SIT (Steep Patch)"]
plt.fill_between(df["Hour"], steep_data, color="#c0392b", alpha=0.1)

# 5. Format the Graph
plt.title("Time-of-Day Accident Analysis: Sus-Pashan vs. Sunny's World Gradient (2024-2026 Aggregate)", fontsize=15, fontweight="bold")
plt.xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
plt.ylabel("Total Number of Accidents", fontsize=12)

# Ensure all 24 hours are shown on the X-axis
plt.xticks(np.arange(0, 24, 1))

# Highlight the distinct Commuter Danger Zones
plt.axvspan(8, 10, color='gray', alpha=0.15, label='Morning Rush (8 AM - 10 AM)')
plt.axvspan(17, 19, color='gray', alpha=0.15, label='Evening Rush (5 PM - 7 PM)')

# Customize the Legend
handles, labels = ax.get_legend_handles_labels()
# Filter out duplicate legend entries caused by axvspan
plt.legend(handles=handles[:2] + handles[-2:], labels=labels[:2] + labels[-2:], loc='upper left')

plt.tight_layout()
plt.show()