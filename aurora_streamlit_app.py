import streamlit as st
import torch
import xarray as xr
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

from aurora.batch import Batch, Metadata
from aurora.model.aurora import Aurora
from aurora.rollout import rollout

# Page configuration
st.set_page_config(
    page_title="Aurora Weather Predictions - Maldives",
    layout="wide"
)

# Maldives coordinates for region focus
MALDIVES_LAT_RANGE = (-1.0, 8.0)  # Latitude range for Maldives (with some buffer)
MALDIVES_LON_RANGE = (72.0, 74.0)  # Longitude range for Maldives (with some buffer)

@st.cache_data
def load_era5_data():
    """Load ERA5 datasets"""
    download_path = Path("~/downloads").expanduser()
    
    static_vars_ds = xr.open_dataset(download_path / "static.nc", engine="netcdf4")
    surf_vars_ds = xr.open_dataset(download_path / "2025-05-05-surface-level.nc", engine="netcdf4")
    atmos_vars_ds = xr.open_dataset(download_path / "2025-05-05-atmospheric.nc", engine="netcdf4")
    
    return static_vars_ds, surf_vars_ds, atmos_vars_ds

@st.cache_resource
def load_aurora_model():
    """Load and initialize Aurora model"""
    st.info("**Downloading/Loading Aurora Model**")
    st.info("Downloading ~1-2GB model checkpoint and initializing weights")
    
    start_time = time.time()
    model = Aurora(use_lora=False)
    
    checkpoint_time = time.time()
    st.info(f"Model initialization took {checkpoint_time - start_time:.1f} seconds")
    st.info("**Loading checkpoint weights**")
    
    model.load_checkpoint("microsoft/aurora", "aurora-0.25-pretrained.ckpt")
    
    load_time = time.time()
    st.info(f"Checkpoint loading took {load_time - checkpoint_time:.1f} seconds")
    
    model.eval()
    model = model.to("cpu")
    
    total_time = time.time() - start_time
    st.success(f"**Model loaded successfully!** Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    return model

@st.cache_data
def create_batch_data(_static_vars_ds, _surf_vars_ds, _atmos_vars_ds):
    """Create batch data for Aurora model"""
    batch = Batch(
        surf_vars={
            # Using time points 2:4 (12:00 and 18:00 on 5/5/2025)
            "2t": torch.from_numpy(_surf_vars_ds["t2m"].values[2:4][None]),
            "10u": torch.from_numpy(_surf_vars_ds["u10"].values[2:4][None]),
            "10v": torch.from_numpy(_surf_vars_ds["v10"].values[2:4][None]),
            "msl": torch.from_numpy(_surf_vars_ds["msl"].values[2:4][None]),
        },
        static_vars={
            "z": torch.from_numpy(_static_vars_ds["z"].values[0]),
            "lsm": torch.from_numpy(_static_vars_ds["lsm"].values[0]),
        },
        atmos_vars={
            "t": torch.from_numpy(_atmos_vars_ds["t"].values[2:4][None]),
            "u": torch.from_numpy(_atmos_vars_ds["u"].values[2:4][None]),
            "v": torch.from_numpy(_atmos_vars_ds["v"].values[2:4][None]),
            "q": torch.from_numpy(_atmos_vars_ds["q"].values[2:4][None]),
            "z": torch.from_numpy(_atmos_vars_ds["z"].values[2:4][None]),
        },
        metadata=Metadata(
            lat=torch.from_numpy(_surf_vars_ds.latitude.values),
            lon=torch.from_numpy(_surf_vars_ds.longitude.values),
            time=(_surf_vars_ds.valid_time.values.astype("datetime64[s]").tolist()[3],),
            atmos_levels=tuple(int(level) for level in _atmos_vars_ds.pressure_level.values),
        ),
    )
    return batch

@st.cache_data
def run_aurora_predictions(_model, _batch):
    """Run Aurora model predictions"""
    st.info("**Running 6-step predictions**")
    st.info("Computing weather forecasts for 6 timesteps using Aurora model")
    
    start_time = time.time()
    with torch.inference_mode():
        preds = [pred for pred in rollout(_model, _batch, steps=6)]
    
    prediction_time = time.time() - start_time
    st.success(f"**Predictions completed.** Time: {prediction_time:.1f} seconds ({prediction_time/60:.1f} minutes)")
    
    return preds

def crop_to_maldives(data, lats, lons):
    """Crop data to Maldives region"""
    lat_mask = (lats >= MALDIVES_LAT_RANGE[0]) & (lats <= MALDIVES_LAT_RANGE[1])
    lon_mask = (lons >= MALDIVES_LON_RANGE[0]) & (lons <= MALDIVES_LON_RANGE[1])
    
    # Find indices
    lat_indices = np.where(lat_mask)[0]
    lon_indices = np.where(lon_mask)[0]
    
    if len(lat_indices) == 0 or len(lon_indices) == 0:
        return None, None, None
    
    lat_start, lat_end = lat_indices[0], lat_indices[-1] + 1
    lon_start, lon_end = lon_indices[0], lon_indices[-1] + 1
    
    cropped_data = data[lat_start:lat_end, lon_start:lon_end]
    cropped_lats = lats[lat_start:lat_end]
    cropped_lons = lons[lon_start:lon_end]
    
    return cropped_data, cropped_lats, cropped_lons

def create_interactive_map(data, lats, lons, title, unit, colorscale='RdYlBu_r'):
    """Create interactive geographic map with fixed color scaling"""
    # Create meshgrid for coordinates
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # Calculate fixed color scale range based on data
    vmin, vmax = np.nanmin(data), np.nanmax(data)
    
    fig = go.Figure(data=go.Scattermapbox(
        lat=lat_grid.flatten(),
        lon=lon_grid.flatten(),
        mode='markers',
        marker=dict(
            size=8,
            color=data.flatten(),
            colorscale=colorscale,
            showscale=True,
            cmin=vmin,  # Fixed minimum - colors won't change with zoom
            cmax=vmax,  # Fixed maximum - colors won't change with zoom
            colorbar=dict(title=unit),
            opacity=0.8
        ),
        text=[f'{val:.2f}' for val in data.flatten()],
        hovertemplate='<b>Latitude: %{lat:.2f}°</b><br>' +
                     '<b>Longitude: %{lon:.2f}°</b><br>' +
                     f'<b>{title}: %{{text}} {unit}</b><extra></extra>'
    ))
    
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=np.mean(lats), lon=np.mean(lons)),
            zoom=8
        ),
        title=title,
        height=450,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    
    return fig

def main():
    st.title("Aurora Weather Predictions - Maldives")
    st.markdown("### Visualize weather predictions for May 6, 2025")
    
    # Add loading time warning
    st.warning("Website may take a while to load due to large model downloads and computations.")
    
    try:
        # Load data and model
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("Loading ERA5 data")
        progress_bar.progress(5)
        static_vars_ds, surf_vars_ds, atmos_vars_ds = load_era5_data()
        
        status_text.text("Loading Aurora model")
        progress_bar.progress(15)
        model = load_aurora_model()
        
        status_text.text("Preparing data batch")
        progress_bar.progress(70)
        batch = create_batch_data(static_vars_ds, surf_vars_ds, atmos_vars_ds)
        
        status_text.text("Running Aurora predictions")
        progress_bar.progress(75)
        predictions = run_aurora_predictions(model, batch)
        
        progress_bar.progress(100)
        status_text.text("All predictions computed.")
        
        # Clear progress indicators after a moment
        time.sleep(2)
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"Error loading model or data: {str(e)}")
        st.info("Please make sure:")
        st.info("1. ERA5 data files exist in ~/downloads/")
        st.info("2. Aurora model checkpoint is available")
        st.info("3. All required packages are installed")
        st.info("4. You have sufficient disk space (model needs ~2GB)")
        st.info("5. Stable internet connection for downloading model")
        return
    
    # Time selection
    st.sidebar.header("Time Selection")
    time_options = {
        "00:00": 2,  # Step 3 (index 2)
        "06:00": 3,  # Step 4 (index 3)  
        "12:00": 4,  # Step 5 (index 4)
        "18:00": 5   # Step 6 (index 5)
    }
    
    selected_time = st.sidebar.selectbox(
        "Select time on May 6, 2025:",
        options=list(time_options.keys()),
        index=0
    )
    
    pred_index = time_options[selected_time]
    prediction = predictions[pred_index]
    
    st.subheader(f"Weather Predictions for May 6, 2025 at {selected_time}")
    
    # Get coordinate arrays
    lats = batch.metadata.lat.numpy()
    lons = batch.metadata.lon.numpy()
    
    # Variable definitions
    variables = {
        "2m Temperature": {
            "data": prediction.surf_vars["2t"][0, 0].numpy(),
            "unit": "K",
            "colorscale": "RdYlBu_r"
        },
        "10m Eastward Wind": {
            "data": prediction.surf_vars["10u"][0, 0].numpy(),
            "unit": "m/s",
            "colorscale": "RdBu_r"
        },
        "10m Southward Wind": {
            "data": prediction.surf_vars["10v"][0, 0].numpy(),
            "unit": "m/s", 
            "colorscale": "RdBu_r"
        },
        "Mean Sea Level Pressure": {
            "data": prediction.surf_vars["msl"][0, 0].numpy(),
            "unit": "Pa",
            "colorscale": "viridis"
        }
    }
    
    # Create 2x2 grid for the four variables
    col1, col2 = st.columns(2)
    
    var_names = list(variables.keys())
    
    with col1:
        for i in [0, 2]:  # First and third variables
            var_name = var_names[i]
            var_info = variables[var_name]
            
            # Crop to Maldives region
            cropped_data, cropped_lats, cropped_lons = crop_to_maldives(
                var_info["data"], lats, lons
            )
            
            if cropped_data is not None:
                fig = create_interactive_map(
                    cropped_data, cropped_lats, cropped_lons,
                    var_name, var_info["unit"], var_info["colorscale"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No data available for {var_name} in Maldives region")
    
    with col2:
        for i in [1, 3]:  # Second and fourth variables
            var_name = var_names[i]
            var_info = variables[var_name]
            
            # Crop to Maldives region
            cropped_data, cropped_lats, cropped_lons = crop_to_maldives(
                var_info["data"], lats, lons
            )
            
            if cropped_data is not None:
                fig = create_interactive_map(
                    cropped_data, cropped_lats, cropped_lons,
                    var_name, var_info["unit"], var_info["colorscale"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning(f"No data available for {var_name} in Maldives region")
    
    st.info("Hover over any point on the maps to see exact values")
    
    
    
    

if __name__ == "__main__":
    main() 