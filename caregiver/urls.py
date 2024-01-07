from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_caregiver'),
    path('/karty-pacientu', views.medical_cards, name='medical_cards'),
    path('/rozvrh-smeny', views.shift_schedule, name='shift_schedule'),
    path('/mapa-pokoju', views.floor_map, name='floor_map'),
    path('/prirucka', views.manual, name='manual'),
]
