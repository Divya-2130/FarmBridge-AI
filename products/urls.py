from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("add/", views.add_product, name="add-product"),
    path("<int:product_id>/", views.product_detail, name="product-detail"),
]
