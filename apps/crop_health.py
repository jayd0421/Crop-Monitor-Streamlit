import streamlit as st
import leafmap.foliumap as leafmap
import geemap.foliumap as geemap
import geopandas as gpd
import datetime
import ee
import folium
from apps import ees

# import farms vector file as a gdf
farms_gdf = gpd.read_file(r"data/vector/ce_farms.gpkg")
farms_gdf = farms_gdf[['farmer', 'crop', 'district', 'province', 'area_ha', 'geometry']]
farms_ee = geemap.gdf_to_ee(farms_gdf)

def add_selectors(farms_gdf):
    # create list of farms
    farm_names = list(set(farms_gdf["farmer"].to_list()))

    # normalised difference indices
    indices_list = ['Crop Health', 'Soil Moisture', ]

    # specify columns and their widths
    farm_names_col, indices_list_col, start_date_col, end_date_col, max_cloud_cover_col = st.columns([3, 3, 3, 3, 3])

    with farm_names_col:
        selected_farm_name = st.selectbox(
            "Select the farm to monitor",
            farm_names,
            index=None,
            placeholder="Select farm..."
        )

    with indices_list_col:
        selected_index = st.selectbox(
            "Select the metric to monitor",
            indices_list,
            index=None,
            placeholder="Select metric..."
        )

    with start_date_col:
        selected_start_date = str(st.date_input(
            "Select start date",
            datetime.date.today() - datetime.timedelta(days=7),
            # datetime.date.today() - datetime.timedelta(days=1),
        ))

    with end_date_col:
        selected_end_date = str(st.date_input(
            "Select end date",
            datetime.date.today(),
            # datetime.date.today() - datetime.timedelta(days=5),
        ))

    with max_cloud_cover_col:
        # max_cloud_cover = st.text_input('Select maximum cloud cover',
                                    # 0, 100, 20, step=5)
        max_cloud_cover = st.slider('Select maximum cloud cover',
                                    0, 100, 20, step=5)
        
    return selected_farm_name, selected_index, selected_start_date, selected_end_date, max_cloud_cover


def add_ee_layer(self, ee_object, visparams={}, name='Layer', shown=True, opacity=1.0):
    try:
        if isinstance(ee_object, ee.Image):
            map_id_dict = ee.Image(ee_object).getMapId(visparams)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True,
                show=shown,
                opacity=opacity
            ).add_to(self)
        elif isinstance(ee_object, ee.ImageCollection):
            ee_object_new = ee_object.mosaic()
            map_id_dict = ee.Image(ee_object_new).getMapId(visparams)
            folium.raster_layers.TileLayer(
                tiles=map_id_dict['tile_fetcher'].url_format,
                attr='Google Earth Engine',
                name=name,
                overlay=True,
                control=True,
                show=shown,
                opacity=opacity
            ).add_to(self)
        elif isinstance(ee_object, ee.Geometry) or isinstance(ee_object, ee.Feature) or isinstance(ee_object, ee.FeatureCollection):
            folium.GeoJson(
                data=ee_object.getInfo(),
                name=name
            ).add_to(self)
        else:
            print("Could not add EE object to the map")
    except Exception as e:
        print("Error adding Earth Engine layer: ", e)

def app():
    st.title("Vegetation Health Monitor")

    st.markdown(
        """
    A [streamlit](https://streamlit.io) app for geospatial monitoring of crop health using Sentinel 2 imagery.
    """
    )

    selected_farm_name, selected_index, selected_start_date, selected_end_date, max_cloud_cover = add_selectors(farms_gdf)
    selected_farm_gdf = farms_gdf[farms_gdf["farmer"] == selected_farm_name]
    buffered_selected_farm_gdf = ees.get_buffered_farm_gdf(selected_farm_gdf)

    imagery = ees.get_available_images(selected_farm_gdf, selected_start_date, selected_end_date, max_cloud_cover)
    selected_visparams = ees.get_vis_params(selected_farm_gdf, imagery)

    if selected_farm_name is None:
        m = geemap.Map()
        # m.add_basemap("ROADMAP")
        m.zoom_to_gdf(farms_gdf)
        m.add_gdf(farms_gdf, layer_name="Farms")
        m.to_streamlit(height=700)

    else:
        m = geemap.Map()
        # m.add_basemap("ROADMAP")
        m.add_ee_layer = add_ee_layer.__get__(m)
        m.add_ee_layer(imagery, visparams= selected_visparams, name= 'Imagery')
        m.add_gdf(selected_farm_gdf, layer_name="Farm")
        m.zoom_to_gdf(buffered_selected_farm_gdf)
        m.to_streamlit(height=700)