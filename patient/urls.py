from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_patient'),
    path('/seznam-opatrovniku', views.caregivers_list, name='caregivers_list'),
    path('/kontakty', views.contacts, name='contacts'),
    path('/rozvrh-dne', views.day_schedule, name='day_schedule'),
]
