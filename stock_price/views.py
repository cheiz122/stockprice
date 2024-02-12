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
@csrf_exempt
@api_view(['GET', 'POST']) 
def predict_future(request):
    if request.method == 'POST':
        try:
            input_data = request.data.get('payload')
            test_data = np.array(input_data)
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(BASE_DIR, 'staticfiles', 'models', 'keras.h5')
            model = load_model(model_path)
            scaler = MinMaxScaler()  
            predicted_prices = []
            last_window = test_data[-100:]
          
            for _ in range(30):
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
'''        
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
            

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(BASE_DIR, 'staticfiles', 'models', 'keras.h5')
            model = load_model(model_path)

            predictions = model.predict(input_data)
            return JsonResponse({'predictions': predictions.tolist()})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)  '''

    
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

            symbol = request.data.get('symbol')
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

          