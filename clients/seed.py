import csv
from pathlib import Path

from .models import Client, Vehicle


def seed_clients():
    file_path = Path(__file__).resolve().parent / "clients.csv"

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            Client.objects.update_or_create(
                name=row["name"],
                defaults={
                    "phone_number": row.get("phone_number")
                }
            )


def seed_vehicles():
    file_path = Path(__file__).resolve().parent / "vehicles.csv"

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            client_name = row["client_name"]

            client, _ = Client.objects.get_or_create(
                name=client_name
            )

            Vehicle.objects.update_or_create(
                client=client,
                vehicle_model=row.get("vehicle_model"),
                vehicle_brand=row.get("vehicle_brand"),
                vehicle_year=row.get("vehicle_year"),
                defaults={}
            )