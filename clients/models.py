from django.db import models

from app.models.base import BaseModel


class Client(BaseModel):
    """
    Representa um cliente da oficina.

    O cliente pode possuir um ou mais veículos associados.
    O modelo herda de BaseModel, que fornece campos comuns
    como data de criação, data de atualização e status ativo.

    Campos:
        name (str): Nome do cliente.
        phone_number (str): Número de telefone do cliente (opcional).

    Comportamento:
        soft_delete(): Realiza uma exclusão lógica do cliente,
        marcando-o como inativo e também desativando todos os
        veículos associados.
    """

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def soft_delete(self):
        """
        Realiza a exclusão lógica do cliente.

        - Marca o cliente como inativo.
        - Marca todos os veículos associados como inativos.
        """

        # Desativa o cliente
        self.is_active = False
        self.save()

        # Desativa todos os veículos associados
        self.vehicles.update(is_active=False)

    def __str__(self):
        return self.name


class Vehicle(BaseModel):
    client = models.ForeignKey(Client, related_name='vehicles', on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    vehicle_brand = models.CharField(max_length=100, blank=True, null=True)
    vehicle_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.vehicle_brand} {self.vehicle_model} ({self.vehicle_year})"

