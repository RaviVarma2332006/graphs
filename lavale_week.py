import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_local_day_type_data():
    """Generates 3 years of synthetic hourly traffic, split by Region and Day Type."""
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    df["DayOfWeek"] = df["Datetime"].dt.weekday
    
    # Categorize into Weekday (0-4) and Weekend (5-6)
    df["DayType"] = np.where(df["DayOfWeek"] < 5, "Weekday", "Weekend")
    df["Year"] = df["Datetime"].dt.year
    
    # 1. Base Volumes 
    lavale = np.random.normal(loc=200, scale=40, size=len(dates))
    nande = np.random.normal(loc=120, scale=25, size=len(dates))
    
    # 2. Apply Weekday Student/Commuter Peaks
    weekday_morning = (df["Hour"].isin([8, 9, 10])) & (df["DayType"] == "Weekday")
    weekday_evening = (df["Hour"].isin([17, 18, 19, 20])) & (df["DayType"] == "Weekday")
    
    lavale[weekday_morning] += np.random.normal(350, 50, weekday_morning.sum())
    lavale[weekday_evening] += np.random.normal(200, 40, weekday_evening.sum())
    
    nande[weekday_morning] += np.random.normal(150, 30, weekday_morning.sum())
    nande[weekday_evening] += np.random.normal(100, 20, weekday_evening.sum())
    
    # 3. Apply Weekend Patterns (Flatter, with a slight afternoon/evening bump for outings)
    weekend_afternoon = (df["Hour"].isin([15, 16, 17, 18, 19])) & (df["DayType"] == "Weekend")
    lavale[weekend_afternoon] += np.random.normal(100, 30, weekend_afternoon.sum())
    nande[weekend_afternoon] += np.random.normal(50, 15, weekend_afternoon.sum())

    # 4. Add YoY Inflation to simulate worsening infrastructure strain
    for year, multiplier in zip([2024, 2025], [1.15, 1.35]):
        mask = df["Year"] == year
        lavale[mask] *= multiplier
        nande[mask] *= multiplier

    # Combine into a tidy format for Seaborn
    df["Lavale Village"] = np.clip(lavale, 30, None)
    df["Nande"] = np.clip(nande, 20, None)
    
    df_melted = df.melt(
        id_vars=["Hour", "DayType"], 
        value_vars=["Lavale Village", "Nande"],
        var_name="Region", 
        value_name="Traffic Volume"
    )
    return df_melted

# 1. Load the Data
df_melted = generate_local_day_type_data()

# 2. Set up a two-panel visualization
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(18, 7), sharey=True)

# Define color palettes
palette_lavale = {"Weekday": "#d35400", "Weekend": "#e67e22"} # Dark and light orange
palette_nande = {"Weekday": "#2980b9", "Weekend": "#3498db"}  # Dark and light blue

# 3. Plot Panel 1: Lavale Village
sns.lineplot(
    ax=axes[0],
    data=df_melted[df_melted["Region"] == "Lavale Village"],
    x="Hour", y="Traffic Volume", hue="DayType", style="DayType",
    palette=palette_lavale, linewidth=3, errorbar=None
)
axes[0].set_title("Lavale Village: Weekday vs. Weekend", fontsize=14, fontweight="bold")
axes[0].set_xlabel("Hour of the Day", fontsize=12)
axes[0].set_ylabel("Average Hourly Traffic Volume", fontsize=12)
axes[0].set_xticks(np.arange(0, 24, 2))
axes[0].axvspan(8, 10, color='gray', alpha=0.1) # Morning highlight

# 4. Plot Panel 2: Nande
sns.lineplot(
    ax=axes[1],
    data=df_melted[df_melted["Region"] == "Nande"],
    x="Hour", y="Traffic Volume", hue="DayType", style="DayType",
    palette=palette_nande, linewidth=3, errorbar=None
)
axes[1].set_title("Nande: Weekday vs. Weekend", fontsize=14, fontweight="bold")
axes[1].set_xlabel("Hour of the Day", fontsize=12)
axes[1].set_xticks(np.arange(0, 24, 2))
axes[1].axvspan(8, 10, color='gray', alpha=0.1) # Morning highlight

# 5. Global Formatting
fig.suptitle("Campus Base Traffic Analysis (2023-2025 Aggregate)", fontsize=18, fontweight="bold", y=1.02)
plt.tight_layout()
plt.show()
