from django.core.management.base import BaseCommand

from clients.seed import seed_clients, seed_vehicles
from products.seed import seed_catalog


class Command(BaseCommand):
    help = "Aliementado o banco com dados via CSV"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando seed...")

        seed_clients()
        self.stdout.write(self.style.SUCCESS("Clientes importados"))

        seed_vehicles()
        self.stdout.write(self.style.SUCCESS("Veiculos importados"))

        seed_catalog()
        self.stdout.write(self.style.SUCCESS("Produtos/Serviços importados"))

        self.stdout.write(self.style.SUCCESS("Seed finalizado!"))
