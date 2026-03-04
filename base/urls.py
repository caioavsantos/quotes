from django.urls import path
from . import views

app_name = "base"

urlpatterns = [
    path("", views.Homepage.as_view(), name="home"),
    path("about", views.About.as_view(), name="about"),
    path("login", views.LoginPage.as_view(), name="login"),
    path("register", views.RegisterPage.as_view(), name="register"),
    path("logout", views.logoutUser, name="logout"),
    path("profile/", views.Profile.as_view(), name="profile")
]
