from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import requests
from sklearn.preprocessing import MinMaxScaler
from .models import StockPrice, Load_LSTM,login1
from django_pandas.io import read_frame
from rest_framework.decorators import api_view
from rest_framework.response import Response
from keras.models import model_from_json, load_model
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import loginform
from django.template import loader
from django.http import HttpResponse
def login(request):
    return render(request, 'login.html')
def logout(request):
    return redirect('login')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import login1  # Assuming 'login1' is your model

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f"Login successful. Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    else:
        return redirect('login')
def page(request):
    
    return render(request,'register.html')
    
def register(request):
	if request.method == 'POST':
		form = loginform(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
            #user1=User(username=username,password=password)
			login1(request, user)
			messages.success(request, f"You Have Successfully Registered! Welcome!")
			return render(request,'login.html')
	else:
		form = loginform()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

@csrf_exempt
@api_view(['GET', 'POST']) 
def predict_future(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('payload')
            symbol = request.data.get('symbol').upper()  # Get stock symbol from request
            period = int(request.data.get('period', 1))  # Default period to 1 if not provided
            n_points = int(request.data.get('n_points', 1))  # Default n_points to 1 if not provided

            test_data = np.array(input_data)
            # Load your LSTM model
            saved_model = Load_LSTM.objects.get(model_name=symbol)
            model = load_model(saved_model.model_file.path)

            predicted_prices = []
            last_window = test_data[-n_points:]
            for _ in range(period):
                last_window_reshaped = last_window.reshape(1, n_points)
                prediction = model.predict(last_window_reshaped)
                predicted_prices.append(prediction[0][0])
                last_window = np.append(last_window[1:], prediction[0][0])
            return Response({'predicted_prices': predicted_prices})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
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

          