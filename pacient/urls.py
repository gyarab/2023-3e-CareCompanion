from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/seznam-opatrovniku', views.caretakers_list),
    path('/kontakty', views.contacts),
    path('/rozvrh-dne', views.schedule),
]
