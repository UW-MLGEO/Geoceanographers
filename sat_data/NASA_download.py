import earthaccess
from datetime import datetime

earthaccess.login()

results = []

# --------------------------------------------------
# Load buoy locations
# --------------------------------------------------
buoy_locations = {}

with open("buoy_locations.txt") as f:
    for line in f:
        if not line.strip():
            continue

        site, lat, lon = line.strip().split(",")

        buoy_locations[site] = {
            "lat": float(lat),
            "lon": float(lon)
        }

# --------------------------------------------------
# Define temporal bounds (EDIT AS NEEDED)
# --------------------------------------------------
# Example: one common analysis window
temporal_bounds = (
    "2010-01-01",
    "2020-12-31"
)



# Spatial half-width in degrees
delta = 0.1

# --------------------------------------------------
# Loop over buoys and issue bounded searches
# --------------------------------------------------
for site, coords in buoy_locations.items():

    lat = coords["lat"]
    lon = coords["lon"]

    bounding_box = (
        lon - delta,
        lat - delta,
        lon + delta,
        lat + delta
    )

    # ---- MODIS Aqua Chlorophyll ----
    chl_results = earthaccess.search_data(
        short_name="MODISA_L3b_CHL",
        bounding_box=bounding_box,
        temporal=temporal_bounds,
        downloadable=True
    )

    results.append({
        "site": site,
        "dataset": "MODISA_L3b_CHL",
        "granules": chl_results
    })

    ## ---- GHRSST MUR SST ----
    #sst_results = earthaccess.search_data(
    #    short_name="MUR-JPL-L4-GLOB-v4.1",
    #    bounding_box=bounding_box,
    #    temporal=temporal_bounds,
    #    downloadable=True
    #)

    #results.append({
    #    "site": site,
    #    "dataset": "MUR-JPL-L4-GLOB-v4.1",
    #    "granules": sst_results
    #})

output_file = "search_results.txt"

with open(output_file, "w") as f:
    for entry in results:
        site = entry["site"]
        dataset = entry["dataset"]
        granules = entry["granules"]

        f.write(f"Site: {site}\n")
        f.write(f"Dataset: {dataset}\n")
        f.write(f"Granules found: {len(granules)}\n")

        for g in granules:
            # granule id / name
            granule_id = getattr(g, "id", "UNKNOWN")
            f.write(f"  - {granule_id}\n")

        f.write("\n" + "-" * 50 + "\n\n")

print(f"Wrote search results to {output_file}")

