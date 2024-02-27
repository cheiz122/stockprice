from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

 path('register',views.register,name='register'),
    
#path('',views.run_streamlit_app,name='run_streamlit_app'),
#path('admin/update-data-fetched-date/', views.update_data_fetched_date, name='update_data_fetched_date'),
    
path('', views.login, name='login'),
path('home/',views.home, name='home'), 
path('about/', views.about, name='about'),
path('streamlit/', views.streamlit_redirect, name='streamlit_redirect'),
path('api/predict/', views.predict, name='predict'),
path('api/get_stock_data/<str:symbol>/', views.get_stock_data, name='get_stock_data'),
path('api/predict_future/', views.predict_future, name='predict_future'),
]
