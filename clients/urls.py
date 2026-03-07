from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('list/clients/', views.ListClientsView.as_view(), name='list_clients'),
    path('list/vehicles/', views.ListVehiclesView.as_view(), name='list_vehicles'),
    path('client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
]