import streamlit as st
import leafmap.foliumap as leafmap


def app():
    st.title("Home")

    st.markdown(
        """
    A [streamlit](https://streamlit.io) app for geospatial monitoring of crop health using Sentinel 2 imagery.
    """
    )

    m = leafmap.Map(center= [-13, 28], zoom= 6)
    m.add_basemap("ROADMAP")
    m.to_streamlit(height=700)
