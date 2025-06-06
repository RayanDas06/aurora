# Aurora Weather Predictions - Maldives

A sophisticated weather forecasting web application for the Maldives region using Microsoft's Aurora AI model and ERA5 reanalysis data. The app provides interactive weather visualizations and 6-step weather predictions for May 6, 2025.

![Aurora Weather App](https://img.shields.io/badge/Aurora-Weather%20Forecasting-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## Features

 **Interactive Weather Visualization**
- Interactive maps of the Maldives with real-time weather overlays
- Four key meteorological variables:
  - 2m Temperature (K)
  - 10m Eastward Wind Speed (m/s)
  - 10m Southward Wind Speed (m/s)  
  - Mean Sea Level Pressure (Pa)

**AI-Powered Forecasting**
- Microsoft Aurora transformer model for weather prediction
- 6-step rollout forecasting (24 hours ahead in 6-hour steps)
- Covers May 6, 2025: 00:00, 06:00, 12:00, 18:00

**Interactive Interface**
- Plotly-based interactive maps with hover details
- Time selection dropdown for different forecast times
- Zoom/pan capabilities with Maldives-focused view
- Fixed color scaling for consistent visualization

**Optimized for Deployment**
- Smart data file splitting for GitHub compatibility
- All files under 100MB for Streamlit Community Cloud deployment
- Automatic data loading and caching

## Quick Start

### Prerequisites
- Python 3.8 or higher
- CDS API credentials (for data download)
- At least 4GB RAM (8GB recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "Aurora Test"
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up CDS API credentials:**
   - Register at [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
   - Create `~/.cdsapirc` file with your credentials:
     ```
     url: https://cds.climate.copernicus.eu/api/v2
     key: <your-uid>:<your-api-key>
     ```

### Running the Application

1. **Download ERA5 data (first time only):**
   ```bash
   python download_era5_data.py
   ```

2. **Split atmospheric data for GitHub compatibility:**
   ```bash
   python split_atmospheric_file.py
   ```

3. **Launch the Streamlit app:**
   ```bash
   streamlit run aurora_streamlit_app.py
   ```

4. **Open your browser:**
   Visit `http://localhost:8501`

## Project Structure

```
Aurora Test/
├── aurora_streamlit_app.py         # Main Streamlit application
├── download_era5_data.py           # ERA5 data download script
├── split_atmospheric_file.py       # Atmospheric data splitting utility
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── STREAMLIT_README.md            # Streamlit-specific docs
├── data/                          # ERA5 data files
│   ├── static.nc                  # Static variables (3.3MB)
│   ├── 2025-05-05-surface-level.nc    # Surface variables (27MB)
│   ├── 2025-05-05-atmospheric-part1.nc # Atmospheric data part 1 (99MB)
│   ├── 2025-05-05-atmospheric-part2.nc # Atmospheric data part 2 (97MB)
│   ├── 2025-05-05-atmospheric-part3.nc # Atmospheric data part 3 (95MB)
│   ├── 2025-05-05-atmospheric-part4.nc # Atmospheric data part 4 (59MB)
│   └── 2025-05-05-atmospheric-part5.nc # Atmospheric data part 5 (56MB)
└── .venv/                         # Virtual environment
         └── ERA5.ipynb                 # Original ERA5 exploration notebook
```

## Technical Details

### Data Processing Pipeline

1. **ERA5 Data Download:**
   - Uses CDS API to download global weather data for May 5, 2025
   - Downloads static, surface, and atmospheric variables
   - Atmospheric data includes 13 pressure levels (1000-50 hPa)

2. **Data Splitting for Deployment:**
   - Large atmospheric file (430MB) split into 5 parts (<100MB each)
   - Preserves all 13 pressure levels and global coverage
   - Maintains data integrity for Aurora model requirements

3. **Aurora Model Integration:**
   - Loads pre-trained Microsoft Aurora checkpoint
   - Creates batch data with proper metadata
   - Runs 6-step rollout predictions using PyTorch

4. **Visualization:**
   - Crops global data to Maldives region for display
   - Interactive Plotly maps with hover information
   - Fixed color scaling for consistent comparisons

### Aurora Model Requirements

The Aurora model expects specific data structure:
- **Surface variables:** 2m temperature, 10m winds, mean sea level pressure
- **Static variables:** Geopotential, land-sea mask
- **Atmospheric variables:** Temperature, winds, humidity, geopotential at pressure levels
- **Global coverage** with proper spatial dimensions

### File Splitting Strategy

To overcome GitHub's 100MB file limit:
- Original 430MB atmospheric file split by pressure levels
- 5 files: 3 levels each for parts 1-3, 2 levels each for parts 4-5
- Files automatically recombined during app loading
- Preserves full model performance

## Deployment

### Streamlit Community Cloud

This app is optimized for Streamlit Community Cloud deployment:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Weather prediction app ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - All data files will be automatically included

3. **No additional setup required:**
   - ERA5 data files are included in the repository
   - Aurora model downloads automatically on first run
   - No API keys needed for end users

### Local Development

For development and testing:
```bash
# Download fresh data
python download_era5_data.py

# Split atmospheric file
python split_atmospheric_file.py

# Run locally
streamlit run aurora_streamlit_app.py
```

## Usage Guide

### Main Interface

1. **Time Selection:**
   - Use sidebar dropdown to select forecast time
   - Options: 00:00, 06:00, 12:00, 18:00 (May 6, 2025)

2. **Interactive Maps:**
   - Four weather variables displayed in 2x2 grid
   - Hover over points to see exact values
   - Zoom/pan to explore different areas
   - Maps start at zoom level 6 showing full Maldives

3. **Weather Variables:**
   - **2m Temperature:** Surface air temperature in Kelvin
   - **10m Eastward Wind:** East-west wind component in m/s
   - **10m Southward Wind:** North-south wind component in m/s
   - **Mean Sea Level Pressure:** Atmospheric pressure in Pa

### Model Performance

- **Loading time:** 2-3 minutes for initial model download
- **Prediction time:** 1-2 minutes for 6-step forecast
- **Data size:** ~440MB total (split across 7 files)
- **Memory usage:** ~2GB during model inference

## Configuration

### Maldives Region Settings

The app focuses on the Maldives region:
```python
MALDIVES_LAT_RANGE = (-1.0, 8.0)  # Latitude bounds
MALDIVES_LON_RANGE = (72.0, 74.0)  # Longitude bounds
```

### ERA5 Data Configuration

Download settings in `download_era5_data.py`:
- **Date:** May 5, 2025 (for predictions on May 6)
- **Times:** 00:00, 06:00, 12:00, 18:00 UTC
- **Pressure levels:** 13 levels from 1000-50 hPa
- **Variables:** Temperature, winds, humidity, geopotential

## Troubleshooting

### Common Issues

1. **"Model loading takes too long"**
   - First run downloads ~2GB Aurora checkpoint
   - Subsequent runs use cached model
   - Requires stable internet connection

2. **"Data files not found"**
   - Run `python download_era5_data.py` first
   - Check CDS API credentials in `~/.cdsapirc`
   - Ensure all 7 data files exist in `data/` folder

3. **"Memory errors during prediction"**
   - Requires at least 4GB RAM
   - Close other applications
   - Use CPU instead of GPU if memory limited

4. **"Maps not displaying properly"**
   - Check internet connection (needed for map tiles)
   - Try refreshing the browser
   - Zoom level issues: maps start at level 6

### Performance Tips

1. **Faster loading:**
   - Keep model cached between runs
   - Use SSD storage for data files
   - Ensure adequate RAM

2. **Development workflow:**
   - Use `@st.cache_data` and `@st.cache_resource` decorators
   - Split file loading only when needed
   - Test with smaller data subsets first

## Requirements

Key Python packages:
- `streamlit` - Web app framework
- `torch` - PyTorch for Aurora model
- `xarray` - NetCDF data handling
- `plotly` - Interactive visualizations
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `cdsapi` - ERA5 data download

See `requirements.txt` for complete list with versions.

## Contributing

To contribute:
1. Fork the repository
2. Create a feature branch
3. Test your changes locally
4. Submit a pull request

Areas for improvement:
- Additional weather variables
- Extended forecast periods
- Different geographical regions
- Performance optimizations

## License

This project is for educational and research purposes. Please respect:
- ERA5 data licensing (Copernicus Climate Change Service)
- Aurora model terms (Microsoft Research)
- Associated package licenses

## Acknowledgments

- **Microsoft Research** for the Aurora weather forecasting model
- **ECMWF** for ERA5 reanalysis data
- **Copernicus Climate Change Service** for data access infrastructure
- **Streamlit** team for the excellent web application framework

## Support

For questions or issues:
1. Check this README and troubleshooting section
2. Verify data download and setup steps
3. Ensure all requirements are installed
4. Check GitHub issues for similar problems

---
