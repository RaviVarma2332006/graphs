import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_patch_accident_data():
    """Generates comparative synthetic accident data isolating the Sunny's World steep patch."""
    dates = pd.date_range(start="2024-01-01", end="2026-03-31", freq="ME")
    df = pd.DataFrame({"Date": dates})
    df["Month"] = df["Date"].dt.month
    df["Month_Year"] = df["Date"].dt.strftime('%b %Y')
    
    # 1. General Sus-Pashan stretch (excluding the steep hill)
    general_accidents = np.random.randint(3, 8, size=len(dates)).astype(float)
    
    # 2. Sunny's World to SIT (Steep Gradient)
    # Base accidents are lower (it's a shorter physical distance), but highly volatile
    steep_patch_accidents = np.random.randint(1, 4, size=len(dates)).astype(float)
    
    # Apply Monsoon Multipliers (June - Sept)
    monsoon_mask = df["Month"].isin([6, 7, 8, 9])
    
    # General road gets a standard 1.3x wet-road bump
    general_accidents[monsoon_mask] *= 1.3
    
    # Steep patch gets a MASSIVE 3.5x bump due to waterlogging and skidding on the incline
    steep_patch_accidents[monsoon_mask] *= 3.5 
    
    # Winter Smog Multiplier (Dec - Jan)
    winter_mask = df["Month"].isin([12, 1])
    general_accidents[winter_mask] *= 1.4
    steep_patch_accidents[winter_mask] *= 1.5 # Heavy fog rolling over the hill
    
    # Round and convert to integers
    df["General Route (Flatter Terrain)"] = np.round(general_accidents).astype(int)
    df["Sunny's World to SIT (Steep Patch)"] = np.round(steep_patch_accidents).astype(int)
    
    return df

# 1. Load the Data
df = generate_patch_accident_data()

# 2. Melt the DataFrame so Seaborn can group the bars side-by-side easily
df_melted = df.melt(
    id_vars=["Date", "Month_Year", "Month"], 
    value_vars=["General Route (Flatter Terrain)", "Sunny's World to SIT (Steep Patch)"],
    var_name="Road Zone", 
    value_name="Accidents"
)

# 3. Set up visualization
plt.figure(figsize=(16, 7))
sns.set_theme(style="whitegrid")

# 4. Create a Grouped Bar Chart
ax = sns.barplot(
    data=df_melted,
    x="Month_Year",
    y="Accidents",
    hue="Road Zone",
    palette=["#95a5a6", "#c0392b"], # Grey for general, Alert Red for the dangerous patch
    alpha=0.9
)

# 5. Format the Graph
plt.title("Accident Volatility: Sunny's World Steep Gradient vs. General Route (2024 - 2026)", fontsize=16, fontweight="bold")
plt.xlabel("Timeline", fontsize=12)
plt.ylabel("Number of Accidents", fontsize=12)
plt.xticks(rotation=45, ha='right')

# Highlight Monsoon Months on the X-Axis in Red
for label in ax.get_xticklabels():
    month_str = label.get_text()
    month_num = pd.to_datetime(month_str, format='%b %Y').month
    if month_num in [6, 7, 8, 9]:
        label.set_color('#c0392b')
        label.set_fontweight('bold')

# Customize Legend
plt.legend(title="Risk Zone", loc='upper left')
plt.tight_layout()
plt.show()