from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),
    # Opatrovnická část webu
    path('opatrovnik/', include('caregiver.urls')),
    # Klientská část webu
    path('klient/', include('patient.urls')),
    # Administrační část webu + homepage a login/logout
    path('', include('home.urls')),
    # Potřeba importovat, jelikož zde pracuji s user authentication
    path('', include('django.contrib.auth.urls')),
]
