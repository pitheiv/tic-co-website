
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="dashboard/login.html",
            next_page="/dashboard/",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page="dashboard:login"
        ),
        name="logout",
    ),
    path("", views.index, name="index"),
    path("pos/", views.pos, name="pos"),
    path("checkout/", views.checkout, name="checkout"),
]
