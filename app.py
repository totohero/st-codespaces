import streamlit as st 
import binance_util

st.set_page_config(page_title = "Screener WebApp") 
st.title("Screener")

st.write("Non-trivial symbols:")

# creating a placeholder for the fixed sized textbox
logtxtbox = st.empty()

def st_progress(a):
    # logtxtbox.text_area("Logging: ", a, height = 100)
    print(a)

binance_util.progress_func = st_progress
st.write(binance_util.get_non_trivial_symbols())

binance_util.show_vol_atr_map()