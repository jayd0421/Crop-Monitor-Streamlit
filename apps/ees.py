import ee
import geemap

ee.Initialize()

def get_buffered_farm_gdf(selected_farm_gdf):
    proj_selected_farm_gdf = selected_farm_gdf.to_crs(epsg=3857)
    proj_selected_farm_gdf["geometry"] = proj_selected_farm_gdf.geometry.buffer(50)
    buffered_selected_farm_gdf = proj_selected_farm_gdf.to_crs(epsg=4326)

    return buffered_selected_farm_gdf

def get_available_images(selected_farm_gdf, selected_start_date, selected_end_date, max_cloud_cover):
    buffered_selected_farm_gdf = get_buffered_farm_gdf(selected_farm_gdf)

    buffered_selected_farm_ee = geemap.gdf_to_ee(buffered_selected_farm_gdf)

    available_images =  ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
        .filterBounds(buffered_selected_farm_ee) \
        .filterDate(selected_start_date, selected_end_date) \
        .select(["B12", "B11", "B8", "B4", "B3", "B2"]) \
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", max_cloud_cover))
    
    available_image = available_images.first().clip(buffered_selected_farm_ee)
    return available_image

def get_vis_params(selected_farm_gdf, selected_image):
    buffered_selected_farm_gdf = get_buffered_farm_gdf(selected_farm_gdf)

    buffered_selected_farm_ee = geemap.gdf_to_ee(buffered_selected_farm_gdf)

    # min_max = selected_image.reduceRegion(
    #     reducer=ee.Reducer.minMax(),
    #     geometry=buffered_selected_farm_ee,
    #     scale=10,
    #     maxPixels=1e9
    # )

    # min_dict = {
    #     'B4': min_max.get('B4_min'),
    #     'B3': min_max.get('B3_min'),
    #     'B2': min_max.get('B2_min')
    # }

    # max_dict = {
    #     'B4': min_max.get('B4_max'),
    #     'B3': min_max.get('B3_max'),
    #     'B2': min_max.get('B2_max')
    # }

    # vis_params = {
    #     'bands': ['B4', 'B3', 'B2'],
    #     'min': [min_dict['B4'], min_dict['B3'], min_dict['B2']],
    #     'max': [max_dict['B4'], max_dict['B3'], max_dict['B2']]
    # }

    vis_params = {
        'bands': ['B4', 'B3', 'B2'],
        'min': 200,
        'max': 2000
    }

    return vis_params