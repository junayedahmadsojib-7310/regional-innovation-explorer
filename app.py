import streamlit as st

from utils.ui import bootstrap_app, sidebar_brand


bootstrap_app("U.S. Regional Innovation Explorer", "🌐")

pages = [
    st.Page("pages/0_Overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/1_County_Innovation_Explorer.py", title="County Innovation Explorer", icon="📍"),
    st.Page("pages/2_Technology_Landscape.py", title="Technology Landscape", icon="🧭"),
    st.Page("pages/3_A61_Diffusion_Explorer.py", title="A61 Diffusion Explorer", icon="🌐"),
]

navigation = st.navigation(pages, position="sidebar")
sidebar_brand()
navigation.run()
