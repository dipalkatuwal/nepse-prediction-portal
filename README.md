# NEPSE Prediction Portal 📈

The **NEPSE Prediction Portal** is a full-stack web application designed to assist investors and learners in the Nepali stock market by providing real-time insights and predictive analytics. It leverages Long Short-Term Memory (LSTM) neural networks to provide technical analysis and price forecasting for various Nepalese stocks.

## 🎯 Core Objectives
The project aims to solve the lack of accessible analysis tools for the Nepali stock market through the following goals:

- **Forecasting**: Developing deep learning models using Long Short-Term Memory (LSTM) networks to provide accurate next-day and up-to-next-week stock closing price predictions.
- **Visualization**: Designing an interactive user interface (UI) to visualize historical trends, predictions, and moving averages (100-day and 200-day).
- **Security**: Implementing secure authentication and user management for personalized dashboards.

## 🚀 Key Features
- **User Authentication**: Secure registration and login system powered by JWT (JSON Web Tokens).
- **Technical Analysis**:
  - Historical Closing Price visualization.
  - 100-day and 200-day Moving Averages (DMA) to identify market trends.
- **Deep Learning Predictions**:
  - Uses a pre-trained LSTM model to predict future price movements based on historical data.
  - Visual comparison between original market prices and model-predicted prices.
  - Detailed evaluation metrics: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and R² Score.
- **Multi-Day Forecasting**:
  - Recursive multi-step prediction to forecast stock prices for the next 5 trading days.
  - Visualized 5-day price trajectory.
- **Extensive Coverage**: Support for 100+ NEPSE tickers including major banks, hydro-powers, and commercial enterprises.

## 🏗️ Technical Architecture & Tools
The system is built using a modern decoupled architecture:

- **Frontend**: Developed with **React.js (Vite)** and **Bootstrap** for a responsive, interactive user interface.
- **Backend**: Powered by **Python** and **Django REST Framework (DRF)** to serve RESTful APIs.
- **Machine Learning**: Built with **TensorFlow** and **Keras** for the LSTM models, using **Pandas** and **NumPy** for data preprocessing.
- **Authentication**: Uses **JWT (JSON Web Tokens)** to handle secure login and session management.

## 🧩 System Modules & Components
- **Prediction Engine**: Processes historical CSV data (sourced from open-source repositories like Aabishkar’s NEPSE Data), normalizes it with a `MinMaxScaler`, and generates forecasts.
- **Data Visualization**: Generates plots for closing prices, moving averages, and prediction metrics like Mean Squared Error (MSE) and R² score.
- **User Management**: Separate registration and login workflows with protected routes that only authenticated users can access.

## 📈 Methodology & Implementation
The project followed an **Agile development methodology**, ensuring iterative progress through planning, designing, implementation, and testing phases.

### Implementation Steps
Development moved from backend setup and API creation to frontend component building, followed by ML model integration and final deployment.

### Testing
- **Unit Testing**: Performed on individual components (like JWT login and model loading).
- **System Testing**: Conducted to verify end-to-end data flow between the React frontend and Django backend.

---

## 📂 Project Structure
```text
.
├── backend-drf/               # Django Backend
│   ├── accounts/             # User Authentication Logic
│   ├── api/                  # Prediction & Data Analysis API
│   ├── stock_prediction_main/# Main Configuration
│   ├── Resources/data/       # Ticker CSV datasets
│   └── stock_prediction_model.keras # Pre-trained LSTM Model
├── frontend-react/           # React Frontend
│   ├── src/
│   │   ├── components/       # UI Components (Dashboard, Login, etc.)
│   │   └── axiosinstance.js  # API Configuration
│   └── vite.config.js        # Build configuration
└── requirements.txt          # Python dependencies
```

## ⚙️ Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend-drf
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
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
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

## 📊 How it Works
The application uses a **recursive prediction strategy** for multi-day forecasting.
1. The model takes the last 100 days of stock prices as input.
2. It predicts the price for Day 1.
3. This predicted price is then appended back to the input sequence to predict Day 2, and so on for 5 days.
4. All plots are generated server-side using Matplotlib and served via static media URLs to the React frontend.


