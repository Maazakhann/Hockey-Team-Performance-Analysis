import pandas as pd
import numpy as np
from pathlib import Path

SEED = 12  

# File paths
raw_path = Path("data/hockey_teams_raw.csv")
output_path = Path("data/hockey_teams_missing.csv")

df = pd.read_csv(raw_path)
df_missing = df.copy()
columns = ["GF", "GA"]
rng = np.random.default_rng(SEED)

total_cells = len(df_missing) * len(columns)
missing_count = round(total_cells * 0.05)

positions = []

for row in range(len(df_missing)):
    for col in columns:
        if pd.notna(df_missing.loc[row, col]):  # introduce missing values to cells that originally contains data
            positions.append((row, col))
# Randomly select cells
selected = rng.choice(
    len(positions),
    size=missing_count,
    replace=False    
)

# Introduce missing values
for index in selected:
    row, col = positions[index]
    df_missing.loc[row, col] = np.nan


df_missing["Team_Status"] = (
    df_missing["Win %"] >= 0.500
).astype(int)

# Verify protected columns remain unchanged
assert df_missing["Wins"].equals(df["Wins"])
assert df_missing["Win %"].equals(df["Win %"])

# Save working dataset
output_path.parent.mkdir(parents=True, exist_ok=True)
df_missing.to_csv(output_path, index=False)


print("Original shape:", df.shape)
print("Modified shape:", df_missing.shape)

print("\nOriginal missing values:")
print(df.isnull().sum())

print("\nModified missing values:")
print(df_missing.isnull().sum())

print("\nSynthetic missing values:", missing_count)
print("Missing percentage:",
      round(missing_count / total_cells * 100, 2), "%")

print("\nWins unchanged:",
      df["Wins"].equals(df_missing["Wins"]))

print("Win % unchanged:",
      df["Win %"].equals(df_missing["Win %"]))