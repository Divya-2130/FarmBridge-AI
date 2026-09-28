from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from farmers.models import Farm, FarmerProfile


def product_list(request):
    """Marketplace page - search + filter, the Customer Module's entry point."""
    products = Product.objects.select_related("farm").all()

    query = request.GET.get("q")
    category = request.GET.get("category")
    max_price = request.GET.get("max_price")

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)
    if max_price:
        products = products.filter(price_per_kg__lte=max_price)

    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})


@login_required
def add_product(request):
    """Farmer adds a product to their farm. Requires an approved farm/KYC."""
    profile = get_object_or_404(FarmerProfile, user=request.user)
    farm = Farm.objects.filter(farmer=profile).first()
    kyc_approved = profile.kyc_status == FarmerProfile.KYCStatus.APPROVED
    if request.method == "POST" and farm and kyc_approved:
        Product.objects.create(
            farm=farm,
            name=request.POST["name"],
            category=request.POST["category"],
            price_per_kg=request.POST["price_per_kg"],
            quantity_available_kg=request.POST["quantity_available_kg"],
            quality_grade=request.POST.get("quality_grade", "B"),
            harvest_date=request.POST["harvest_date"],
            is_preorder_available=bool(request.POST.get("is_preorder_available")),
            image=request.FILES.get("image"),
        )
        return redirect("farmer-dashboard")

    return render(request, "products/add_product.html", {"farm": farm, "kyc_approved": kyc_approved})
