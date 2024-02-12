import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import streamlit as st

# Function to fetch and preprocess data
def fetch_and_preprocess_data(stock_symbol, start_date, end_date, test_split=0.2):
    # Fetch data from Yahoo Finance API
    df = yf.download(stock_symbol, start=start_date, end=end_date)
    df = df.reset_index()

    # Feature Engineering: Calculate Simple Moving Average (SMA)
    window = 20
    df['SMA'] = df['Close'].rolling(window=window).mean()

    # Split data into training and testing sets
    train_size = int(len(df) * (1 - test_split))
    train_data = df[:train_size]
    test_data = df[train_size:]

    # Scaling data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_train_data = scaler.fit_transform(train_data[['Close', 'SMA']])
    scaled_test_data = scaler.transform(test_data[['Close', 'SMA']])

    return scaled_train_data, scaled_test_data, scaler, train_data, test_data

# Function to prepare training and validation sets
def prepare_data(data, window):
    x, y = [], []
    for i in range(window, len(data)):
        x.append(data[i-window:i])
        y.append(data[i, 0])
    return np.array(x), np.array(y)

# Function to build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60, activation='relu', return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(units=80, activation='relu', return_sequences=True))
    model.add(Dropout(0.4))
    model.add(LSTM(units=120, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Function to visualize training history
def plot_training_history(history):
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Training History')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    st.pyplot()

# Function to evaluate model performance
def evaluate_model(model, x_val, y_val, scaler):
    predictions = model.predict(x_val)
    predictions = scaler.inverse_transform(np.concatenate((np.zeros((window, 1)), predictions), axis=0))[:, 0]
    y_val = scaler.inverse_transform(np.concatenate((np.zeros((window, 1)), y_val[:, None]), axis=0))[:, 0]

    mse = mean_squared_error(y_val, predictions)
    mae = mean_absolute_error(y_val, predictions)
    rmse = np.sqrt(mse)

    return mse, mae, rmse

# Main function
def main():
    st.title('Stock Price Prediction')
    stock_symbol = "TSLA"
    start_date = "2010-01-01"
    end_date = "2024-01-01"
    test_split = 0.2

    try:
        # Fetch and preprocess data
        scaled_train_data, scaled_test_data, scaler, train_data, test_data = fetch_and_preprocess_data(stock_symbol, start_date, end_date, test_split)

        # Prepare training and validation sets
        window = 100
        x_train, y_train = prepare_data(scaled_train_data, window)
        x_val, y_val = prepare_data(scaled_test_data, window)

        # Build and train LSTM model
        input_shape = (x_train.shape[1], x_train.shape[2])
        model = build_lstm_model(input_shape)
        history = model.fit(x_train, y_train, epochs=50, validation_data=(x_val, y_val), shuffle=False, verbose=1)

        # Visualize training history
        plot_training_history(history)

        # Evaluate model performance
        mse, mae, rmse = evaluate_model(model, x_val, y_val, scaler)

        # Display evaluation metrics
        st.subheader("Validation Metrics:")
        st.write("Mean Squared Error (MSE):", mse)
        st.write("Mean Absolute Error (MAE):", mae)
        st.write("Root Mean Squared Error (RMSE):", rmse)

    except Exception as e:
        st.error("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
