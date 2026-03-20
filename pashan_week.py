import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def generate_pashan_daytype_data():
    """Generates 3 years of synthetic hourly traffic for Pashan, split by Weekday/Weekend."""
    dates = pd.date_range(start="2023-01-01", end="2025-12-31 23:00:00", freq="h")
    df = pd.DataFrame({"Datetime": dates})
    df["Hour"] = df["Datetime"].dt.hour
    df["DayOfWeek"] = df["Datetime"].dt.weekday
    
    # Categorize into Weekday (0-4) and Weekend (5-6)
    df["DayType"] = np.where(df["DayOfWeek"] < 5, "Weekday", "Weekend")
    df["Year"] = df["Datetime"].dt.year
    
    # Base Volume (Pashan is always relatively busy)
    traffic = np.random.normal(loc=600, scale=100, size=len(dates))
    
    # 1. Apply Weekday Commuter Peaks (IT + Highway + University)
    weekday_morning = (df["Hour"].isin([8, 9, 10, 11])) & (df["DayType"] == "Weekday")
    weekday_evening = (df["Hour"].isin([17, 18, 19, 20, 21])) & (df["DayType"] == "Weekday")
    
    traffic[weekday_morning] += np.random.normal(1200, 150, weekday_morning.sum())
    traffic[weekday_evening] += np.random.normal(1400, 200, weekday_evening.sum())
    
    # 2. Apply Weekend Patterns (City Outings + Highway Travel)
    # Mornings are quiet, but afternoons and late evenings swell significantly
    weekend_afternoon = (df["Hour"].isin([12, 13, 14, 15, 16])) & (df["DayType"] == "Weekend")
    weekend_evening = (df["Hour"].isin([17, 18, 19, 20, 21, 22])) & (df["DayType"] == "Weekend")
    
    traffic[weekend_afternoon] += np.random.normal(400, 100, weekend_afternoon.sum())
    traffic[weekend_evening] += np.random.normal(900, 150, weekend_evening.sum())
    
    df["Traffic_Volume"] = traffic
    
    # 3. Add YoY Inflation to simulate worsening city congestion
    df.loc[df["Year"] == 2024, "Traffic_Volume"] *= 1.18
    df.loc[df["Year"] == 2025, "Traffic_Volume"] *= 1.40
    
    # Clean up minimums
    df["Traffic_Volume"] = df["Traffic_Volume"].clip(lower=200)
    
    return df

# 1. Load the Data
df = generate_pashan_daytype_data()

# 2. Set up visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(15, 7))

# 3. Create the Line Plot comparing Weekday vs Weekend
ax = sns.lineplot(
    data=df, 
    x="Hour", 
    y="Traffic_Volume", 
    hue="DayType",      
    style="DayType",    
    palette=["#8e44ad", "#2ecc71"], # Purple for Weekday, Green for Weekend
    linewidth=3.5,
    errorbar=None       
)

# 4. Format the Graph
plt.title("Weekday vs. Weekend Traffic: Pashan / Sutarwadi Gateway (2023-2025)", fontsize=16, fontweight="bold")
plt.xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
plt.ylabel("Average Hourly Traffic Volume (Vehicles)", fontsize=12)
plt.xticks(np.arange(0, 24, 1))

# Highlight the distinct behavioral shifts
plt.axvspan(8, 11, color='purple', alpha=0.08, label='Weekday Morning Commute')
plt.axvspan(17, 22, color='green', alpha=0.08, label='Weekend Evening Leisure/Highway Rush')

# Clean up the legend
handles, labels = ax.get_legend_handles_labels()
plt.legend(handles=handles, title="Day Type & Key Zones", loc="upper left")

plt.tight_layout()
plt.show()