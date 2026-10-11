from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    path('', views.tutor_list, name='list'),
    path('<int:pk>/', views.tutor_detail, name='detail'),
]