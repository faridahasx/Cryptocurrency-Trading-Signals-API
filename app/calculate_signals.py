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


class BackgroundRunner:
    async def update_signals(self):
        await asyncio.sleep(0.1)
        if dt.now().hour == 22:
            session = Session(engine)
            signal_query = session.query(models.Crypto).all()

            for s in signal_query:
                #  Check if the crypto does not appear in anyone's watchlist, remove it from the database
                on_watchlist = session.query(models.Watchlist).filter(models.Watchlist.crypto_id == s.id).first
                crypto = session.execute(select(models.Crypto).filter_by(id=s.id)).scalar_one()

                if on_watchlist:
                    pair = s.name
                    exchange = s.exchange
                    signal_stage = calculate_signals(pair, exchange)
                    crypto.signal_stage = signal_stage
                    session.commit()
                else:
                    crypto.delete(synchronize_session=False)
                    session.commit()

            session.close()
