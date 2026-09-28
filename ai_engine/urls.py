from django.urls import path
from . import views

urlpatterns = [
    path("price-recommendation/", views.price_recommendation, name="price-recommendation"),
]
