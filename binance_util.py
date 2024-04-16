from binance.client import Client
import pandas as pd
import streamlit as st
import logging

logger = logging.getLogger(__name__)

binance_client = Client()

@st.cache_data
def get_symbols():
    futures_exchange_info = binance_client.futures_exchange_info()
    symbols = [symbol['symbol'] for symbol in futures_exchange_info['symbols']
            if 'PERP' in symbol['contractType'] and 'USDT' in symbol['symbol']] #  if 'USDT' in symbol['symbol'] and 'BTCUSDT' != symbol['symbol']
    return symbols


@st.cache_data(ttl="10m")
def fetch_historical_klines(symbol, interval):
    start_str = "20 min ago UTC" # 200 min before from now
    klines = binance_client.futures_historical_klines(symbol, interval, start_str, None)
    # convert klines to df row
    df = pd.DataFrame(klines, columns = ['open_time', 'o', 'h', 'l', 'c', 'v', 'close_time', 'quote_asset_volume',
                                          'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    
    # specify open_time as index
    df.set_index('open_time', inplace = True)

    # remove columns: close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, ignore
    df.drop(columns = ['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'], inplace = True)
    df = df.astype(float)
    return df

# @st.cache_data(ttl="10m")
def fetch_all_symbols_klines():
    symbols = get_symbols()
    sym_klines = {}

    i = 0
    for sym in symbols:
        i = i + 1
        logger.info(f"{i}/{len(symbols)} processing {sym}")
        sym_klines[sym] = fetch_historical_klines(sym, "1m")
    
    logger.info("fetch_all_symbols_klines done")
    return sym_klines


import pandas_ta as ta
import matplotlib.pyplot as plt

def show_vol_atr_map():
    sym_klines = fetch_all_symbols_klines()
    symbols = sym_klines.keys()

    # Lists to store values for each symbol
    volusdsma_values = []
    volratio_values = []
    atrp_values = []
    rsi_values = []
    sym_labels = []

    # Collect requisite data for each symbol
    for sym in symbols:
        df = sym_klines[sym]
        volsma = df.ta.sma(close=df.v, length=10)
        volusdsma = round(df.ta.sma(close=df.v * df.c, length=10))
        volratio = round(100.0 * df.v / volsma)
        atr = df.ta.atr(high=df.h, low=df.l, close=df.c, length=10)
        atrp = round(100.0 * atr / df.c, 2)
        rsi = df.ta.rsi(high=df.h, low=df.l, close=df.c, length=10)

        if volusdsma.iloc[-1] > 10000 and atrp.iloc[-1] > 0.4:
            volusdsma_values.append(volusdsma.iloc[-1])
            volratio_values.append(volratio.iloc[-1] * 2)
            atrp_values.append(atrp.iloc[-1])
            rsi_values.append(rsi.iloc[-1])
            sym_labels.append(sym)

    # Create scatter plot
    fig = plt.figure(figsize=(10, 7))
    scatter = plt.scatter(rsi_values, atrp_values, s=volratio_values, alpha=0.5)

    # Add labels for each symbol
    for i in range(len(volratio_values)):
        plt.annotate(sym_labels[i], (rsi_values[i], atrp_values[i]))

    plt.xlabel('RSI')
    plt.ylabel('ATRP')
    plt.title('Scatter Map of RSI and ATRP')
    plt.grid(True)
    # plt.show()

    st.pyplot(fig)
