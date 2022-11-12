from typing import Any, Union
from fastapi import FastAPI, Query
import services
from schemas import GetAllCurrenciesResponseSchema

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Team Bevel Black Market Exchange Rate Service"}


@app.get("/curriences", response_model=GetAllCurrenciesResponseSchema)
def get_all_currencies() -> Any:
    """
    This endpoint returns all available and supported currencies.
    """
    return {
        "success": True,
        "message": "All available currencies retrived successfully.",
        "data": services.get_currency_list(),
    }


@app.get("/rates")
async def get_currency_rate(
    currency_code: Union[str, None] = Query(default="NGN", max_length=3, min_length=3)
) -> Any:
    """
    This endpoint returns the exchange rate of a given currency. It defaults to `NGN` when a
    currency_code is not provided. `currency_code`: It's a 3 letter code.
    """
    currency_code = currency_code.upper()
    if currency_code not in services.get_currency_list():
        return {"success": False, "message": "Please send a valid currency_code."}
    try:
        resp_data = await services.get_binancep2p_rate(currency_code)
        formatted_data = await services.format_response_data(resp_data)
        return {
            "success": True,
            "message": f"Exchange rate for {currency_code} retrieved successfully.",
            "base_currency": "USD",
            "currency": currency_code,
            "buy": formatted_data["buy_rate"],
            "sell": formatted_data["sell_rate"],
        }
    except:
        return {"success": False, "message": "Unable to get rate"}


@app.get("/convert")
async def convert_currency(
    *,
    from_currency: str = Query(default="NGN", max_length=3, min_length=3),
    to_currency: str = Query(default="USD", max_length=3, min_length=3),
    amount: str,
) -> Any:
    """
    This endpoint converts amount from one currency to another.
    `amount`: The amount you want to covert
    `from`: The currency you want to convert from.
    `to`: The currency you want to convert to.
    """
    currency_list = services.get_currency_list()
    if (
        from_currency.upper() not in currency_list
        or to_currency.upper() not in currency_list
    ):
        return {"success": False, "message": "Please send a valid currency_code."}

    # FORMULAR
    # Get usd value of both from_currency and to_currency
    # Divide amount_given by from_usd_rate
    # multiply the result by to_usd_rate to get actual rate.

    try:
        from_currency_resp_data = await services.get_binancep2p_rate(from_currency)
        to_currency_resp_data = await services.get_binancep2p_rate(to_currency)
        from_currency_formatted_data = await services.format_response_data(
            from_currency_resp_data
        )
        to_currency_formatted_data = await services.format_response_data(
            to_currency_resp_data
        )

        from_rate_in_usd = float(from_currency_formatted_data["buy_rate"])
        to_rate_in_usd = float(to_currency_formatted_data["buy_rate"])

        result = float(amount) / from_rate_in_usd * to_rate_in_usd

        result = "{:,.2f}".format(result)

        return {
            "amount": amount,
            "from": from_currency,
            "to": to_currency,
            "total": result,
        }
    except:
        return {"success": False, "message": "Unable to get rate"}
