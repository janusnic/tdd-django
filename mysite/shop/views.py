from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    products = Product.objects.filter(available=True)
    
    return render(request, 'shop/product/index.html', {'products': products})
    # return render(request,'shop/product/index.html')

def product_detail(request, id):
    product = Product.objects.get(id=id, available=True)
    
    return render(request,'shop/product/detail.html', {'product': product })