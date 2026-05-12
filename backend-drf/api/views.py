from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import NepsePredictionSerializer
from rest_framework import status
from rest_framework.response import Response
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from .utils import save_plot
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

BASE_DIR = Path(__file__).resolve().parents[1].parent

class NepsePredictionAPIView(APIView):
    def post(self, request):
        serializer = NepsePredictionSerializer(data=request.data)
        if serializer.is_valid():
            ticker = serializer.validated_data['ticker']

            # --- Load CSV data ---
            now = datetime.now()
            start = datetime(now.year - 10, now.month, now.day)
            end = now
            csv_path = BASE_DIR / "Resources" / "data" / f"{ticker}.csv"
            if not csv_path.exists():
                return Response(
                    {"error": f"No data file found for ticker '{ticker}'."},
                    status=status.HTTP_404_NOT_FOUND
                )

            df = pd.read_csv(csv_path)
            if df.empty:
                return Response({"error": "No data found for the given ticker."}, status=status.HTTP_400_BAD_REQUEST)

            df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
            df = df[(df['published_date'] >= start) & (df['published_date'] <= end)]
            df = df.drop(columns=['per_change','traded_amount','status'], errors='ignore').reset_index(drop=True)

            # --- Historical Closing Price Plot ---
            plt.switch_backend('AGG')
            plt.figure(figsize=(12,5))
            plt.plot(df.close, label='Closing Price')
            plt.title(f'Closing Price of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Close Price')
            plt.legend()
            plot_img = save_plot(f'{ticker}_plot.png')

            # --- 100-day Moving Average ---
            ma100 = df.close.rolling(100).mean()
            plt.figure(figsize=(12,5))
            plt.plot(df.close, label='Closing Price')
            plt.plot(ma100, 'r', label='100 DMA')
            plt.title(f'100-Day Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_100_dma = save_plot(f'{ticker}_100_dma.png')

            # --- 200-day Moving Average ---
            ma200 = df.close.rolling(200).mean()
            plt.figure(figsize=(12,5))
            plt.plot(df.close, label='Closing Price')
            plt.plot(ma200, 'g', label='200 DMA')
            plt.title(f'200-Day Moving Average of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_200_dma = save_plot(f'{ticker}_200_dma.png')

            # --- Split data for LSTM ---
            data_training = pd.DataFrame(df.close[0:int(len(df)*0.7)])
            data_testing = pd.DataFrame(df.close[int(len(df)*0.7):])

            scaler = MinMaxScaler(feature_range=(0,1))
            model = load_model('stock_prediction_model.keras')

            past_100_days = data_training.tail(100)
            final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
            input_data = scaler.fit_transform(final_df)

            # --- Prepare test data ---
            x_test, y_test = [], []
            for i in range(100, input_data.shape[0]):
                x_test.append(input_data[i-100:i])
                y_test.append(input_data[i,0])
            x_test, y_test = np.array(x_test), np.array(y_test)

            # --- Predict on test data ---
            y_predicted = model.predict(x_test)
            y_predicted = scaler.inverse_transform(y_predicted.reshape(-1,1)).flatten()
            y_test = scaler.inverse_transform(y_test.reshape(-1,1)).flatten()

            # --- Final Prediction Plot ---
            plt.figure(figsize=(12,5))
            plt.plot(y_test, 'b', label='Original Price')
            plt.plot(y_predicted, 'r', label='Predicted Price')
            plt.title(f'Final Prediction of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.legend()
            plot_prediction = save_plot(f'{ticker}_final_prediction.png')

            # --- Model Evaluation ---
            mse = mean_squared_error(y_test, y_predicted)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_predicted)

            # --- Last Known Price (Yesterday) ---
            yesterday_price = final_df['close'].iloc[-1]

            # --- Recursive Multi-Step Prediction for Next Week (5 days) ---
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
            next_day_price = next_week_prices[0]  # predicted next day

            # --- Plot Next Week ---
            plt.figure(figsize=(10,5))
            plt.plot(range(1,6), next_week_prices, marker='o', linestyle='-', color='orange')
            plt.title(f'Predicted Price upto Next Week of {ticker}')
            plt.xlabel('Days')
            plt.ylabel('Price')
            plt.grid(True)
            plt.xticks(range(1,6), ['Day 1','Day 2','Day 3','Day 4','Day 5'])
            plot_next_week = save_plot(f'{ticker}_next_week.png')
            

            # --- Return Response ---
            return Response({
                'status': 'success',
                'plot_img': plot_img,
                'plot_100_dma': plot_100_dma,
                'plot_200_dma': plot_200_dma,
                'plot_prediction': plot_prediction,
                'mse': mse,
                'rmse': rmse,
                'r2': r2,
                'yesterday_price': float(yesterday_price),
                'predicted_price': float(next_day_price),
                'next_week_prices': next_week_prices,
                'plot_next_week': plot_next_week,
            })
