from django.core.management.base import BaseCommand
from stock_price.models import StockPrice,load_lstm  # Import any necessary functions or modules
from django.core.management import call_command
class Command(BaseCommand):
    help = 'Perform setup tasks for your app'

    def handle(self, *args, **options):
        # Your setup logic here
        call_command('makemigrations')
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS('Setup tasks completed successfully'))
