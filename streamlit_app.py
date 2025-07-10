import streamlit as st
from streamlit_option_menu import option_menu
from apps import compare, crop_health, timelapse  # import your app modules here

st.set_page_config(page_title="Streamlit Geospatial", layout="wide")

# A dictionary of apps in the format of {"App title": "App icon"}
# More icons can be found here: https://icons.getbootstrap.com

apps = [
    {"func": crop_health.app, "title": "Home", "icon": "leaf"},
    {"func": compare.app, "title": "Compare Health", "icon": "map"},
    {"func": timelapse.app, "title": "Timelapse", "icon": "hourglass-split"},
]

titles = [app["title"] for app in apps]
titles_lower = [title.lower() for title in titles]
icons = [app["icon"] for app in apps]

# params = st.experimental_get_query_params()

# if "page" in params:
#     default_index = int(titles_lower.index(params["page"][0].lower()))
# else:
#     default_index = 0

with st.sidebar:
    selected = option_menu(
        "Menu",
        options=titles,
        icons=icons,
        menu_icon="globe-europe-africa",
        # default_index=default_index,
    )

    st.sidebar.title("About")
    st.sidebar.info(
        """
        This web [app](https://crop-monitor-app-yyhg7vyflyu7dwisr8hihf.streamlit.app/) is maintained by Jedidiah Chibinga.
    """
    )

for app in apps:
    if app["title"] == selected:
        app["func"]()
        break
