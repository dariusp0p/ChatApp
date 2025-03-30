from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profilePage, name="profilePage"),
    path('signIn/', views.signInPage, name="signInPage"),
]