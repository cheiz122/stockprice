from django.db import models

# Create your models here.
###  open=models.CharField(('Open'),max_length=255)
   # high=models.CharField(('High'),max_length=255)
    #low=models.CharField(('Low'),max_length=255)
    #close=models.CharField(('Close'),max_length=255) 
    #volume=models.CharField(('Volume'),max_length=255)

from django.db import models

#
class StockPrice(models.Model):
    symbol = models.CharField(max_length=10)  # Symbol of the stock, e.g., "IBM"
    date = models.DateTimeField()  # DateTimeField for date and time

    open = models.FloatField()  # FloatField for open price
    high = models.FloatField()  # FloatField for high price
    low = models.FloatField()   # FloatField for low price
    close = models.FloatField() # FloatField for close price
    volume = models.PositiveIntegerField()  # PositiveIntegerField for volume (assuming it's a non-negative integer)

    def __str__(self):   
        return f"{self.symbol} - {self.timestamp}"    

class load_lstm(models.Model):
    symbol = models.CharField(max_length=10)
    model_path = models.CharField(max_length=255)
    def __str__(self):
        return self.symbol 

class LastLoadedDate(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    last_loaded_date = models.DateTimeField() 

    def __str__(self):
        return self.symbol
     