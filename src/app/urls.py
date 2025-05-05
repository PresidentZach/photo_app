from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("confirm", views.confirm_email, name="confirm_email"),
    path('set-favorite/', views.set_favorite, name='set_favorite'),
]
