from django.core.management.base import BaseCommand
import requests
from datetime import datetime, timezone
from stock_price.models import StockPrice, LastLoadedDate
import pytz
from django.core.exceptions import ObjectDoesNotExist
class Command(BaseCommand):
    help = 'Fetch and save historical stock data'

    def handle(self, *args, **options):
        url = "https://www.alphavantage.co/query"
        api_key = "GF9IGY262QOKWTLV"  
        company_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'IBM']
        interval='60min'
        end_date = datetime.now(pytz.utc).date()
        for symbol in company_symbols:
            try:
                last_loaded_date_obj = LastLoadedDate.objects.get(
                symbol=symbol,
                
            )
                start_date = last_loaded_date_obj
            except ObjectDoesNotExist:
               print("LastLoadedDate matching query does not exist.")
               new_last_loaded_date = LastLoadedDate.objects.create(
               symbol=symbol,
               last_loaded_date=datetime(2023, 10, 1, tzinfo=pytz.utc)
               )
        
        
               last_loaded_date_obj = new_last_loaded_date
               start_date = last_loaded_date_obj.last_loaded_date 
                
            if start_date == end_date:
                self.stdout.write(self.style.SUCCESS(f'Data for {symbol} is up to date.'))
                continue  
                response = requests.get(url, params=params)
            data = requests.Response.json()

            if "Time Series (Daily)" in data:
                daily_data = data["Time Series (Daily)"]

        # Iterate through the data and save it to the database
                for date, price_data in daily_data.items():
                    if date >= start_date:
                        timestamp = datetime.strptime(date, "%Y-%m-%d")
                        open_price = float(price_data["1. open"])
                        close_price = float(price_data["4. close"])
                        high_price = float(price_data["2. high"])
                        low_price = float(price_data["3. low"])
                        volume = int(price_data["5. volume"])

                        StockPrice.objects.create(
                        symbol=symbol,
                        date=timestamp,
                        open=open_price,
                        close=close_price,
                        high=high_price,
                        low=low_price,
                        volume=volume,
                    )
       
                
                
                last_loaded_date_obj.last_loaded_date = end_date
                last_loaded_date_obj.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully fetched and saved data for {symbol}'))
            else:
                self.stdout.write(self.style.WARNING(f'No data found for {symbol}'))

