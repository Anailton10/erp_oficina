from django import forms

from .models import Client, Vehicle


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone_number"]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["vehicle_brand", "vehicle_model", "vehicle_year"]
