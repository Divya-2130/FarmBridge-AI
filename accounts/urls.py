from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard-redirect"),
    path("customer-dashboard/", views.customer_dashboard, name="customer-dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin-dashboard"),
]
