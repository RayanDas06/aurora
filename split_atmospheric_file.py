import xarray as xr
import numpy as np
from pathlib import Path

def split_atmospheric_file():
    """Split the large atmospheric file into 5 smaller files by pressure levels"""
    
    data_path = Path("data")
    input_file = data_path / "2025-05-05-atmospheric.nc"
    
    print(f"Loading atmospheric data from {input_file}...")
    atmos_ds = xr.open_dataset(input_file, engine="netcdf4")
    
    # Get all pressure levels
    pressure_levels = atmos_ds.pressure_level.values
    print(f"Found {len(pressure_levels)} pressure levels: {pressure_levels}")
    
    # Split into 5 groups (approximately 2-3 levels per file)
    n_files = 5
    levels_per_file = len(pressure_levels) // n_files
    remainder = len(pressure_levels) % n_files
    
    level_groups = []
    start_idx = 0
    
    for i in range(n_files):
        # Add one extra level to first 'remainder' files to distribute evenly
        end_idx = start_idx + levels_per_file + (1 if i < remainder else 0)
        level_groups.append(pressure_levels[start_idx:end_idx])
        start_idx = end_idx
    
    print(f"\nSplitting into {n_files} files:")
    for i, levels in enumerate(level_groups):
        print(f"  Part {i+1}: {levels} ({len(levels)} levels)")
    
    # Create split files
    for i, levels in enumerate(level_groups):
        output_file = data_path / f"2025-05-05-atmospheric-part{i+1}.nc"
        
        print(f"\nCreating {output_file}...")
        
        # Select data for these pressure levels
        subset = atmos_ds.sel(pressure_level=levels)
        
        # Save to new file
        subset.to_netcdf(output_file, engine="netcdf4")
        
        # Check file size
        file_size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"  File size: {file_size_mb:.1f} MB")
    
    print(f"Successfully split atmospheric data into {n_files} files!")
    
    # Automatically delete the original large file
    print(f"\nDeleting original large file: {input_file}")
    input_file.unlink()
    print("Original file deleted successfully!")

if __name__ == "__main__":
    split_atmospheric_file() 