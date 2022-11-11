import asyncio
from typing import Any, Dict, List, Optional
import aiohttp
from schemas import BinanceRequestSchema, BinanaceResponseSchema

binancep2p_endpoint = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
request_headers = {"Cache-Control": "no-cache", "Content-Type": "application/json"}

def get_currency_list()-> List[str]:
    currency_list = [
            "ARS",
            "EUR",
            "USD",
            "AED",
            "AUD",
            "BDT",
            "BHD",
            "BOB",
            "BRL",
            "CAD",
            "CLP",
            "CNY",
            "COP",
            "CRC",
            "CZK",
            "DOP",
            "DZD",
            "EGP",
            "GBP",
            "GEL",
            "GHS",
            "HKD",
            "IDR",
            "INR",
            "JPY",
            "KES",
            "KHR",
            "KRW",
            "KWD",
            "KZT",
            "LAK",
            "LBP",
            "LKR",
            "MAD",
            "MMK",
            "MXN",
            "MYR",
            "NGN",
            "OMR",
            "PAB",
            "PEN",
            "PHP",
            "PKR",
            "PLN",
            "PYG",
            "QAR",
            "RON",
            "RUB",
            "SAR",
            "SDG",
            "SEK",
            "SGD",
            "THB",
            "TND",
            "TRY",
            "TWD",
            "UAH",
            "UGX",
            "UYU",
            "VES",
            "VND",
            "ZAR"
    ]
    return currency_list 


async def make_post_request(
    session: aiohttp.ClientSession, url, data: Dict[str, Any], headers=request_headers
):
    async with session.post(url, json=data, ssl=True, headers=headers) as resp:
        payload = await resp.json()
        return payload


async def get_binancep2p_rate(currency_code: str) -> Optional[Dict[str, Any]]:
    """
    `currency_code`: 3 letter code
    """
    d1 = BinanceRequestSchema(fiat=currency_code, tradeType='sell').dict()
    d2 = BinanceRequestSchema(fiat=currency_code, tradeType='buy').dict()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for data in [d1, d2]:
            tasks.append(asyncio.ensure_future(make_post_request(session, binancep2p_endpoint, data)))

        results = await asyncio.gather(*tasks)
        return results


async def format_response_data(response_data: List[Dict[str, Any]]) -> Any:
    formatted_data = []
    for d in response_data:
        formatted_data.append(BinanaceResponseSchema(**d).dict())
    
    # Get the BUY Data
    buy_data = formatted_data[1]['data'][5]

    # Get the SELL Data
    sell_data = formatted_data[0]['data'][5]

    return [buy_data, sell_data]
    