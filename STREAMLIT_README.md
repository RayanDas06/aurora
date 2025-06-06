# Aurora Weather Predictions - Streamlit App

🌤️ **Interactive web app for visualizing Aurora model weather predictions over the Maldives**

## Overview

This Streamlit application provides an interactive interface to visualize Aurora weather model predictions for the Maldives region on May 6, 2025. The app displays four key weather variables as gradient maps with clickable interactions.

## Features

- **Interactive Time Selection**: Choose from 4 different times on May 6, 2025 (00:00, 06:00, 12:00, 18:00)
- **Four Weather Variables**:
  - 2-meter Temperature (K)
  - 10-meter Eastward Wind Speed (m/s)
  - 10-meter Southward Wind Speed (m/s)
  - Mean Sea Level Pressure (Pa)
- **Interactive Maps**: Hover over any location to see exact values
- **Maldives-Focused**: Automatically crops to the Maldives geographic region
- **Real-time Predictions**: Uses Aurora model predictions, not raw ERA5 data

## Prerequisites

1. **Aurora Model Data**: Ensure you have run the ERA5 Jupiter notebook first to:
   - Download ERA5 data files to `~/downloads/`
   - Have the Aurora model checkpoint available

2. **Python Environment**: Make sure you have all required packages installed:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Option 1: Simple Launch Script
```bash
python run_app.py
```

### Option 2: Direct Streamlit Command
```bash
streamlit run aurora_streamlit_app.py
```

### Option 3: Custom Port
```bash
streamlit run aurora_streamlit_app.py --server.port 8502
```

## Usage

1. **Launch the App**: Use one of the run methods above
2. **Wait for Loading**: The app will load the Aurora model and generate predictions (this may take a few minutes)
3. **Select Time**: Use the sidebar dropdown to choose a time on May 6, 2025
4. **Explore Maps**: 
   - Each map shows a different weather variable
   - Hover over any point to see exact values
   - Use zoom and pan controls to explore
5. **Compare Variables**: All four variables are displayed simultaneously for easy comparison

## App Structure

- `aurora_streamlit_app.py` - Main Streamlit application
- `run_app.py` - Simple launcher script
- `requirements.txt` - Python dependencies

## Technical Details

### Data Pipeline
1. Loads ERA5 data from `~/downloads/` directory
2. Initializes Aurora 0.25 pretrained model
3. Creates batch data from 5/5/2025 12:00 and 18:00 input times
4. Runs 6-step predictions to get 5/6/2025 forecasts
5. Crops data to Maldives region for visualization

### Predictions Timeline
- **Input Data**: May 5, 2025 at 12:00 and 18:00
- **Prediction Steps**:
  - Step 1: May 5, 2025 12:00 ✅
  - Step 2: May 5, 2025 18:00 ✅  
  - Step 3: May 6, 2025 00:00 📊 (Displayed)
  - Step 4: May 6, 2025 06:00 📊 (Displayed)
  - Step 5: May 6, 2025 12:00 📊 (Displayed)
  - Step 6: May 6, 2025 18:00 📊 (Displayed)

### Geographic Bounds
- **Latitude**: -1.0° to 8.0° (covers Maldives with buffer)
- **Longitude**: 72.0° to 74.0° (covers Maldives with buffer)

## Troubleshooting

### Common Issues

1. **"Error loading model or data"**
   - Ensure ERA5 data files exist in `~/downloads/`
   - Check that Aurora model checkpoint is downloaded
   - Verify all packages are installed

2. **App loads slowly**
   - First run takes longer as model loads
   - Subsequent runs use Streamlit caching for faster loading

3. **Empty maps**
   - Check that data exists for the Maldives region
   - Verify geographic bounds are correct

4. **Port already in use**
   - Use a different port: `streamlit run aurora_streamlit_app.py --server.port 8502`

### Performance Tips

- The app uses Streamlit caching for model and data loading
- First run may take 2-5 minutes depending on hardware
- Subsequent interactions should be much faster

## File Requirements

Make sure these files exist before running:
- `~/downloads/static.nc`
- `~/downloads/2025-05-05-surface-level.nc`  
- `~/downloads/2025-05-05-atmospheric.nc`
- Aurora model checkpoint (downloaded automatically)

## Browser Compatibility

Tested with:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Support

If you encounter issues:
1. Check that all prerequisites are met
2. Verify file paths and permissions
3. Ensure Python environment has all required packages
4. Check the terminal output for detailed error messages 