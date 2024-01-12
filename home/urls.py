from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('prihlaseni', views.login_user, name='login_user'),
    path('sprava', views.administration, name='administration'),
    path('sprava/vytvoreni-uctu', views.register_user, name='account_creation'),
    # path('sprava/registrace-klienta', views.register_user, name='patient_registration'),
    # path('sprava/registrace-opatrovnika', views.register_user, name='caregiver_registration'),
    path('odhlaseni', views.logout_user, name='logout_user'),
]
