from django.contrib import admin

from .models import Order, OrderItem

admin.site.register(Order)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'quantity', 'unit_price')


admin.site.register(OrderItem, OrderItemAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'vehicle', 'order_date', 'status', 'total')
    list_filter = ('status', 'order_date')
    search_fields = ('number', 'client__name', 'vehicle__model')  