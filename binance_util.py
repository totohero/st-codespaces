from binance.client import Client
import pandas as pd
import streamlit as st

@st.cache_data
def get_symbols():
    binance_client = Client()

    futures_exchange_info = binance_client.futures_exchange_info()
    symbols = [symbol['symbol'] for symbol in futures_exchange_info['symbols']
            if 'PERP' in symbol['contractType'] and 'USDT' in symbol['symbol']] #  if 'USDT' in symbol['symbol'] and 'BTCUSDT' != symbol['symbol']
    return symbols
