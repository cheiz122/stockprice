# admin.py
from django.contrib import admin
from .models import Load_LSTM

  
admin.site.register(Load_LSTM)
admin.site.site_header = "Stock price Prediction Admin"
admin.site.site_title = "Stock Price Prediction Admin Portal"
admin.site.index_title = "Welcome to Stock Price Prediction Portal"


'''
import os
from django.contrib import admin
from django import forms
from .models import load_lstm
from keras.models import load_model

class SavedModelForm(forms.ModelForm):
    class Meta:
        model = load_lstm
        fields = '__all__'

    def clean_path(self):
        path = self.cleaned_data['path']
        if not os.path.exists(path):
            raise forms.ValidationError("The specified path does not exist.")
        if not os.path.isdir(path):
            raise forms.ValidationError("The specified path is not a directory.")

        directory_path, file_name = os.path.split(path)
        if file_name not in os.listdir(directory_path):
            raise forms.ValidationError(f"No file named '{file_name}' found in the specified directory.")

        return path

class SavedModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'path')
    search_fields = ('name', 'description')
    form = SavedModelForm

    def add_model(self, request, queryset):
        return super().add_view(request)

    add_model.short_description = "Add New Model"

    def delete_model(self, request, queryset):
        for obj in queryset:
            obj.delete()
        self.message_user(request, "Selected model(s) deleted successfully.")
    
    delete_model.short_description = "Delete Selected Model(s)"

admin.site.register(load_lstm, SavedModelAdmin)'''