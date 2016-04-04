from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .forms import CartAddProductForm

def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # products = Product.objects.filter(status='available')
    products = Product.available.all()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/index.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, status='available')
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})

def cart_add(request, product_id):
    return render(request,
                  'shop/product/cart.html')