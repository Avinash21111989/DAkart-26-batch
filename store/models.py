from django.db import models
from category.models import category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True,blank=False)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    images = models.ImageField()
    stock = models.IntegerField()
    category = models.ForeignKey(category, on_delete = models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now_add = True)
    is_available = models.BooleanField(default = True)

    def __str__(self):
        return self.product_name

