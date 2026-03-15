from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('list/clients/', views.ListClientsView.as_view(), name='list_clients'),
    path('list/vehicles/', views.ListVehiclesView.as_view(), name='list_vehicles'),
    path('detail/client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('detail/vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('create/client/', views.CreateClientView.as_view(), name='create_client'),
    path('create/vehicle/<int:client_id>/', views.CreateVehicleView.as_view(), name='create_vehicle'),
    path('delete/client/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('delete/vehicle/<int:vehicle_id>/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
]