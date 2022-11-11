from typing import Any, Union
from fastapi import FastAPI, Query
import services
# from schemas import GetAllCurrenciesResponseSchema

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Team Bevel Black Market Exchange Rate Service"}


@app.get("/curriences")
def get_all_currencies() -> Any:
    """
    This endpoint returns all available and supported currencies.
    """
    return {'success': True, 'message': 'All available currencies retrived successfully.', 'data': services.get_currency_list() }


@app.get("/rates")
async def get_currency_rate(currency_code: Union[str, None] = Query(default='NGN', max_length=3, min_length=3)) -> Any:
    """
    This endpoint returns the exchange rate of a given currency. It defaults to `NGN` when a 
    currency_code is not provided. `currency_code`: It's a 3 letter code.
    """
    try:
        resp_data = await services.get_binancep2p_rate(currency_code)
        formatted_data = await services.format_response_data(resp_data)
        buy_rate = formatted_data[0]['adv']['price']
        sell_rate = formatted_data[1]['adv']['price']
        return {'success': True, 'message':f'Exchange rate for {currency_code} retrieved successfully.', 'currency': currency_code, 'buy': buy_rate, 'sell': sell_rate }
    except:
        return {'success': False, 'message': 'Unable to get rate'}
