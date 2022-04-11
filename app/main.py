from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, auth, available_data, watchlist
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime as dt
from . import models
from . database import engine
from app.calculate_signals import calculate_signals
import asyncio


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BackgroundRunner:
    def __init__(self):
        self.updated = False

    async def update_signals(self):
        while True:
            await asyncio.sleep(0.1)
            if self.updated is False:
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
                    self.updated = True

            else:
                if dt.now().hour == 10:
                    self.updated = False


runner = BackgroundRunner()

@app.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.update_signals())



app.include_router(user.router)
app.include_router(auth.router)
app.include_router(available_data.router)
app.include_router(watchlist.router)
