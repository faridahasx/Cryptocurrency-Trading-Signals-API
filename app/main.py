from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from .routers import user, auth, available_data, watchlist
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime as dt
from . import models
from . database import engine
from app.calculate_signals import calculate_signals, BackgroundRunner
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

runner = BackgroundRunner()

# Run a background task in every 24 hours to update cryptocurrency signals
@app.on_event('startup')
@repeat_every(seconds=60*60*24) 
async def app_startup():
    asyncio.create_task(runner.update_signals())

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(available_data.router)
app.include_router(watchlist.router)
