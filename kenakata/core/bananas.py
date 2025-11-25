from django.urls import path
from core import views

app_name = "bananas"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
]