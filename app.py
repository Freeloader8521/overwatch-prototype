
import streamlit as st

st.set_page_config(page_title="Overwatch v5", layout="wide")

st.title("Overwatch Prototype v5")

st.sidebar.title("Exposure Layers")

st.sidebar.checkbox("Show office locations", value=True)
st.sidebar.checkbox("Show temporary locations", value=True)
st.sidebar.checkbox("Show travelling staff locations", value=True)

st.write("v5 placeholder generated successfully.")
