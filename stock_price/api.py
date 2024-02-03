import datetime
import requests
from datetime import datetime, timedelta
#from stock_price.models import StockPrice
import pytz
#replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
'''symbol='MSFT'
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=60min&apikey=GF9IGY262QOKWTLV'
r = requests.get(url)
data = r.json()
for timestamp, price_data in data["Time Series (60min)"].items():
    timestamp = datetime(2023, 10, 31, 19, 20, 0, tzinfo=pytz.UTC)

    stockprice = StockPrice(
        symbol=symbol,
        date=timestamp,
        open=float(price_data["1. open"]),
        high=float(price_data["2. high"]),
        low=float(price_data["3. low"]),
        close=float(price_data["4. close"]),
        volume=int(price_data["5. volume"])
    )
    stockprice.save() 


# Define the list of company symbols

company_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN",]

# Alpha Vantage API endpoint
url = "https://www.alphavantage.co/query"
api_key = "GF9IGY262QOKWTLV"

# API request parameters
interval = "5min"  # Set your desired interval

for symbol in company_symbols:
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval,
        "apikey": api_key,
    }

    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()

    # Iterate through the data and save it to the database
    for timestamp, price_data in data["Time Series (5min)"].items():
        timestamp = datetime(2023, 10, 30, 19, 20, 0, tzinfo=pytz.UTC)

        stockprice = StockPrice(
           symbol=symbol,
           date=timestamp,
           open=float(price_data["1. open"]),
           high=float(price_data["2. high"]),
           low=float(price_data["3. low"]),
           close=float(price_data["4. close"]),
           volume=int(price_data["5. volume"])
    )
    stockprice.save()  
        
        # Create a timezone-aware datetime using UTC
        #timestamp = timestamp.replace(tzinfo=pytz.UTC)

        # Save data to the database with the symbol
       # StockPrice.objects.create(symbol=symbol, timestamp=timestamp, price=price)''''''


       '''

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=0QUKLCWBWU46FLMF'
r = requests.get(url)
data = r.json()

print(data)
'''
company_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'IBM']

# Alpha Vantage API endpoint
url = "https://www.alphavantage.co/query"
api_key = "Your_API_Key"  # Replace with your actual API key

# Define the date range (from July of the current year to today)
current_year = datetime.now().year
start_date = f"{current_year}-07-01"
end_date = datetime.now().strftime("%Y-%m-%d")

for symbol in company_symbols:
    # Define the API request parameters
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
       # "outputsize": "full",  # Get full daily data
        "apikey": api_key,
    }

    # Make the API request
    response = requests.get(url, params=params)
    data = response.json()

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

                # Save data to the database with the symbol
                StockPrice.objects.create(
                    symbol=symbol,
                    date=timestamp,
                    open=open_price,
                    close=close_price,
                    high=high_price,
                    low=low_price,
                    volume=volume,
                )

    else:
        print(f"No data found for {symbol}")
'''