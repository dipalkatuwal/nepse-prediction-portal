from pydantic import BaseModel, field_validator
from typing import List


class PredictionRequest(BaseModel):
    """Replaces DRF NepsePredictionSerializer."""
    ticker: str

    @field_validator("ticker")
    @classmethod
    def ticker_max_length(cls, v):
        if len(v) > 20:
            raise ValueError("Ticker must be 20 characters or fewer")
        return v.upper()


class PredictionResponse(BaseModel):
    status: str
    plot_img: str
    plot_100_dma: str
    plot_200_dma: str
    plot_prediction: str
    mse: float
    rmse: float
    r2: float
    yesterday_price: float
    predicted_price: float
    next_week_prices: List[float]
    plot_next_week: str
