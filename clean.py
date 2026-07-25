import pandas as pd

# Load dataset
df = pd.read_csv('data/startup_funding.csv')

print("Original shape:", df.shape)

# ---------------- CLEANING ----------------

# Remove duplicate rows
df.drop_duplicates(inplace=True)

# Remove completely empty rows
df.dropna(how='all', inplace=True)

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Fill missing values
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].fillna("Unknown")

for col in df.select_dtypes(include="number").columns:
    df[col] = df[col].fillna(0)

# Convert investment amount to numeric
df["InvestmentAmount_USD"] = pd.to_numeric(
    df["InvestmentAmount_USD"],
    errors="coerce"
)

# Remove invalid investment rows
df = df[df["InvestmentAmount_USD"] > 0]


# ---------------- CHECK ----------------

print("\nAfter cleaning:")
print(df.info())

print("\nNull values:")
print(df.isnull().sum())

print("\nDuplicates:")
print(df.duplicated().sum())

print("\nStatistics:")
print(df.describe())


# ---------------- SAVE ----------------

df.to_csv(
    "data/cleaned_startup_funding.csv",
    index=False
)

print("\nCleaned dataset successfully saved")
print("Final shape:", df.shape)