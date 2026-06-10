# Nepal Stock Prediction LSTM 📈

The **Nepal Stock Prediction LSTM** is a full-stack web application designed to assist investors and learners in the Nepali stock market by providing real-time insights and predictive analytics. It leverages Long Short-Term Memory (LSTM) neural networks for technical analysis and price forecasting across various NEPSE-listed stocks.

## 🎯 Core Objectives

- **Forecasting**: Deep learning models using LSTM networks for next-day and up-to-5-day stock closing price predictions.
- **Visualization**: Interactive UI for historical trends, predictions, and moving averages (100-day and 200-day).
- **Security**: JWT-based authentication and user management for personalized dashboards.

## 🚀 Key Features

- **User Authentication**: Secure registration and login powered by JWT (JSON Web Tokens).
- **Technical Analysis**:
  - Historical Closing Price visualization.
  - 100-day and 200-day Moving Averages (DMA) to identify market trends.
- **Deep Learning Predictions**:
  - Pre-trained LSTM model to predict future price movements based on historical data.
  - Visual comparison between original market prices and model-predicted prices.
  - Evaluation metrics: MSE, RMSE, and R² Score.
- **Multi-Day Forecasting**:
  - Recursive multi-step prediction for the next 5 trading days.
  - Visualized 5-day price trajectory.
- **Extensive Coverage**: 100+ NEPSE tickers including major banks, hydro-powers, and commercial enterprises.

## 🏗️ Technical Architecture & Tools

- **Frontend**: React.js (Vite) + Bootstrap for a responsive, interactive UI.
- **Backend**: Python + **FastAPI** serving RESTful APIs.
- **Machine Learning**: TensorFlow and Keras for LSTM models; Pandas and NumPy for data preprocessing.
- **Authentication**: JWT (JSON Web Tokens) for secure login and session management.

## 🧩 System Modules & Components

- **Prediction Engine**: Processes historical CSV data, normalizes it with `MinMaxScaler`, and generates forecasts.
- **Data Visualization**: Server-side plots (Matplotlib) for closing prices, moving averages, and metrics.
- **User Management**: Registration and login with protected routes for authenticated users.

## 📈 Methodology

The project followed an **Agile development methodology** through iterative planning, design, implementation, and testing phases.

### How Predictions Work

1. The model takes the last 100 days of stock prices as input.
2. It predicts the price for Day 1.
3. The predicted price is appended back into the input to predict Day 2 — repeated for 5 days total.
4. Plots are generated server-side via Matplotlib and served as static media URLs to the React frontend.

## 📂 Project Structure

```
.
├── backend-fastapi/           # FastAPI Backend
│   ├── accounts/             # User Authentication Logic
│   ├── api/                  # Prediction & Data Analysis API
│   ├── main.py               # FastAPI app entry point
│   ├── Resources/data/       # Ticker CSV datasets
│   └── stock_prediction_model.keras  # Pre-trained LSTM Model
├── frontend-react/            # React Frontend
│   ├── src/
│   │   ├── components/       # UI Components (Dashboard, Login, etc.)
│   │   └── axiosinstance.js  # API Configuration
│   └── vite.config.js        # Build configuration
└── requirements.txt           # Python dependencies
```

## ⚙️ Setup Instructions

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend-fastapi
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r ../requirements.txt
```

4. Set up environment variables in a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
```

5. Start the development server:

```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend-react
```

2. Install dependencies:

```bash
npm install
```

3. Create a `.env` file:

```env
VITE_BACKEND_ROOT=http://127.0.0.1:8000
```

4. Start the development server:

```bash
npm run dev
```
