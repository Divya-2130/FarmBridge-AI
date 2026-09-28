from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import FarmerProfile, Farm
from products.models import Product
from orders.models import OrderItem


def _is_farmer(user):
    return user.is_authenticated and user.is_farmer()


@login_required
@user_passes_test(_is_farmer)
def farmer_dashboard(request):
    profile, _ = FarmerProfile.objects.get_or_create(user=request.user)
    products = Product.objects.filter(farm__farmer=profile)
    pending_orders = OrderItem.objects.filter(product__farm__farmer=profile, order__status="PENDING")
    context = {
        "profile": profile,
        "products": products,
        "pending_orders": pending_orders,
    }
    return render(request, "farmers/dashboard.html", context)


@login_required
@user_passes_test(_is_farmer)
def submit_kyc(request):
    profile, _ = FarmerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile.id_document = request.FILES.get("id_document")
        profile.kyc_status = FarmerProfile.KYCStatus.PENDING
        profile.save()
        return redirect("farmer-dashboard")
    return render(request, "farmers/submit_kyc.html", {"profile": profile})


@login_required
def admin_approve_kyc(request, farmer_id):
    """Only staff/admin should reach this - enforced by is_staff check."""
    if not request.user.is_staff:
        return redirect("home")
    profile = get_object_or_404(FarmerProfile, id=farmer_id)
    action = request.POST.get("action")
    if action == "approve":
        profile.kyc_status = FarmerProfile.KYCStatus.APPROVED
    elif action == "reject":
        profile.kyc_status = FarmerProfile.KYCStatus.REJECTED
    profile.save()
    return redirect("admin-dashboard")
