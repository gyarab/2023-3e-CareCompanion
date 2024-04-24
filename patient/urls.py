from django.urls import path
from . import views

urlpatterns = [
    # Home klienta
    path('', views.index, name='index_patient'),
    # Seznam opatrovníku a jejich směny
    path('seznam-opatrovniku/', views.caregivers_list, name='caregivers_list'),
    # Zobrazení kontaktů na blízké
    path('kontakty/', views.contacts, name='contacts'),
    # Rozvrhy dnů
    path('rozvrh-dne/', views.day_schedule, name='day_schedule'),
]
