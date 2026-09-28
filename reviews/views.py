from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import OrderItem, Order
from .models import Review


@login_required
def add_review(request, product_id):
    """A customer can only review a product after it was actually delivered to them."""
    product = get_object_or_404(Product, id=product_id)
    delivered = OrderItem.objects.filter(
        product=product, order__customer=request.user, order__status=Order.Status.DELIVERED
    ).exists()

    if request.method == "POST" and delivered:
        Review.objects.create(
            customer=request.user,
            product=product,
            rating=int(request.POST["rating"]),
            comment=request.POST.get("comment", ""),
        )
    return redirect("product-detail", product_id=product.id)
