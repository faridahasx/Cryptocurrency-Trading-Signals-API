# FastAPI - Cryptocurrency Trends API
This project is an API for cryptocurrency trends. 
Users can create profiles and add cryptocurrencies to their watchlist to follow trends.

#### Bullish Trend
- Price is above ichimoku conversion line

#### Bearish Trend
- Price is below ichimoku conversion line

or 

- If daily candle is closed with more than 5% loss, the trend will remain bearish until price crosses from below to above ichimoku conversion line.

***

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

###### Downgrade to the initial state
    
    alembic downgrade base

##### 6. Run project

        uvicorn main:app --reload



### Auto-Generated API Documentation

navigate to `localhost:8001/docs` or `localhost:8001/redocs`
