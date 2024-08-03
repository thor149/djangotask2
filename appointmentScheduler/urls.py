from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('book/<str:pk>/', views.book_appointment, name='book_appointment'),
    path('appointment/<str:pk>/', views.appointment_details, name='appointment_details'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
]
