from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.farmer_dashboard, name="farmer-dashboard"),
    path("kyc/submit/", views.submit_kyc, name="submit-kyc"),
    path("kyc/<int:farmer_id>/review/", views.admin_approve_kyc, name="admin-approve-kyc"),
]
