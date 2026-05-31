from fastapi import APIRouter, Depends, HTTPException, status
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from keras.models import load_model

from auth.models import User
from auth.security import get_current_user
from prediction.schemas import PredictionRequest, PredictionResponse
from prediction.utils import save_plot

router = APIRouter(tags=["prediction"])

# Resolve paths relative to the project root (same logic as Django BASE_DIR)
BASE_DIR = Path(__file__).resolve().parents[2]   # …/stock-prediction-portal
MODEL_PATH = Path(__file__).resolve().parents[1] / "stock_prediction_model.keras"


# POST /api/v1/predict/  →  replaces NepsePredictionAPIView.post()
@router.post(
    "/predict/",
    response_model=PredictionResponse,
    # Require a valid JWT — replaces DRF's IsAuthenticated (add this dependency
    # if you want the endpoint protected; remove it to keep it public)
    # dependencies=[Depends(get_current_user)],
)
def predict_stock(
    payload: PredictionRequest,
    # current_user: User = Depends(get_current_user),  # uncomment to protect
):
    ticker = payload.ticker

    # --- Load CSV data ---
    now = datetime.now()
    start = datetime(now.year - 10, now.month, now.day)
    csv_path = BASE_DIR / "Resources" / "data" / f"{ticker}.csv"

    if not csv_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data file found for ticker '{ticker}'.",
        )

    df = pd.read_csv(csv_path)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data found for the given ticker.",
        )

    df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce")
    df = df[(df["published_date"] >= start) & (df["published_date"] <= now)]
    df = df.drop(
        columns=["per_change", "traded_amount", "status"], errors="ignore"
    ).reset_index(drop=True)

    # --- Historical Closing Price Plot ---
    plt.figure(figsize=(12, 5))
    plt.plot(df.close, label="Closing Price")
    plt.title(f"Closing Price of {ticker}")
    plt.xlabel("Days")
    plt.ylabel("Close Price")
    plt.legend()
    plot_img = save_plot(f"{ticker}_plot.png")

    # --- 100-day Moving Average ---
    ma100 = df.close.rolling(100).mean()
    plt.figure(figsize=(12, 5))
    plt.plot(df.close, label="Closing Price")
    plt.plot(ma100, "r", label="100 DMA")
    plt.title(f"100-Day Moving Average of {ticker}")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plot_100_dma = save_plot(f"{ticker}_100_dma.png")

    # --- 200-day Moving Average ---
    ma200 = df.close.rolling(200).mean()
    plt.figure(figsize=(12, 5))
    plt.plot(df.close, label="Closing Price")
    plt.plot(ma200, "g", label="200 DMA")
    plt.title(f"200-Day Moving Average of {ticker}")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plot_200_dma = save_plot(f"{ticker}_200_dma.png")

    # --- Split data for LSTM ---
    data_training = pd.DataFrame(df.close[0 : int(len(df) * 0.7)])
    data_testing = pd.DataFrame(df.close[int(len(df) * 0.7) :])

    scaler = MinMaxScaler(feature_range=(0, 1))
    model = load_model(str(MODEL_PATH))

    past_100_days = data_training.tail(100)
    final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
    input_data = scaler.fit_transform(final_df)

    # --- Prepare test data ---
    x_test, y_test = [], []
    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i - 100 : i])
        y_test.append(input_data[i, 0])
    x_test, y_test = np.array(x_test), np.array(y_test)

    # --- Predict on test data ---
    y_predicted = model.predict(x_test)
    y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1)).flatten()
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

    # --- Final Prediction Plot ---
    plt.figure(figsize=(12, 5))
    plt.plot(y_test, "b", label="Original Price")
    plt.plot(y_predicted, "r", label="Predicted Price")
    plt.title(f"Final Prediction of {ticker}")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.legend()
    plot_prediction = save_plot(f"{ticker}_final_prediction.png")

    # --- Model Evaluation ---
    mse = float(mean_squared_error(y_test, y_predicted))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_test, y_predicted))

    # --- Last Known Price ---
    yesterday_price = float(final_df["close"].iloc[-1])

    # --- Recursive Multi-Step Prediction (Next 5 trading days) ---
    last_100_days = final_df[-100:].values
    last_100_days_scaled = scaler.transform(last_100_days)

    def predict_multiple_days(model, input_sequence, scaler, days):
        temp_input = input_sequence.copy()
        predictions = []
        for _ in range(days):
            X_input = np.array([temp_input[-100:]])
            pred_scaled = model.predict(X_input)
            pred_price = scaler.inverse_transform(pred_scaled)[0][0]
            predictions.append(float(pred_price))
            temp_input = np.append(temp_input, [[pred_scaled[0][0]]], axis=0)
        return predictions

    next_week_prices = predict_multiple_days(model, last_100_days_scaled, scaler, 5)
    next_day_price = next_week_prices[0]

    # --- Plot Next Week ---
    plt.figure(figsize=(10, 5))
    plt.plot(
        range(1, 6),
        next_week_prices,
        marker="o",
        linestyle="-",
        color="orange",
    )
    plt.title(f"Predicted Price upto Next Week of {ticker}")
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.grid(True)
    plt.xticks(range(1, 6), ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"])
    plot_next_week = save_plot(f"{ticker}_next_week.png")

    return PredictionResponse(
        status="success",
        plot_img=plot_img,
        plot_100_dma=plot_100_dma,
        plot_200_dma=plot_200_dma,
        plot_prediction=plot_prediction,
        mse=mse,
        rmse=rmse,
        r2=r2,
        yesterday_price=yesterday_price,
        predicted_price=next_day_price,
        next_week_prices=next_week_prices,
        plot_next_week=plot_next_week,
    )
