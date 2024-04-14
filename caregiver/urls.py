from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_caregiver'),
    path('karty-klientu/', views.medical_cards, name='medical_cards'),
    path('karty-klientu/<str:full_name_of_patient>/', views.patient_info, name='patient_info'),
    # path('karty-pacientu/<str:full_name_of_patient>/doktor/', views.patient_info, name='patient_info'),
    path('rozvrhy-klientu/', views.patient_schedules, name='patient_schedules'),
    path('rozvrhy-klientu/<int:pk>/', views.edit_patient_schedules, name='edit_patient_schedules'),
    path('rozvrh-smeny/', views.shift_schedule, name='shift_schedule'),
    path('prirucka/', views.manual, name='manual'),
    path('prirucka/co-delat', views.what_to_do, name='what_to_do'),
    path('prirucka/aktivity', views.activities, name='activities'),
    path('prirucka/rozsirte-znalosti', views.education, name='education'),
]
