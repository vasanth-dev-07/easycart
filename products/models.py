from django.db import models


class ProductModel(models.Model):
    name = models.CharField(max_length=255,blank=False)
    category = models.CharField(max_length=50,blank=False)
    subcategory = models.CharField(max_length=50,blank=False)
    description = models.TextField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product/images',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name