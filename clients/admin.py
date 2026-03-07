from django.contrib import admin

from .models import Client, Vehicle

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('client', 'vehicle_brand', 'vehicle_model', 'vehicle_year')
