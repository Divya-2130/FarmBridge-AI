from django.urls import path
from . import views

urlpatterns = [
    path("<int:order_id>/checkout/", views.payment_checkout, name="payment-checkout"),
    path("<int:order_id>/verify/", views.verify_payment, name="verify-payment"),
]
