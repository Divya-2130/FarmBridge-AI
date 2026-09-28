from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from products.models import Product
from decimal import Decimal
from .models import Order, OrderItem


def _get_cart(session):
    """Cart lives in the session as {product_id: quantity_kg} - no DB writes until checkout."""
    return session.setdefault("cart", {})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    qty = float(request.POST.get("quantity_kg", 1))
    cart = _get_cart(request.session)
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session.modified = True
    return redirect("view-cart")


@login_required
def view_cart(request):
    cart = _get_cart(request.session)
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = float(product.price_per_kg) * qty
        total += subtotal
        items.append({"product": product, "qty": qty, "subtotal": subtotal})
    return render(request, "orders/cart.html", {"items": items, "total": total})


@login_required
@transaction.atomic
def checkout(request):
    """Turns the session cart into a real Order + OrderItems, then clears the cart."""
    cart = _get_cart(request.session)
    if not cart:
        return redirect("product-list")

    is_preorder = bool(request.POST.get("is_preorder"))
    order = Order.objects.create(customer=request.user, is_preorder=is_preorder)

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order, product=product, quantity_kg=qty, price_at_order=product.price_per_kg
        )
        if not is_preorder:
            product.quantity_available_kg -= Decimal(str(qty))
            product.save()

    order.recalculate_total()
    request.session["cart"] = {}
    return redirect("payment-checkout", order_id=order.id)


@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def update_order_status(request, order_id):
    """Farmer moves an order through the delivery pipeline."""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get("status")
    if new_status in Order.Status.values:
        order.status = new_status
        order.save()
    return redirect("farmer-dashboard")
