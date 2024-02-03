from django.core.management.base import BaseCommand
from stock_price.models import load_lstm
from tensorflow import keras

class Command(BaseCommand):
    '''
    help = 'Load the trained LSTM model into the database'

    def handle(self, *args, **options):
        # Define the path to the saved model in your Jupyter Notebook
        model_path = 'ibm.h5'

        symbol = 'IBM'  # Replace with the relevant stock symbol

        try:
            # Create a StockPricePredictionModel instance and save it to the database
            model_instance = load_lstm(symbol=symbol, model_path=model_path)
            model_instance.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded model for {symbol} into the database.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))'''

    def handle(self,*args,**options):
    
        model_path = 'ibm.h5'

        symbol = 'IBM'  # Replace with the relevant stock symbol

        try:
            # Create a StockPricePredictionModel instance and save it to the database
            model_instance = load_lstm(symbol=symbol, model_path=model_path)
            model_instance.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded model for {symbol} into the database.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {str(e)}'))