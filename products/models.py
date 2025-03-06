from django.db import models


class ProductModel(models.Model):
    name = models.CharField(max_length=255,blank=False)
    description = models.TextField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)