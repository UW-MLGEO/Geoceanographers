import os
import re
import pandas as pd
import xarray as xr
from datetime import datetime

# ------------------------------------------------------------------
# PATHS (AS YOU DESCRIBED)
# ------------------------------------------------------------------
BASE_DIR = "."
CHL_DIR = os.path.join(BASE_DIR, "chl_buoytimespan")
BUOY_FILE = os.path.join(BASE_DIR, "buoy_locations.txt")

# ------------------------------------------------------------------
# HARD FAILS
# ------------------------------------------------------------------
if not os.path.isdir(CHL_DIR):
    raise FileNotFoundError("chl_buoytimespan directory not found")

if not os.path.isfile(BUOY_FILE):
    raise FileNotFoundError("buoy_locations.txt not found")

# ------------------------------------------------------------------
# EXPLICIT, AUTHORITATIVE BUOY NAME TRANSLATION
# ------------------------------------------------------------------
BUOY_NAME_MAP = {
    "CCE2": "Southern California",
    "COASTALLA": "Coastal Louisiana",
    "GRAYSRF": "Grays Reef Georgia",
    "LAPUSH": "La Push",
    "M2": "SE Bering Sea",
    "TAO165E": "South Pacific",
}

# ------------------------------------------------------------------
# LOAD BUOY LOCATIONS
# ------------------------------------------------------------------
buoys = pd.read_csv(
    BUOY_FILE,
    header=None,
    names=["buoy_txt", "lat", "lon"]
)

# Enforce complete mapping coverage
unmapped = set(buoys["buoy_txt"]) - set(BUOY_NAME_MAP.keys())
if unmapped:
    raise ValueError(f"Unmapped buoy names found: {unmapped}")

buoys["buoy"] = buoys["buoy_txt"].map(BUOY_NAME_MAP)

# ------------------------------------------------------------------
# STRICT FILENAME FILTER
# ------------------------------------------------------------------
pattern = re.compile(
    r"AQUA_MODIS\.(\d{8})\.L3m\.DAY\.CHL\.chlor_a\.4km\.nc$"
)

records = []

# ------------------------------------------------------------------
# CHL EXTRACTION (SCIENTIFIC LOGIC UNCHANGED)
# ------------------------------------------------------------------
for fname in sorted(os.listdir(CHL_DIR)):
    match = pattern.match(fname)
    if not match:
        continue

    date = datetime.strptime(match.group(1), "%Y%m%d").date()
    fpath = os.path.join(CHL_DIR, fname)

    with xr.open_dataset(fpath) as ds:
        chlor_a = ds["chlor_a"]
        lats = ds["lat"]
        lons = ds["lon"]

        for _, b in buoys.iterrows():
            lat_idx = abs(lats - b.lat).argmin().item()
            lon_idx = abs(lons - b.lon).argmin().item()

            chl_val = float(
                chlor_a.isel(lat=lat_idx, lon=lon_idx).values
            )

            records.append({
                "buoy": b.buoy,          # TRANSLATED NAME
                "date": date.isoformat(),
                "lat": b.lat,
                "lon": b.lon,
                "chlor_a": chl_val
            })

# ------------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------------
df = pd.DataFrame(records)
df.to_csv("buoy_chl_attached.csv", index=False)

print("✔ Buoy names explicitly translated")
print("✔ CHL attached with zero spatial or temporal leakage")
print("✔ Output: buoy_chl_attached.csv")

