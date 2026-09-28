from django.db import models
from farmers.models import Farm


class Product(models.Model):
    class QualityGrade(models.TextChoices):
        A = "A", "Grade A - Premium"
        B = "B", "Grade B - Standard"
        C = "C", "Grade C - Economy"

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=80, help_text="e.g. Vegetables, Fruits, Grains")
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available_kg = models.DecimalField(max_digits=8, decimal_places=2)
    quality_grade = models.CharField(max_length=1, choices=QualityGrade.choices, default=QualityGrade.B)
    harvest_date = models.DateField()
    is_preorder_available = models.BooleanField(default=False)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.farm.farm_name}"
