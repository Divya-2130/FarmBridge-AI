from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.view_cart, name="view-cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add-to-cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("my-orders/", views.my_orders, name="my-orders"),
    path("<int:order_id>/status/", views.update_order_status, name="update-order-status"),
]
