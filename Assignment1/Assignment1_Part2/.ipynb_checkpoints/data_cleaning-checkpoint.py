import pandas as pd

# Load city distances file
file_path = "city_distances.csv"
df = pd.read_csv(file_path, header=None)

# Check if first row and column contain indices (non-numeric values)
if not pd.to_numeric(df.iloc[0, 1:], errors='coerce').notna().all():
    df = df.iloc[1:, 1:]  # Remove first row and column

# Convert to numeric
cleaned_matrix = df.apply(pd.to_numeric)

# Save cleaned data
cleaned_matrix.to_csv("city_distances_cleaned.csv", index=False, header=False)

print("Data cleaning completed. Saved as city_distances_cleaned.csv")
