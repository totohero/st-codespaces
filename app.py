import streamlit as st 
from streamlit.logger import get_logger
import binance_util
import logging

st.set_page_config(page_title = "Screener WebApp") 

class StreamlitLogHandler(logging.Handler):
    def __init__(self, widget_update_func):
        super().__init__()
        self.widget_update_func = widget_update_func

    def emit(self, record):
        msg = self.format(record)
        self.widget_update_func(msg)

log_box = st.empty()
logger = get_logger("binance_util")
logger.handlers.clear()
handler = StreamlitLogHandler(log_box.code)
logger.addHandler(handler)

st.title("Screener")

st.write("RSI / ATR% (with minimum volume criteria)")
binance_util.show_vol_atr_map()
