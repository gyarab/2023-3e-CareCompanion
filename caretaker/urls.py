from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/karty-pacientu', views.medical_cards),
    path('/rozvrh-smeny', views.schedule),
    path('/mapa-pokoju', views.floor_map),
    path('/prirucka', views.manual),
]
