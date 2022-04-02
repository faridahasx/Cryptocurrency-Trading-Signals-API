from fastapi import status, HTTPException, Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
import ccxt
from app.calculate_signals import calculate_signals

router = APIRouter(
    prefix="/watchlist",
    tags=['Watchlist'])


def add(pair, exchange, user_id, crypto_id, condition):

    Session = Depends(get_db)
    if condition == 'database':
        new_pair = models.Crypto(name=pair, exchange=exchange,
                                 signal_stage=calculate_signals(pair, exchange),
                                 id=crypto_id)
        print(new_pair.dict())
        Session.add(new_pair)
        Session.commit()
        Session.refresh(new_pair)

    # Add to the watchlist

    to_watchlist = models.Watchlist(user_id=user_id, crypto_id=crypto_id)
    Session.add(to_watchlist)
    Session.commit()
    Session.refresh(to_watchlist)



@router.post("/", status_code=status.HTTP_201_CREATED)
def add_crypto_to_watchlist(background_task: BackgroundTasks, crypto: schemas.Crypto, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    exchange = crypto.crypto_exchange.lower()
    pair_symbol = crypto.pair_name.upper()
    crypto_id = pair_symbol + '/' + exchange

    watchlist = db.query(models.Watchlist).filter(models.Watchlist.user_id == current_user.id,
                                                  models.Watchlist.crypto_id == crypto_id)
    already_on_watchlist = watchlist.first()

    if already_on_watchlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="already on watchlist")

    # If crypto is not in the database, first add the crypto to the database
    crypto_query = db.query(models.Crypto).filter(models.Crypto.name == pair_symbol,
                                                  models.Crypto.exchange == exchange).first()
    if not crypto_query:
        try:
            get_exchange = getattr(ccxt, exchange)()

        except AttributeError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Exchange "{exchange}" not found.')
        else:
            pairs = get_exchange.load_markets()
            pairs = list(pairs.keys())
            if pair_symbol not in pairs:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'Pair "{pair_symbol}" not found.')
            background_task.add_task(add,pair_symbol, exchange,current_user.id,crypto_id,'database' )


    else:
        print(999)
        background_task.add_task(add, pair_symbol, exchange, current_user.id, crypto_id, 'only watchlist')

    return {f'Adding {pair_symbol} to watchlist'}


@router.get("/", response_model=List[schemas.Signal])
def get_watchlist(db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    users_watchlist = db.query(models.Crypto).join(models.Watchlist).filter(models.Watchlist.user_id == current_user.id,
                                                                            models.Watchlist.crypto_id == models.Crypto.id).all()

    return users_watchlist


@router.get("/{side}", response_model=List[schemas.Signal])
def get_bullish_or_bearish_signals_from_watchlist(side: str, db: Session = Depends(get_db),
                                                  current_user: int = Depends(oauth2.get_current_user)):
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    side = side.capitalize()
    watchlist = db.query(models.Crypto).join(models.Watchlist).filter(models.Watchlist.user_id == current_user.id,
                                                                      models.Watchlist.crypto_id == models.Crypto.id,
                                                                      models.Crypto.signal_stage == side).all()

    return watchlist


@router.delete("/{exchange}/{pair_symbol}", status_code=status.HTTP_204_NO_CONTENT)
def remove_crypto_from_watchlist(exchange: str, pair_symbol: str, db: Session = Depends(get_db),
                                 current_user: int = Depends(oauth2.get_current_user)):

    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    exchange = exchange.lower()
    pair_symbol = pair_symbol.upper()
    crypto_id = pair_symbol + '/' + exchange

    watchlist = db.query(models.Watchlist).filter(models.Watchlist.user_id == current_user.id,
                                                  models.Watchlist.crypto_id == crypto_id)
    on_watchlist = watchlist.first()

    if not on_watchlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not found on watchlist")



    watchlist.delete(synchronize_session=False)
    db.commit()

    return {"message": f"removed the {pair_symbol} from watchlist"}

