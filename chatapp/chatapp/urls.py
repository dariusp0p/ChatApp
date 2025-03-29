from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('mainApp.urls')),
    path('user/', include('userApp.urls')),
]
