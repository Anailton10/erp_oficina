import re

from django import forms

from .models import Client, Vehicle


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone_number"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-secondary",
                    "placeholder": "Nome completo",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control bg-dark text-light border-secondary",
                    "placeholder": "(00) 0-0000-0000",
                    "maxlength": "11",
                }
            ),
        }
        labels = {
            "name": "Nome",
            "phone_number": "Telefone",
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        pattern = r"[0-9]{11}"
        if not re.fullmatch(pattern, str(phone_number)):
            raise forms.ValidationError("Número de telefone fora do padrão")

        if (
            Client.objects.filter(phone_number=phone_number)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Número de telefone já pertence a um usuário.")

        return phone_number


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["vehicle_brand", "vehicle_model", "vehicle_year", "plate"]
        widgets = {
            "vehicle_brand": forms.TextInput(
                attrs={"class": "form-control bg-dark text-light border-secondary"}
            ),
            "vehicle_model": forms.TextInput(
                attrs={"class": "form-control bg-dark text-light border-secondary"}
            ),
            "vehicle_year": forms.NumberInput(
                attrs={
                    "class": "form-control bg-dark text-light border-secondary",
                    "min": "1900",
                }
            ),
            "plate": forms.TextInput(
                attrs={"class": "form-control bg-dark text-light border-secondary"}
            ),
        }
        labels = {
            "vehicle_brand": "Marca",
            "vehicle_model": "Modelo",
            "vehicle_year": "Ano",
            "plate": "Placa",
        }

    def clean_plate(self):
        plate = str(self.cleaned_data.get("plate")).upper().strip()

        pattern_mercosul = re.fullmatch(r"[A-Z]{3}[0-9][A-Z][0-9]{2}", plate)
        pattern_gray = re.fullmatch(r"[A-Z]{3}[0-9]{4}", plate)
        if not pattern_gray and not pattern_mercosul:
            raise forms.ValidationError("Placa fora do padrão")

        if Vehicle.objects.filter(plate=plate).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Placa já pertence a um veículo.")

        return plate
