from django.contrib.auth.models import AbstractUser
from django.db import models
from product.models import Group, Product


class Student(AbstractUser):
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, default=None, null=True)
    available_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, default=None, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
