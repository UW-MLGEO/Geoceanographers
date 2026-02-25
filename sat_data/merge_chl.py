import pandas as pd
import os

# -------------------------------------------------------------
# FILES
# -------------------------------------------------------------
COMBINED_FILE = "combined_satellite_buoy.csv"
CHL_FILE = "buoy_chl_attached.csv"
OUTPUT_FILE = "combined_satellite_buoy_with_chl.csv"

# -------------------------------------------------------------
# HARD FAILS
# -------------------------------------------------------------
for f in [COMBINED_FILE, CHL_FILE]:
    if not os.path.isfile(f):
        raise FileNotFoundError(f"Required file not found: {f}")

# -------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------
combined = pd.read_csv(COMBINED_FILE)
chl = pd.read_csv(CHL_FILE)

# -------------------------------------------------------------
# VALIDATE REQUIRED COLUMNS (EXACT)
# -------------------------------------------------------------
required_combined = {"location", "date"}
required_chl = {"buoy", "date", "chlor_a"}

missing_combined = required_combined - set(combined.columns)
missing_chl = required_chl - set(chl.columns)

if missing_combined:
    raise ValueError(f"combined_satellite_buoy.csv missing columns: {missing_combined}")

if missing_chl:
    raise ValueError(f"buoy_chl_attached.csv missing columns: {missing_chl}")

# -------------------------------------------------------------
# NORMALIZE DATE FORMAT (SAFE, NO SEMANTIC CHANGE)
# -------------------------------------------------------------
combined["date"] = pd.to_datetime(combined["date"]).dt.date.astype(str)
chl["date"] = pd.to_datetime(chl["date"]).dt.date.astype(str)

# -------------------------------------------------------------
# ALIGN BUOY COLUMN NAME
# -------------------------------------------------------------
combined = combined.rename(columns={"location": "buoy"})

# -------------------------------------------------------------
# MERGE (VALIDATED)
# -------------------------------------------------------------
merged = combined.merge(
    chl[["buoy", "date", "chlor_a"]],
    on=["buoy", "date"],
    how="left",
    validate="many_to_one"
)

# -------------------------------------------------------------
# WRITE OUTPUT
# -------------------------------------------------------------
merged.to_csv(OUTPUT_FILE, index=False)

print("✔ CHL successfully merged into combined dataset")
print(f"✔ Output written to: {OUTPUT_FILE}")

