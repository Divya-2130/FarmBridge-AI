from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .predictor import predict_demand_and_price


@login_required
def price_recommendation(request):
    """
    Farmer enters rough historical numbers for a crop, sees the AI's demand
    forecast and suggested price range in their dashboard.
    """
    result = None
    if request.method == "POST":
        season = int(request.POST["season"])
        past_avg_demand_kg = float(request.POST["past_avg_demand_kg"])
        past_avg_price = float(request.POST["past_avg_price"])
        result = predict_demand_and_price(season, past_avg_demand_kg, past_avg_price)

    return render(request, "ai_engine/price_recommendation.html", {"result": result})
