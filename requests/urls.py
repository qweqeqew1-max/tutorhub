from django.urls import path
from . import views

app_name = 'requests'

urlpatterns = [
    path('', views.request_create, name='create'),
    path('success/', views.request_success, name='success'),
]