
from pathlib import Path
import pandas as pd
import numpy as np

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RAW_FILE = DATA_DIR / "raw_dataset.csv"

# 1. Load the raw dataset
df = pd.read_csv(RAW_FILE)

print("\n===== DATASET OVERVIEW =====")
print("Rows and columns:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== DATASET INFORMATION =====")
df.info()

# 2. Check missing values
missing_report = pd.DataFrame({
    "Column": df.columns,
    "Missing_Count": df.isna().sum().values,
    "Missing_Percentage": (
        df.isna().mean().values * 100
    ).round(2)
})

missing_report.to_csv(
    OUTPUT_DIR / "missing_values_report.csv",
    index=False
)

print("\n===== MISSING VALUES =====")
print(missing_report.to_string(index=False))

# 3. Check duplicate rows
print("\n===== DUPLICATE CHECK =====")
print("Duplicate rows:", df.duplicated().sum())

# 4. Summary statistics
print("\n===== SUMMARY STATISTICS =====")
print(df.describe(include="all").T)

# 5. Unique values in each column
print("\n===== UNIQUE VALUE COUNTS =====")
for column in df.columns:
    print(f"{column}: {df[column].nunique(dropna=True)}")

print("\nInspection completed.")
print("Missing-value report saved in the output folder.")



from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_DIR / "raw_dataset.csv")

# Preserve the original row count for validation
original_rows = len(df)

# 1. Standardize column names
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^\w]", "", regex=True)
)

# 2. Convert empty strings and whitespace-only cells to missing
df = df.replace(r"^\s*$", np.nan, regex=True)

# 3. Trim whitespace in text columns
text_columns = df.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    df[column] = df[column].map(
        lambda value: value.strip()
        if isinstance(value, str) else value
    )

# 4. Report exact duplicates before removing them
duplicate_count = int(df.duplicated().sum())
print("Exact duplicate rows found:", duplicate_count)

# Remove exact duplicate rows after review
df = df.drop_duplicates().copy()

# 5. Save the cleaned dataset
cleaned_file = OUTPUT_DIR / "cleaned_dataset.csv"
df.to_csv(cleaned_file, index=False)

# 6. Validate the cleaned result
print("\n===== VALIDATION =====")
print("Original rows:", original_rows)
print("Rows after cleaning:", len(df))
print("Rows removed:", original_rows - len(df))
print("Remaining exact duplicates:", df.duplicated().sum())
print("\nMissing values by column:")
print(df.isna().sum())
print("\nFinal data types:")
print(df.dtypes)

print("\nCleaned dataset saved to:", cleaned_file)


#dir

import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw_dataset.csv")

dictionary = pd.DataFrame({
    "Column_Name": df.columns,
    "Data_Type": df.dtypes.astype(str).values,
    "Description": ["To be documented"] * len(df.columns),
    "Example_Value": [
        df[col].dropna().iloc[0]
        if not df[col].dropna().empty else None
        for col in df.columns
    ],
    "Missing_Values": df.isna().sum().values,
    "Unique_Values": df.nunique(dropna=True).values
})

Path("output").mkdir(exist_ok=True)

dictionary.to_csv(
    "output/data_dictionary.csv",
    index=False
)

print("Data dictionary created successfully!")
print(dictionary)

