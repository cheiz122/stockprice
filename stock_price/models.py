from django.db import models

# Model to store stock price data
class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)  # Stock symbol (e.g., "IBM")
    date = models.DateTimeField()  # Timestamp for the stock price record

    open = models.FloatField()  # Opening price of the stock
    high = models.FloatField()  # Highest price during the period
    low = models.FloatField()   # Lowest price during the period
    close = models.FloatField() # Closing price of the stock
    volume = models.PositiveIntegerField()  # Number of shares traded (must be non-negative)

    def __str__(self):   
        return f"{self.symbol} - {self.date}"  # Corrected from "timestamp" to "date"

# Model to store pre-trained LSTM models for stock price prediction
class Load_LSTM(models.Model):
    model_name = models.CharField(max_length=100, unique=True)  # Unique name for the model
    model_file = models.FileField(upload_to='pretrained_models/')  # File field to store the model
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the model is uploaded

    def __str__(self):
        return self.model_name  

# Model to track the last date stock data was loaded for a specific stock symbol
class LastLoadedDate(models.Model):
    symbol = models.CharField(max_length=10, unique=True)  # Stock symbol (e.g., "AAPL")
    last_loaded_date = models.DateTimeField()  # Last date stock data was loaded

    def __str__(self):
        return self.symbol

# User authentication model (Not recommended, use Django's built-in User model instead)
class login1(models.Model):
    username = models.CharField(max_length=50)  # Username for login
    password1 = models.CharField(max_length=50)  # Password (should be securely hashed, use Django's User model)
    password2 = models.CharField(max_length=50)  # Confirm password (should be securely hashed)

# Model to store user names
class name(models.Model):
    first_name = models.CharField(max_length=70)  # User's first name
    last_name = models.CharField(max_length=50)   # User's last name
