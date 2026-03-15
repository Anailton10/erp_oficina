from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('list/clients/', views.ListClientsView.as_view(), name='clients_list'),
    path('list/vehicles/', views.ListVehiclesView.as_view(), name='vehicles_list'),
    path('detail/client/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('detail/vehicle/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('create/client/', views.CreateClientView.as_view(), name='client_create'),
    path('create/vehicle/<int:client_id>/', views.CreateVehicleView.as_view(), name='vehicle_create'),
    path('update/client/<int:pk>/', views.UpdateClientView.as_view(), name='client_update'),
    path('update/vehicle/<int:pk>/', views.UpdateVehicleView.as_view(), name='vehicle_update'),
    path('delete/client/<int:pk>/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('delete/vehicle/<int:vehicle_id>/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
]