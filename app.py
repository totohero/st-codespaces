import streamlit as st 
import binance_util

st.set_page_config(page_title = "This is a Multipage WebApp") 
st.title("This is the Home Page Geeks.")

st.write("Hello, world???")

st.write(binance_util.get_symbols())