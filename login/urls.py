from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_login'),
    path('/help', views.help_w_registration, name='help'),
    path('/odhlaseni', views.logout_user, name='logout'),
    path('/registrace', views.register_user, name='registration'),
]
