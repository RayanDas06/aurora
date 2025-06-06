# Aurora Weather Forecasting - Maldives

A sophisticated weather visualization and forecasting web application for the Maldives region using Microsoft's Aurora AI model and ERA5 reanalysis data.

![Aurora Weather App](https://img.shields.io/badge/Aurora-Weather%20Forecasting-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Features

🌤️ **Real-time Weather Visualization**
- Interactive map of the Maldives with weather data overlays
- Four key meteorological variables:
  - Two-meter Temperature (K)
  - Ten-meter Eastward Wind Speed (m/s)
  - Ten-meter Southward Wind Speed (m/s)  
  - Mean Sea-Level Pressure (Pa)

🗺️ **Interactive Interface**
- Clickable map interface for location selection
- Time series analysis for any selected point
- Current conditions display with multiple metrics
- Wind speed and direction calculations

🔮 **AI-Powered Forecasting**
- Integration with trained Aurora transformer model
- Multi-step weather prediction capability
- Visualization of forecast trends
- Real-time model inference

📊 **Rich Visualizations**
- Plotly-based interactive charts
- Folium maps with color-coded weather data
- Time series plots for historical analysis
- Forecast visualization with multiple variables

## Prerequisites

### System Requirements
- Python 3.8 or higher
- macOS, Linux, or Windows
- At least 4GB RAM (8GB recommended for model inference)
- Internet connection for initial data loading

### Data Requirements
Your `~/downloads/` directory should contain ERA5 data files:
- `*surface-level.nc` - Surface meteorological variables
- `*atmospheric.nc` - Atmospheric pressure level data (optional)
- `static.nc` - Static geographical variables (land-sea mask, topography)

## Installation

1. **Clone or navigate to your project directory:**
   ```bash
   cd "Aurora Test"
   ```

2. **Create and activate virtual environment (if not already done):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Aurora package installation:**
   ```bash
   python -c "from aurora import Aurora; print('Aurora imported successfully')"
   ```

## Quick Start

1. **Ensure ERA5 data is available:**
   ```bash
   ls ~/downloads/*surface-level.nc
   ls ~/downloads/static.nc
   ```

2. **Launch the Streamlit application:**
   ```bash
   streamlit run streamlit_weather_app.py
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Usage Guide

### Main Interface

1. **Map Interaction:**
   - Use the sidebar to select which meteorological variable to display on the map
   - Click anywhere on the map to select a location for detailed analysis
   - The map shows color-coded weather data with a legend

2. **Time Controls:**
   - Select different timestamps using the sidebar dropdown
   - Navigate through available ERA5 time steps (typically 6-hourly)

3. **Current Conditions Panel:**
   - Displays real-time weather metrics for the selected location
   - Includes temperature, wind components, pressure, wind speed, and direction
   - Updates automatically when you click on the map

4. **Time Series Analysis:**
   - Select multiple variables for time series plotting
   - Visualizes weather trends over the available time period
   - Interactive Plotly charts with zoom and pan capabilities

### Aurora AI Forecasting

1. **Generate Forecast:**
   - Click the "Generate Forecast" button in the Aurora AI section
   - The app will process your ERA5 data through the Aurora model
   - Forecast plots will display predicted weather conditions

2. **Forecast Visualization:**
   - Four-panel forecast showing all meteorological variables
   - Time series extending 6-24 hours into the future
   - Interactive charts with hover information

### Data Information

- Expand the "Data Information" section to view:
  - Data source and resolution details
  - Available time range
  - Grid point information
  - Spatial coverage

## Configuration

### Maldives Region Settings

The app is pre-configured for the Maldives region:
```python
MALDIVES_LAT_RANGE = (-0.7, 7.1)  # South to North
MALDIVES_LON_RANGE = (72.6, 73.8)  # West to East
MALDIVES_CENTER = (3.2, 73.2)     # Map center
```

To modify for other regions, edit these coordinates in `streamlit_weather_app.py`.

### Aurora Model Integration

If you have a trained Aurora model:

1. **Add model path to the configuration:**
   ```python
   from aurora_model import AuroraWeatherModel
   
   # Initialize with your trained model
   aurora_model = AuroraWeatherModel(
       model_path="path/to/your/trained_model.pth",
       device="cuda" if torch.cuda.is_available() else "cpu"
   )
   ```

2. **The app will automatically detect and use your model for real forecasting**

## File Structure

```
Aurora Test/
├── streamlit_weather_app.py     # Main Streamlit application
├── aurora_model.py              # Aurora model integration module
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── .venv/                       # Virtual environment
│   ├── ERA5.ipynb              # ERA5 data download notebook
│   └── aurora test.ipynb       # Aurora model architecture notebook
└── ~/downloads/                 # ERA5 data directory
    ├── *surface-level.nc       # Surface weather data
    ├── *atmospheric.nc         # Atmospheric data
    └── static.nc               # Static geographical data
```

## Troubleshooting

### Common Issues

1. **"No surface-level ERA5 data found"**
   - Ensure ERA5 files are in `~/downloads/` directory
   - Check file naming pattern matches `*surface-level.nc`
   - Verify files are not corrupted

2. **"Aurora model not available"**
   - Check Aurora package installation: `pip install aurora`
   - App will work in demo mode without the package

3. **Map not displaying**
   - Check internet connection (required for map tiles)
   - Ensure folium and streamlit-folium are installed correctly

4. **Slow performance**
   - Reduce the data region size
   - Use fewer time steps
   - Consider using GPU for model inference

### Performance Optimization

1. **For large datasets:**
   - Pre-process ERA5 data to smaller regional files
   - Use data caching effectively
   - Consider reducing spatial resolution

2. **For Aurora model inference:**
   - Use GPU acceleration when available
   - Implement batch processing for multiple forecasts
   - Cache model predictions

## Technical Details

### Data Processing Pipeline

1. **ERA5 Data Loading:**
   - NetCDF files loaded with xarray
   - Automatic regional filtering to Maldives bounds
   - Variable name mapping (ERA5 → Aurora conventions)

2. **Aurora Batch Creation:**
   - Surface variables: 2t, 10u, 10v, msl
   - Static variables: z, lsm, slt
   - Atmospheric variables: z, u, v, t, q (at pressure levels)

3. **Model Inference:**
   - PyTorch-based Aurora transformer model
   - Rollout prediction for multi-step forecasting
   - GPU acceleration support

### Visualization Components

- **Folium:** Interactive maps with weather data overlays
- **Plotly:** Time series and forecast visualization
- **Streamlit:** Web application framework and UI components

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and research purposes. Please respect the licensing terms of:
- ERA5 data (Copernicus Climate Change Service)
- Aurora model (Microsoft Research)
- Associated Python packages

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review your ERA5 data setup
3. Verify Aurora package installation
4. Check Python environment and dependencies

## Acknowledgments

- **Microsoft Research** for the Aurora weather forecasting model
- **ECMWF** for ERA5 reanalysis data
- **Copernicus Climate Change Service** for data access
- **Streamlit** team for the excellent web app framework 