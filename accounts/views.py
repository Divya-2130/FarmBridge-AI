from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm
from .models import User


def home(request):
    """Public landing page - the 'storefront' of FarmBridge AI."""
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Welcome to FarmBridge AI.")
            return redirect("dashboard-redirect")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard-redirect")
        messages.error(request, "Invalid username or password.")
    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard_redirect(request):
    """Sends each role to its own dashboard - the core of role-based access."""
    user = request.user
    if user.is_farmer():
        return redirect("farmer-dashboard")
    if user.is_customer():
        return redirect("customer-dashboard")
    if user.is_admin_role() or user.is_staff:
        return redirect("admin-dashboard")
    return redirect("home")


@login_required
@user_passes_test(lambda u: u.is_customer())
def customer_dashboard(request):
    """Module: customer's home base - recent orders + quick links."""
    from orders.models import Order
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")[:5]
    return render(request, "accounts/customer_dashboard.html", {"orders": orders})


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_admin_role())
def admin_dashboard(request):
    """Module 10: platform-wide view for KYC approvals, orders, and stats."""
    from farmers.models import FarmerProfile
    from orders.models import Order
    from products.models import Product

    context = {
        "pending_kyc": FarmerProfile.objects.filter(kyc_status=FarmerProfile.KYCStatus.PENDING),
        "total_farmers": User.objects.filter(role=User.Role.FARMER).count(),
        "total_customers": User.objects.filter(role=User.Role.CUSTOMER).count(),
        "total_products": Product.objects.count(),
        "total_orders": Order.objects.count(),
        "recent_orders": Order.objects.order_by("-created_at")[:10],
    }
    return render(request, "accounts/admin_dashboard.html", context)
