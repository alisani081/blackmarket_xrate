from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class BinanceRequestSchema(BaseModel):
    proMerchantAds: bool = False
    page: int = 1
    rows: int = 11
    asset: str = 'USDT'
    fiat: Optional[str] = 'NGN'
    tradeType: str


class EndpointResponseSchema(BaseModel):
    success: bool
    message: str


class GetAllCurrenciesResponseSchema(EndpointResponseSchema):
    data: List[str]


class Adv(BaseModel):
    tradeType: str
    asset: str
    fiatUnit: str
    price: str
    fiatSymbol: str


class BinanceResponseData(BaseModel):
    adv: Adv


class BinanaceResponseSchema(BaseModel):
    data: List[BinanceResponseData]
    # created_at: Optional[datetime] = datetime.now()
    # success: bool
