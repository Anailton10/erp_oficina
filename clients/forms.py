import re

from django import forms

from .models import Client, Vehicle


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone_number"]

    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "maxlength": "11",
                "placeholder": "(00) 0-0000-0000",
            }
        )
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        pattern = r"[0-9]{11}"
        x = re.fullmatch(pattern, str(phone_number))
        if not x:
            raise forms.ValidationError("Numero de tefefone fora do padrão")
        return phone_number


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["vehicle_brand", "vehicle_model", "vehicle_year"]
