from django.contrib import admin

from .models import CatalogItem


@admin.register(CatalogItem)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "stock", "created_at")
    list_filter = ("type",)
    search_fields = ("name", "description")
