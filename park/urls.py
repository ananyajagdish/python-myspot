from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book/', views.create, name='create-booking'),
    path('book/detail/<int:id>/', views.detail, name='detail-booking'),
    path('book/park/<int:id>/', views.park, name='park'),
    path('book/exit/<int:id>/', views.exit, name='exit'),
    path('book/edit/<int:id>/', views.edit, name='edit-booking'),
    path('book/cancel/<int:id>/', views.cancel, name='cancel-booking'),
    path('vehicle/', views.add_vehicle, name='add-vehicle'),
    path('vehicle/remove/<int:id>/', views.remove_vehicle, name='remove-vehicle'),
    path('book/selectvehicle/', views.select_vehicle, name='select-vehicle'),
    path('book/selectgarage/', views.select_garage, name='select-garage'),
]
