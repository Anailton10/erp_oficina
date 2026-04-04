import csv
from decimal import Decimal
from pathlib import Path

from .models import CatalogItem


def seed_catalog():
    file_path = Path(__file__).resolve().parent / "catalog_items.csv"

    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            stock = int(row["stock"]) if row["stock"] else None
            price = Decimal(row["price"])

            CatalogItem.objects.update_or_create(
                name=row["name"],
                defaults={
                    "description": row.get("description"),
                    "price": price,
                    "stock": stock,
                    "type": row["type"],
                },
            )
