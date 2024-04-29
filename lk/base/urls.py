from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("profile/", views.lk_profile, name="lk_profile"),
    # path('apply-filters', views.apply_filters, name='apply-filters'),
    path("", views.home, name="home"),
]
