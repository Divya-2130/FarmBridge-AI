from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Payment


@login_required
def payment_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    payment, _ = Payment.objects.get_or_create(
        order=order, defaults={"amount": order.total_amount}
    )
    return render(request, "payments/checkout.html", {"order": order, "payment": payment})


@login_required
def verify_payment(request, order_id):
    """MOCK payment for demo purposes - marks the order paid without calling Razorpay."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    payment = order.payment
    payment.status = Payment.Status.PAID
    payment.razorpay_payment_id = "MOCK_PAYMENT_SUCCESS"
    payment.save()
    order.status = Order.Status.CONFIRMED
    order.save()
    return redirect("my-orders")