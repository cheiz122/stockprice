import os
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from .models import StockPrice,Load_LSTM
from django_pandas.io import read_frame
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from keras.models import model_from_json
from django.core.serializers import serialize
from django.http import JsonResponse
from keras.models import load_model
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignupForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Print out form errors to debug
            print(form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@csrf_exempt
@api_view(['GET', 'POST']) 
def predict_future(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('payload')
            symbol = request.data.get('symbol').upper() # Get stock symbol from request
            period = int(request.data.get('period',))
            print(symbol)
            print(period)
            test_data = np.array(input_data)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            #model_path = os.path.join(BASE_DIR, 'staticfiles', 'models', 'keras.h5')
            saved_model = Load_LSTM.objects.get(model_name=symbol)
            model = load_model(saved_model.model_file.path)
            scaler = MinMaxScaler()  
            predicted_prices = []
            last_window = test_data[-100:]
          
            for _ in range(period):
                last_window_reshaped = last_window.reshape(1, 100)
                print("Last Window Reshaped Shape:", last_window_reshaped.shape)
                prediction = model.predict(last_window_reshaped)
               # print("Prediction:", prediction) 
                predicted_prices.append(prediction[0][0])
                last_window = np.append(last_window[1:], prediction[0][0])

            #predicted_prices = scaler.inverse_transform((predicted_prices).reshape(-1, 1))
            return Response({'predicted_prices': predicted_prices})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
@api_view(['GET'])
def get_stock_data(request, symbol):
    try:
        stock_data_queryset = StockPrice.objects.filter(symbol=symbol)
        stock_data_df = read_frame(stock_data_queryset)
        return requests.Response({"data": stock_data_df.to_dict(orient='records')})
    except Exception as e:
        return Response({"error": str(e)})

def streamlit_redirect(request):
    # Redirect to the Streamlit app URL
    return HttpResponseRedirect("http://localhost:8501")

def about(request):
    return render(request, 'about.html')
def home(request):
    api_key = 'YOUR_API_KEY'
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'NEWS_SENTIMENT',
        'apikey': api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        data = response.json()

        context = {
            'news_sentiment_data': data
        }

        return render(request, 'home.html', context)
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data: {str(e)}"
        return render(request, 'error.html', {'error_message': error_message})
    except Exception as ex:
        error_message = f"An unexpected error occurred: {str(ex)}"
        return render(request, 'error.html', {'error_message': error_message})

@csrf_exempt
@api_view(['GET', 'POST']) 
def predict(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('data')
            if input_data is None:
                return JsonResponse({'error': 'No input data provided'}, status=400)

            input_data = [0 if x is None else x for x in input_data]  # Replace None with 0
            input_data = np.array(input_data)
            
            if input_data.size == 0:
                return JsonResponse({'error': 'Input data is empty'}, status=400)

            symbol = request.data.get('symbol').upper()
            print("Received symbol:", symbol)
            saved_model = Load_LSTM.objects.get(model_name=symbol)
            model = load_model(saved_model.model_file.path)

            # Perform prediction
            predictions = model.predict(input_data)
            
            return JsonResponse({'predictions': predictions.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

          