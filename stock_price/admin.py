
from django.contrib import admin
from django.db.models import Count
from .models import StockPrice, LastLoadedDate,load_lstm
from .management.commands.api import Command
from datetime import datetime
import pytz
from django.utils.timezone import make_aware
'''
def run_stock_data_fetch(modeladmin, request, queryset):
    # Call the management command
    command = Command()
    command.handle()
    # Inform the user that the command has been executed
    modeladmin.message_user(request, "Stock data has been fetched and saved.")

run_stock_data_fetch.short_description = "Run Stock Data Fetch"

@admin.register(LastLoadedDate)
class LastLoadedDateAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'last_loaded_date']
    list_filter = ['symbol']
    actions = [run_stock_data_fetch]

    def changelist_view(self, request, extra_context=None):
        # Add a custom context variable to display the latest date data was fetched
        latest_data = LastLoadedDate.objects.latest('last_loaded_date')
        latest_data_fetched = latest_data.last_loaded_date
        return super(LastLoadedDateAdmin, self).changelist_view(request, extra_context={'latest_data_fetched': latest_data_fetched})

    def get_urls(self):
        from django.urls import path
        from .views import update_data_fetched_date
        urls = super().get_urls()
        custom_urls = [
            path('update-data-fetched-date/', self.admin_site.admin_view(update_data_fetched_date), name='update_data_fetched_date'),
        ]
        return custom_urls + urls

@admin.register(StockPrice)
class StockPriceAdmin(admin.ModelAdmin):
    list_display = ['symbol', 'date', 'open', 'close', 'high', 'low', 'volume']
    list_filter = ['symbol']

    def changelist_view(self, request, extra_context=None):
        # Add a custom context variable to display the total number of stock price records
        total_records = StockPrice.objects.count()
        return super(StockPriceAdmin, self).changelist_view(request, extra_context={'total_records': total_records})
'''
@admin.register(load_lstm)
class OtherModelAdmin(admin.ModelAdmin):
    # Define admin for other models if needed
    pass
