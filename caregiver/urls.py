from django.urls import path
from . import views

urlpatterns = [
    # Home opatrovníka
    path('', views.index, name='index_caregiver'),
    # Zdravotní karty všech klientů
    path('karty-klientu/', views.medical_cards, name='medical_cards'),
    # Jedna konkrétní karta klienta
    path('karty-klientu/<str:full_name_of_patient>/', views.patient_info, name='patient_info'),
    # Rozvrhy dne všech klientů
    path('rozvrhy-klientu/', views.patient_schedules, name='patient_schedules'),
    # Úprava rozvrhu konkrétního klienta
    path('rozvrhy-klientu/<int:pk>/', views.edit_patient_schedules, name='edit_patient_schedules'),
    # Směny přihlášeného opatrovníka
    path('rozvrh-smeny/', views.shift_schedule, name='shift_schedule'),
    # Příručka
    path('prirucka/', views.manual, name='manual'),
    path('prirucka/co-delat/', views.what_to_do, name='what_to_do'),
    path('prirucka/aktivity/', views.free_time_activities, name='free_time_activities'),
    path('prirucka/rozsirte-znalosti/', views.education, name='education'),
]
