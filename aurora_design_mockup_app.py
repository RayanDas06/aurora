import streamlit as st
import plotly.graph_objects as go
import numpy as np

def create_interactive_map(data, lats, lons, title, unit, colorscale='RdYlBu_r'):
    """Create interactive geographic map with fixed color scaling"""
    lon_grid, lat_grid = np.meshgrid(lons, lats)
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
            cmin=vmin,
            cmax=vmax,
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
            zoom=6
        ),
        title=title,
        height=450,
        margin={"r":0,"t":30,"l":0,"b":0}
    )
    return fig

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Aurora Design Mockup",
    layout="wide"
)

# --- LOCATION SELECTOR ---
locations = [
    "Malé", "Port Louis", "Chennai", "Dar es Salaam", "Perth", "Muscat", "Maputo", "Jakarta", "Phuket"
]

# --- VARIABLE NAMES ---
all_variables = [f"Variable {i+1}" for i in range(36)]
variables_by_tab = [all_variables[i*9:(i+1)*9] for i in range(4)]

# --- SIDEBAR/HEADER LAYOUT ---
st.markdown("""
    <style>
    .location-selector {float: right; margin-top: -60px;}
    .world-map {float: left;}
    </style>
""", unsafe_allow_html=True)

# --- HEADER ROW ---
col_map, col_selector = st.columns([2, 1])

# Coordinates for each location
location_coords = {
    "Malé": (3.2, 73.2),         # North-central Indian Ocean
    "Port Louis": (-20.16, 57.50),   # Mauritius
    "Chennai": (13.08, 80.27),      # North-east (India)
    "Dar es Salaam": (-6.8, 39.28), # West (Tanzania)
    "Perth": (-31.95, 115.86),      # East (Australia)
    "Muscat": (23.61, 58.59),       # North-west (Oman)
    "Maputo": (-25.97, 32.58),      # South-west (Mozambique)
    "Jakarta": (-6.21, 106.85),     # East (Indonesia)
    "Phuket": (7.88, 98.39)         # North-east (Thailand)
}

with col_map:
    st.markdown("#### World Map")
    # World map with markers for each location
    world_lats = [v[0] for v in location_coords.values()]
    world_lons = [v[1] for v in location_coords.values()]
    world_names = list(location_coords.keys())
    world_fig = go.Figure(go.Scattermapbox(
        lat=world_lats,
        lon=world_lons,
        mode='markers+text',
        marker=dict(size=12, color='red'),
        text=world_names,
        textposition="top right"
    ))
    world_fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(
            center=dict(lat=0, lon=0),
            zoom=1.2
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=350
    )
    st.plotly_chart(world_fig, use_container_width=True)

with col_selector:
    st.markdown("#### Location Selector")
    selected_location = st.selectbox("Select a location:", locations, key="location_selector")

# --- SUBPAGE BUTTONS ---
st.markdown("---")
col_b1, col_b2, col_b3, col_b4 = st.columns(4)

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = 0

with col_b1:
    if st.button("Tab 1", key="tab1"):
        st.session_state["active_tab"] = 0
with col_b2:
    if st.button("Tab 2", key="tab2"):
        st.session_state["active_tab"] = 1
with col_b3:
    if st.button("Tab 3", key="tab3"):
        st.session_state["active_tab"] = 2
with col_b4:
    if st.button("Tab 4", key="tab4"):
        st.session_state["active_tab"] = 3

# --- 3x3 GRID OF MAPS ---
st.markdown("---")
current_variables = variables_by_tab[st.session_state["active_tab"]]
st.markdown(f"### 3x3 Grid of Maps for {selected_location} (Variables {st.session_state['active_tab']*9+1}-{st.session_state['active_tab']*9+9})")

# Get center lat/lon for selected location
center_lat, center_lon = location_coords[selected_location]
# Create a small grid around the center for demo
lats = np.linspace(center_lat-1, center_lat+1, 8)
lons = np.linspace(center_lon-1, center_lon+1, 8)

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        var_idx = i*3 + j
        with cols[j]:
            # Fake data: just zeros for now
            data = np.zeros((len(lats), len(lons)))
            fig = create_interactive_map(
                data, lats, lons,
                current_variables[var_idx], "unit", "RdYlBu_r"
            )
            st.plotly_chart(fig, use_container_width=True) 