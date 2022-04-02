from fastapi import status, HTTPException
import ccxt
import pandas as pd
from ta.trend import IchimokuIndicator
from datetime import timedelta, datetime as dt


def calculate_signals(pair, exchange):
    # GET DATA
    try:
        exchange = getattr(ccxt, exchange)()
        exchange.load_markets()

        days = timedelta(days=60)
        ending_date = dt.now()
        since = ending_date - days
        since = exchange.parse8601(since)

        data = exchange.fetch_ohlcv(pair, '1d', since=since, limit=60)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"{e}")

    # To DataFrame
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(data, columns=header)

    ichimoku = IchimokuIndicator(high=df['High'], low=df['Low'], window1=9, window2=26, window3=52)
    ichimoku_base = ichimoku.ichimoku_base_line()
    df['trend'] = ichimoku_base

    # Calculate
    close = float(df['Close'][len(df.index) - 2])
    open = float(df['Open'][len(df.index) - 2])
    trend = float(df['trend'][len(df.index) - 2])

    signal_stage = 0

    if close <= open * 0.95:
        signal_stage = 'Bearish'
    else:
        if close <= trend:
            signal_stage = 'Bearish'
        else:
            for row in df.itertuples(index=False):
                if row.Close <= row.Open * 0.95:
                    signal_stage = 'Bearish'
                elif signal_stage == 'Bearish':
                    if row.Close < row.trend:
                        signal_stage = 0

            if signal_stage == 0 and close > trend:
                signal_stage = 'Bullish'

    return signal_stage


