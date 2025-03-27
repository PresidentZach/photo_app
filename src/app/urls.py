from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Maps 'app/' to views.index
]
