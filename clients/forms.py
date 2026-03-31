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

        if Client.objects.filter(phone_number=phone_number).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError("Numero de telefone já pertence a um usuário.")

        return phone_number


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["vehicle_brand", "vehicle_model", "vehicle_year", "plate"]

    def clean_plate(self):
        plate = str(self.cleaned_data.get("plate")).upper().strip()

        pattern_mercosul = re.fullmatch(
            pattern=r"[A-Z]{3}[0-9][A-Z][0-9]{2}", string=plate
        )
        pattern_gray = re.fullmatch(pattern=r"([A-Z]{3})[0-9]{4}", string=plate)
        if not pattern_gray and not pattern_mercosul:
            raise forms.ValidationError("Placa fora do padrão")

        if Vehicle.objects.filter(plate=plate).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Placa já pertence a um veiculo.")

        return plate
