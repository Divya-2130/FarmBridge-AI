from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. Every account is one of three roles.
    Django's built-in auth (password hashing, sessions, login/logout) does
    the heavy lifting - we just add a role on top of it.
    """
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer"
        CUSTOMER = "CUSTOMER", "Customer"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)

    def is_farmer(self):
        return self.role == self.Role.FARMER

    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    def is_admin_role(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.role})"
