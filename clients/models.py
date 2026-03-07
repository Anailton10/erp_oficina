from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    client = models.ForeignKey(Client, related_name='vehicles', on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    vehicle_brand = models.CharField(max_length=100, blank=True, null=True)
    vehicle_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model} ({self.vehicle_year})"

