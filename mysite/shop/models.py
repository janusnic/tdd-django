from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('Categories Name', max_length=100)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(max_length=4096, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_index_by_category', args=[self.slug])


@python_2_unicode_compatible
class Product(models.Model):
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sale', 'For Sale'),
        ('onstock', 'On Stock'),
        ('notavailbl', 'Not Available'),
    )

    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
