# Import necessary Django modules
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template import loader
from django_pandas.io import read_frame
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import external libraries
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from keras.models import model_from_json, load_model
import os

# Import models and forms from the app
from .models import StockPrice, Load_LSTM, login1  # Ensure models are correctly defined
from .forms import loginform


# View function for rendering the login page
def login(request):
    return render(request, 'login.html')


# View function for logging out users and redirecting to the login page
def logout(request):
    return redirect('login')


# View function for handling user authentication
def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username from request
        password = request.POST.get('password')  # Get password from request
        user = authenticate(request, username=username, password=password)  # Authenticate user

        if user is not None:
            messages.success(request, f"Login successful. Welcome, {username}!")
            return redirect('home')  # Redirect to home page on success
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to login on failure
    else:
        return redirect('login')  # Redirect to login page if request is not POST


# View function for rendering the registration page
def page(request):
    return render(request, 'register.html')


# View function for handling user registration
def register(request):
    if request.method == 'POST':
        form = loginform(request.POST)  # Initialize form with POST data
        if form.is_valid():
            form.save()  # Save new user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)  # Authenticate newly registered user

            # Login the user
            login1(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return render(request, 'login.html')  # Redirect to login page after successful registration
    else:
        form = loginform()  # Initialize empty form
    return render(request, 'register.html', {'form': form})  # Render registration page with form


# API endpoint for predicting future stock prices using an LSTM model
@csrf_exempt  # Disable CSRF protection for this view (use carefully)
@api_view(['GET', 'POST'])
def predict_future(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('payload')  # Get input data from request
            symbol = request.data.get('symbol').upper()  # Convert stock symbol to uppercase
            period = int(request.data.get('period', 1))  # Get prediction period (default is 1)
            n_points = int(request.data.get('n_points', 1))  # Get number of points to predict (default is 1)

            test_data = np.array(input_data)  # Convert input data to NumPy array

            # Load pre-trained LSTM model
            saved_model = Load_LSTM.objects.get(model_name=symbol)
            model = load_model(saved_model.model_file.path)

            predicted_prices = []
            last_window = test_data[-n_points:]  # Select last n_points for prediction
            for _ in range(period):
                last_window_reshaped = last_window.reshape(1, n_points)
                prediction = model.predict(last_window_reshaped)
                predicted_prices.append(prediction[0][0])  # Store prediction
                last_window = np.append(last_window[1:], prediction[0][0])  # Shift window for next prediction
            
            return Response({'predicted_prices': predicted_prices})  # Return predicted prices
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Handle errors


# API endpoint for retrieving stock data from the database
@api_view(['GET'])
def get_stock_data(request, symbol):
    try:
        stock_data_queryset = StockPrice.objects.filter(symbol=symbol)  # Query stock data
        stock_data_df = read_frame(stock_data_queryset)  # Convert queryset to DataFrame
        return Response({"data": stock_data_df.to_dict(orient='records')})  # Return data as JSON
    except Exception as e:
        return Response({"error": str(e)})  # Handle errors


# Redirects the user to the Streamlit dashboard
def streamlit_redirect(request):
    return HttpResponseRedirect("http://localhost:8501")  # Redirect to Streamlit local server


# View function for rendering the 'About' page
def about(request):
    return render(request, 'about.html')


# View function for rendering the home page with stock news sentiment data
def home(request):
    api_key = 'YOUR_API_KEY'  # API key for external stock news data (replace with actual key)
    base_url = 'https://www.alphavantage.co/query'
    
    params = {
        'function': 'NEWS_SENTIMENT',
        'apikey': api_key
    }

    try:
        response = requests.get(base_url, params=params)  # Make API request
        response.raise_for_status()  # Raise an exception if the request fails
        data = response.json()  # Convert response to JSON

        context = {'news_sentiment_data': data}
        return render(request, 'home.html', context)  # Render home page with data
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})  # Handle request errors
    except Exception as ex:
        error_message = f"An unexpected error occurred: {str(ex)}"
        return render(request, 'error.html', {'error_message': error_message})  # Handle unexpected errors


# API endpoint for handling predictions
@csrf_exempt  # Disable CSRF protection (use carefully)
@api_view(['GET', 'POST'])
def predict(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('data')  # Get input data from request
            if input_data is None:
                return JsonResponse({'error': 'No input data provided'}, status=400)  # Handle missing data

            # Replace None values with 0 in input data
            input_data = [0 if x is None else x for x in input_data]
            input_data = np.array(input_data)  # Convert input data to NumPy array
            
            if input_data.size == 0:
                return JsonResponse({'error': 'Input data is empty'}, status=400)  # Handle empty input data

            symbol = request.data.get('symbol').upper()  # Get and format stock symbol
            print("Received symbol:", symbol)

            # Load pre-trained LSTM model
            saved_model = Load_LSTM.objects.get(model_name=symbol)
            model = load_model(saved_model.model_file.path)

            # Perform prediction using the loaded model
            predictions = model.predict(input_data)
            
            return JsonResponse({'predictions': predictions.tolist()})  # Return predictions as JSON
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Handle errors
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)  # Handle invalid request method
