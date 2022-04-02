# FastAPI - Cryptocurrency Trading Signals
This project is a trading signals API, users add cryptocurrencies to their watchlist and get trading signals.

## Getting Started


#### Prerequisites
  - [Python](https://www.python.org/downloads/) is installed 


#### Run the project
1.create python virtualenv

        python3 -m venv venv

2.active python virtualenv

3.install packages

    pip install -r requirements.txt
4. set .env variables

5 .run project

        uvicorn main:app --reload
#### Running Database Migrations (Alembic)
##### Downgrade to the initial state (blank DB)
Run `alembic downgrade base`

##### Run all migrations to current/highest state
Run `alembic upgrade head`

#### Auto-Generated API Documentation

refer to `localhost:8001/docs` or `localhost:8001/redocs`