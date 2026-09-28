from django.db import models
from django.conf import settings


class FarmerProfile(models.Model):
    class KYCStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farmer_profile")
    id_document = models.FileField(upload_to="kyc_docs/", blank=True, null=True)
    kyc_status = models.CharField(max_length=10, choices=KYCStatus.choices, default=KYCStatus.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - KYC {self.kyc_status}"


class Farm(models.Model):
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name="farms")
    farm_name = models.CharField(max_length=150)
    location = models.CharField(max_length=200)
    size_in_acres = models.DecimalField(max_digits=6, decimal_places=2)
    farming_method = models.CharField(max_length=100, help_text="e.g. Organic, Natural, Conventional")

    def __str__(self):
        return self.farm_name
