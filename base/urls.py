from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='base-home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('cookies/', views.cookies, name='cookies'),
]