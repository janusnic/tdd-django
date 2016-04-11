from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('Categories Name', max_length=100)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(max_length=4096, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_index_by_category', args=[self.slug])

class AvailabledManager(models.Manager):
    def get_queryset(self):
        return super(AvailabledManager, self).get_queryset().filter(status='available')

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
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

    objects = models.Manager() # The default manager.
    available = AvailabledManager() # The Dahl-specific manager.

    class Meta:
        ordering = ('-price','-updated',)
        index_together = (('id', 'slug'),)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        s = self.name
        if self.status != 'available':
            s += ' (not available)'
        return s

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

@python_2_unicode_compatible
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

@python_2_unicode_compatible
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
