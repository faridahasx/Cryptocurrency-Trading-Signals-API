from fastapi import status, HTTPException, APIRouter
from .. import schemas
import ccxt

router = APIRouter(
    prefix="/exchanges",
    tags=['Exchanges'])


@router.get('/', response_model=schemas.ListMessage)
def get_available_exchanges():
    exchanges = ccxt.exchanges
    return {"message": exchanges}


@router.get('/{exchange}', response_model=schemas.ListMessage)
def get_available_pairs_from_exchange(exchange: str):
    exchange = exchange.lower()

    try:
        get_exchange = getattr(ccxt, exchange)()

    except AttributeError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Exchange "{exchange}" not found.')
    else:
        pairs = get_exchange.load_markets()
        pairs = list(pairs.keys())
        return {"message": pairs}
