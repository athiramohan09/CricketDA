import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load specific sheet by name
df = pd.read_excel('FinalMatches.xlsx', sheet_name='Matches')

print("DataFrame Info:")
print(df.info())
# Shape of the DataFrame
print(f"\nDataFrame Shape: {df.shape}")
# Column names
print(f"\nColumn Names: {list(df.columns)}")
# Data types
print("\nData Types:")
print(df.dtypes)
print("Descriptive Statistics (Numerical):")
print(df.describe())

fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Target runs distribution
axes[0,0].hist(df['target_runs'].dropna(), bins=30, color='lightblue', edgecolor='black')
axes[0,0].set_title('Distribution of Target Runs')
axes[0,0].set_xlabel('Target Runs')
axes[0,0].set_ylabel('Frequency')


# 3. Scatter: Target Runs vs Target Overs
axes[1,0].scatter(df['target_overs'], df['target_runs'], alpha=0.6, color='blue')
axes[1,0].set_title('Target Runs vs Target Overs')
axes[1,0].set_xlabel('Target Overs')
axes[1,0].set_ylabel('Target Runs')

# 4. Boxplot of target runs by match result
df_box = df.dropna(subset=['target_runs', 'result'])
sns.boxplot(data=df_box, x='result', y='target_runs', ax=axes[1,1])
axes[1,1].set_title('Target Runs by Match Result')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()


# Home vs Away performance
plt.figure(figsize=(12, 6))

# Home team wins
home_wins = df[df['Home'] == df['winner']]['Home'].value_counts().head(10)

# Away team wins  
away_wins = df[df['Away'] == df['winner']]['Away'].value_counts().head(10)

plt.subplot(1, 2, 1)
home_wins.plot(kind='bar', color='blue', alpha=0.7)
plt.title('Top 10 Home Win Teams')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
away_wins.plot(kind='bar', color='red', alpha=0.7)
plt.title('Top 10 Away Win Teams')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Top venues and their toss decisions
top_venues = df['city'].value_counts().head(8).index
venue_toss_data = df[df['city'].isin(top_venues)]

plt.figure(figsize=(12, 8))
sns.countplot(data=venue_toss_data, y='city', hue='toss_decision')
plt.title('Toss Decision by Top Venues')
plt.xlabel('Number of Matches')
plt.show()

# --- Pie Charts: Toss Winner & Home Team Wins ---

# Toss winner vs match winner
toss_match_same = (df['toss_winner'] == df['winner']).sum()
toss_match_diff = (df['toss_winner'] != df['winner']).sum()

# Home team vs match winner
home_match_same = (df['Home'] == df['winner']).sum()
home_match_diff = (df['Home'] != df['winner']).sum()

# Create subplots for both pie charts
fig, axes = plt.subplots(1, 2, figsize=(14, 7))

# Pie 1: Toss Winner Wins
axes[0].pie(
    [toss_match_same, toss_match_diff],
    labels=['Toss Winner Won', 'Toss Winner Lost'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#4CAF50', '#F44336'],
    explode=(0.05, 0),
    shadow=True,
    textprops={'fontsize': 12}
)
axes[0].set_title('Toss Winner Winning the Match', fontsize=14)

# Pie 2: Home Team Wins
axes[1].pie(
    [home_match_same, home_match_diff],
    labels=['Home Team Won', 'Home Team Lost'],
    autopct='%1.1f%%',
    startangle=90,
    colors=['#2196F3', '#FF9800'],
    explode=(0.05, 0),
    shadow=True,
    textprops={'fontsize': 12}
)
axes[1].set_title('Home Team Winning the Match', fontsize=14)

plt.tight_layout()
plt.show()
