# FastAPI - Cryptocurrency Trading Signals
This project is a trading signals API, users add cryptocurrencies to their watchlist and get trading signals.

## Getting Started


### Prerequisites
  - [Python](https://www.python.org/downloads/) is installed 


### Run the project
##### 1. Create python virtualenv

        python3 -m venv venv

##### 2. Active python virtualenv

##### 3. Install packages

    pip install -r requirements.txt
##### 4. Set .env variables

##### 5. Run Database Migrations (Alembic)

###### Run all migrations to current/highest state

    alembic upgrade head

###### Downgrade to the initial state (blank DB)
    
    alembic downgrade base

##### 6. Run project

        uvicorn main:app --reload



### Auto-Generated API Documentation

navigate to `localhost:8001/docs` or `localhost:8001/redocs`
