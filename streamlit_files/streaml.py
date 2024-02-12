import requests
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from plotly import graph_objs as go
import yfinance as yf
from datetime import datetime

@st.cache
def fetch_stock_data(symbol):
    start_date = "2015-01-01"
    end_date = datetime.now().strftime('%Y-%m-%d')
    df = yf.download(symbol, start=start_date, end=end_date)
    df = df.reset_index()
    return df
def predict_future_prices(test_data):
    payload = {'payload': test_data.tolist()}
    response = requests.post('http://localhost:8000/api/predict_future/', json=payload)
    if response.status_code == 200:
        predicted_prices = response.json()['predicted_prices']
        return predicted_prices
    else:
        st.error("Error occurred while fetching future predictions")
        return None

def predict(input_data,symbol):
    url = 'http://localhost:8000/api/predict/'
    #print("Data type of input_data:", type(x_test))
    input_data_list = input_data.tolist()
    print(symbol)
    data = {"data": input_data_list,"symbol":symbol}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        predictions = response.json().get('predictions')
        return np.array(predictions) if predictions else None
    else:
        st.error(f"Error: {response.status_code}, {response.text}")
        return None
def main():
    st.title("Stock Price Predictions")

    # Get user input for stock symbol
    symbol = st.text_input("Enter stock symbol:", 'AAPL')
    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365

    if st.button("Fetch Data"):
        try:
            # Make an HTTP request to fetch stock data
            df = fetch_stock_data(symbol)

            # Display summary statistics and stock data
            st.write(df.describe())
            st.write("First 5 rows:")
            st.write(df.head())
            st.write("Last 5 rows:")
            st.write(df.tail())

            def visualization():
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], mode='lines', name='Open'))
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close'))
                fig.update_layout(title='Open vs Close Prices', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=True)
                fig.update_layout(xaxis_rangeslider_visible=True)
                st.plotly_chart(fig)

            visualization()

            # Preprocess data for LSTM model
            scaler = MinMaxScaler(feature_range=(0,1))
            scaled_data = scaler.fit_transform(df[['Close']])

            # Split data into training and testing sets
            train_data = scaled_data[:int(len(df)*0.80)]
            test_data = scaled_data[int(len(df)*0.80) - 100:]

            # Prepare testing data
            x_test = []
            y_test = []
            for i in range(100, len(test_data)):
                x_test.append(test_data[i-100:i, 0])
                y_test.append(test_data[i, 0])
            x_test, y_test = np.array(x_test), np.array(y_test)
            predictions = predict(x_test,symbol)
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1))
            future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=30, freq='D')
            predicted_prices = predict_future_prices(test_data)

            if predictions is not None:
                predictions = scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Original'))
                fig.add_trace(go.Scatter(x=df['Date'].iloc[-len(y_test):], y=y_test.flatten(), mode='lines', name='Actual'))
                fig.add_trace(go.Scatter(x=df['Date'].iloc[-len(predictions):], y=predictions.flatten(), mode='lines', name='Predicted'))
                fig.update_layout(xaxis_rangeslider_visible=True)

                st.plotly_chart(fig)
            else:
                st.error("Failed to get predictions from the API")
            if predicted_prices:
                predicted_prices = np.array(predicted_prices)
                predicted_prices = scaler.inverse_transform((predicted_prices).reshape(-1, 1))
                future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.Timedelta(days=1), periods=30, freq='D')
                fig_predicted_prices = go.Figure()
                fig_predicted_prices.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Actual'))
                fig_predicted_prices.add_trace(go.Scatter(x=future_dates, y=predicted_prices.flatten(), mode='lines', name='Predicted - Future', line=dict(dash='dot')))
                fig_predicted_prices.update_layout(title='Predicted Prices', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=True)
                st.plotly_chart(fig_predicted_prices)
    
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
