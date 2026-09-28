from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        PACKED = "PACKED", "Packed"
        SHIPPED = "SHIPPED", "Shipped"
        OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY", "Out for Delivery"
        DELIVERED = "DELIVERED", "Delivered"

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_preorder = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def recalculate_total(self):
        self.total_amount = sum(item.subtotal() for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_kg = models.DecimalField(max_digits=6, decimal_places=2)
    price_at_order = models.DecimalField(max_digits=8, decimal_places=2)

    def subtotal(self):
        return self.quantity_kg * self.price_at_order

    def __str__(self):
        return f"{self.product.name} x {self.quantity_kg}kg"
