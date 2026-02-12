#!/usr/bin/env python3
"""
Create MP4 animation from MODIS Level 4 Phyto-Carbon data (2010-2020)
"""
#Claude sonnet 4.5, with some debugging done by me 


import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LogNorm
import numpy as np
import glob
import os
from datetime import datetime
import pandas as pd
import re 

# ============================================================================
# CONFIGURATION
# ============================================================================

# Directory containing your .nc files (change if needed)
data_dir = '.'  # Current directory

# Output video filename
output_video = 'modis_carbon_phyto_2010_2020.mp4'

# Video settings
fps = 5  # Frames per second
dpi = 150  # Resolution

# Phytoplankton carbon  scale (mg/m^3)
vmin = 0 
vmax = 120.0 

# ============================================================================
# LOAD DATA
# ============================================================================

print("=" * 60)
print("MODIS Carbon Animation Generator")
print("=" * 60)

# Find all .nc files
print("\n1. Finding NetCDF files...")
nc_files = sorted(glob.glob(os.path.join(data_dir, '*.nc')))

print(f"   Found {len(nc_files)} files")

if len(nc_files) == 0:
    print("ERROR: No NetCDF files found!")
    print(f"Searched in: {os.path.abspath(data_dir)}")
    exit(1)

# Show first few filenames to verify
print("\n   First few files:")
for f in nc_files[:3]:
    print(f"   - {os.path.basename(f)}")

# ============================================================================
# EXTRACT DATES FROM FILENAMES AND LOAD DATA
# ============================================================================

print("\n2. Loading data files...")

# Function to extract date from MODIS filename
def extract_date_from_filename(filename):
    """Extract start date from AQUA_MODIS.20100101_20100131.* format"""
    basename = os.path.basename(filename)
    
    # Pattern: find YYYYMMDD_YYYYMMDD
    match = re.search(r'(\d{8})_(\d{8})', basename)
    
    if match:
        start_date = match.group(1)  # First date
        return pd.Timestamp(f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}")
    
    print(f"   WARNING: Could not parse date from {basename}")
    return None

# Load each file and add time coordinate
datasets = []
dates = []

for i, file in enumerate(nc_files):
    # Extract date from filename
    date = extract_date_from_filename(file)
    
    if date is None:
        print(f"   Warning: Could not extract date from {os.path.basename(file)}, skipping...")
        continue
    
    # Load dataset
    ds = xr.open_dataset(file)
    
    # Add time coordinate
    ds = ds.expand_dims(time=[date])
    
    datasets.append(ds)
    dates.append(date)
    
    if (i + 1) % 20 == 0:
        print(f"   Loaded {i + 1}/{len(nc_files)} files...")

print(f"   Successfully loaded {len(datasets)} files")

# Concatenate all datasets along time dimension
print("\n3. Concatenating datasets...")
ds = xr.concat(datasets, dim='time')

# Sort by time
ds = ds.sortby('time')

# Identify chlorophyll variable
print("\n4. Available variables in dataset:")
for var in ds.data_vars:
    print(f"   - {var}")

# Try common chlorophyll variable names
chl_var = 'carbon_phyto' 

print(f"\n   Using variable: '{chl_var}'")

# Extract chlorophyll data
chl = ds[chl_var]

print(f"\n5. Data summary:")
print(f"   Shape: {chl.shape}")
print(f"   Time steps: {len(chl.time)}")
print(f"   Date range: {str(chl.time.min().values)[:10]} to {str(chl.time.max().values)[:10]}")
if 'lat' in chl.dims and 'lon' in chl.dims:
    print(f"   Spatial extent: {float(chl.lat.min()):.2f}°N to {float(chl.lat.max()):.2f}°N")
    print(f"                   {float(chl.lon.min()):.2f}°E to {float(chl.lon.max()):.2f}°E")

# ============================================================================
# CREATE ANIMATION
# ============================================================================

print("\n6. Creating animation...")
print(f"   This will generate {len(chl.time)} frames...")

# Set up figure
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('white')

# Create initial plot
first_frame = chl.isel(time=0).values

# Get lat/lon for extent
if 'lat' in chl.coords and 'lon' in chl.coords:
    lon = chl.lon.values
    lat = chl.lat.values
    extent = [lon.min(), lon.max(), lat.min(), lat.max()]
else:
    extent = None

im = ax.imshow(
    first_frame,
    origin='upper',
    cmap='viridis',
    vmin=vmin, vmax=vmax,
    aspect='auto',
    interpolation='nearest',
    extent=extent
)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, label='Phytoplankon Carbon Concentration (mg/m³)', pad=0.02)

# Labels
ax.set_xlabel('Longitude (°E)', fontsize=12)
ax.set_ylabel('Latitude (°N)', fontsize=12)
ax.set_title('MODIS Aqua Phytonplankton Carbon Concentration', fontsize=14, weight='bold', pad=20)

# Date text overlay
time_text = ax.text(
    0.02, 0.98,
    '',
    transform=ax.transAxes,
    fontsize=16,
    color='white',
    weight='bold',
    verticalalignment='top',
    bbox=dict(boxstyle='round', facecolor='black', alpha=0.7, pad=0.5)
)

# Frame counter
frame_text = ax.text(
    0.98, 0.98,
    '',
    transform=ax.transAxes,
    fontsize=12,
    color='white',
    weight='bold',
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='black', alpha=0.7, pad=0.5)
)

# Animation update function
def update(frame):
    # Update image data
    data = chl.isel(time=frame).values
    im.set_array(data)
    
    # Update date text
    date_str = str(chl.time.isel(time=frame).values)[:10]
    time_text.set_text(f'{date_str}')
    
    # Update frame counter
    frame_text.set_text(f'Frame {frame + 1}/{len(chl.time)}')
    
    # Progress indicator
    if frame % 10 == 0:
        print(f"   Processing frame {frame + 1}/{len(chl.time)} ({100*frame/len(chl.time):.1f}%)")
    
    return [im, time_text, frame_text]

# Create animation
n_frames = len(chl.time)
anim = animation.FuncAnimation(
    fig,
    update,
    frames=n_frames,
    interval=1000/fps,  # milliseconds per frame
    blit=True,
    repeat=True
)

# ============================================================================
# SAVE VIDEO
# ============================================================================

print(f"\n7. Saving video to '{output_video}'...")
print("   This may take several minutes depending on data size...")

# Set up writer
writer = animation.FFMpegWriter(
    fps=fps,
    metadata=dict(
        artist='Python/xarray',
        title='MODIS Phytoplankton Carbon 2010-2020',
        comment='Created from MODIS Aqua Level 4 data'
    ),
    bitrate=2000,
    codec='libx264'
)

# Save animation
try:
    anim.save(output_video, writer=writer, dpi=dpi)
    plt.close()
    
    # Get file size
    file_size = os.path.getsize(output_video) / (1024 * 1024)  # MB
    duration = n_frames / fps
    
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print(f"Video saved: {output_video}")
    print(f"File size: {file_size:.1f} MB")
    print(f"Duration: {duration:.1f} seconds ({n_frames} frames at {fps} fps)")
    print(f"Resolution: {int(14*dpi)} x {int(8*dpi)} pixels")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERROR: Failed to save video!")
    print(f"Error message: {str(e)}")
    print("\nMake sure ffmpeg is installed:")
    print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("  Mac: brew install ffmpeg")
    print("  Conda: conda install ffmpeg")
