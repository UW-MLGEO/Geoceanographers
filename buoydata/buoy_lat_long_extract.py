import csv
import os

DATA_DIR = "./buoy_raw_csv"
OUTPUT_FILE = "buoy_locations.txt"

buoys = {}

def is_float(x):
    try:
        float(x)
        return True
    except:
        return False

for fname in os.listdir(DATA_DIR):
    if not fname.lower().endswith(".csv"):
        continue
    if "qf" in fname.lower():
        continue

    site = fname.split("_")[0].upper()
    if site in buoys:
        continue

    path = os.path.join(DATA_DIR, fname)

    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if len(row) < 3:
                continue

            lat_raw = row[1].strip()
            lon_raw = row[2].strip()

            if is_float(lat_raw) and is_float(lon_raw):
                buoys[site] = (float(lat_raw), float(lon_raw))
                break

# write output
with open(OUTPUT_FILE, "w") as f:
    for site, (lat, lon) in sorted(buoys.items()):
        f.write(f"{site},{lat},{lon}\n")

print(f"Wrote {len(buoys)} buoy locations to {OUTPUT_FILE}")

