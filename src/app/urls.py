from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("confirm", views.confirm_email, name="confirm_email"),
    path("delete_photo/", views.delete_photo, name="delete_photo"),
    path("toggle_favorite/", views.toggle_favorite, name="toggle_favorite"),
]
