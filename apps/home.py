import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd

# import farms vector file as a gdf
farms_df = gpd.read_file(r"data/vector/ce_farms.gpkg")
farms = farms_df[['farmer', 'crop', 'district', 'province', 'area_ha', 'geometry']]

def add_selectors(farms):
    # create list of farms
    farm_names = list(set(farms["farmer"].to_list()))

    # normalised difference indices
    indices_list = ['Crop Health', 'Soil Moisture', ]

    # specify columns and their widths
    farm_names_col, indices_list_col, max_cloud_cover_col, submit_button_col = st.columns([3, 3, 3, 1.5])

    with farm_names_col:
        farm_name = st.selectbox(
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

    with max_cloud_cover_col:
        # max_cloud_cover = st.text_input('Select maximum cloud cover',
                                    # 0, 100, 20, step=5)
        max_cloud_cover = st.slider('Select maximum cloud cover',
                                    0, 100, 20, step=5)

    # with submit_button_col:
    #     submit_button = st.button("Submit")
    return farm_name, selected_index, max_cloud_cover#, submit_button_col

def app():
    st.title("Vegetation Health Monitor")

    st.markdown(
        """
    A [streamlit](https://streamlit.io) app for geospatial monitoring of crop health using Sentinel 2 imagery.
    """
    )

    farm_name, selected_index, max_cloud_cover = add_selectors(farms)
    selected_farm = farms[farms["farmer"] == farm_name]

    if farm_name == None:
        m = leafmap.Map(center= [-13.2, 28], zoom= 7)
        m.add_basemap("ROADMAP")
        m.add_gdf(farms, zoom_to_layer=False, layer_name="Farms")
        m.to_streamlit(height=700)

    else:
        m = leafmap.Map()
        m.add_basemap("ROADMAP")
        m.add_gdf(selected_farm, zoom_to_layer=True, layer_name="Farms")
        m.to_streamlit(height=700)
