# Import necessary Django modules for URL routing
from django.contrib import admin
from django.urls import path
from . import views  # Import views from the current app
from django.contrib.auth.views import LogoutView  # Built-in logout view

# Define URL patterns for the application
urlpatterns = [
    # User authentication and registration routes
    path('register', views.register, name='register'),  # User registration page
    path('logout/', views.logout, name='logout'),  # User logout functionality
    path('authenticate', views.authenticate_user, name="authenticate_user"),  # Handle user authentication

    # Main navigation routes
    path('', views.login, name='login'),  # Login page (default landing page)
    path('home/', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page

    # Redirect to external Streamlit dashboard
    path('streamlit/', views.streamlit_redirect, name='streamlit_redirect'),

    # API endpoints for stock price prediction
    path('api/predict/', views.predict, name='predict'),  # Predict stock prices using LSTM model
    path('api/get_stock_data/<str:symbol>/', views.get_stock_data, name='get_stock_data'),  # Get stock data from api sent by streamlit
    path('api/predict_future/', views.predict_future, name='predict_future'),  # Future price prediction endpoint
]
