from django.urls import path

from . import views

urlpatterns = [
    path('create/<int:client_id>/<int:vehicle_id>/',views.OrderCreateView.as_view(),name='create_order'),
]