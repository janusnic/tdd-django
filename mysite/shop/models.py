from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField('Categories Name', max_length=100)
    description = models.TextField(max_length=4096, default='')

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=200, db_index=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
