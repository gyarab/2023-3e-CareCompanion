from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prihlaseni/', views.login_user, name='login_user'),
    path('sprava/', views.administration, name='administration'),
    path('sprava/vytvoreni-uctu/', views.account_creation, name='account_creation'),
    path('sprava/registrace-klienta/', views.universal_patient_form, name='patient_registration'),
    # path('sprava/registrace-opatrovnika/', views.register_caregiver, name='caregiver_registration'),
    path('sprava/smeny/', views.shifts, name='shifts'),
    path('sprava/smeny/<int:pk>/', views.edit_shifts, name='edit_shifts'),
    path('sprava/aktivity/', views.patient_activities, name='patient_activities'),
    path('sprava/aktivity/<int:pk>/', views.edit_patient_activities, name='edit_patient_activities'),
    path('sprava/uzivatele/', views.display_users, name='display_users'),
    path('sprava/uzivatele/smazat-<int:pk>/', views.delete_user, name='delete_user'),
    path('sprava/uzivatele/<str:info_on_user>/', views.user_update, name='user_update'),
    path('sprava/uzivatele/<str:info_on_user>/zmena-infa/', views.universal_patient_form, name='patient_update'),
    path('sprava/uzivatele/<str:info_on_user>/zmena-hesla/', views.user_reset_password, name='user_reset_password'),
    path('sprava/zmena-infa-o-domove/', views.institute_info, name='institute_info'),
    path('sprava/zmena-infa-o-domove/<str:category>/', views.edit_institute_info, name='edit_institute_info'),
    path('odhlaseni/', views.logout_user, name='logout_user'),
]
