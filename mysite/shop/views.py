from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, OrderItem
from .forms import CartAddProductForm
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .tasks import order_created

from reviews.models import Review

from reviews.forms import ReviewForm
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def index(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    
    products = Product.available.all()

    paginator = Paginator(products, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        products = paginator.page(page)
    except (InvalidPage, EmptyPage):
        products = paginator.page(paginator.num_pages)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.available.all()
        products = products.filter(category=category)
        paginator = Paginator(products, 2)

        try: page = int(request.GET.get("page", '1'))
        except ValueError: page = 1
        try:
            products = paginator.page(page)
        except (InvalidPage, EmptyPage):
            products = paginator.page(paginator.num_pages)

    return render(request, 'shop/product/index.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, status='available')

    review_form = ReviewForm()

    try:
        product.views = product.views + 1
        product.save()
    except:
        pass

    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form, 'review_form': review_form})
@login_required
def add_review(request, id):
    product = get_object_or_404(Product, id=id, status='available')
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        #user_name = form.cleaned_data['username']
        user_name = request.user.username
        review = Review()
        review.product = product
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('shop:product_detail',kwargs={"id": product.id}))
        #return HttpResponseRedirect(reverse('shop:product_detail',args=(product.id,)))
        return redirect('shop:product_detail',id=product.id,slug=product.slug)
    
    return render(request, 'shop/product/detail.html', {'product': product, 'form': form})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('shop:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'shop/product/cart.html', {'cart': cart})

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch task
            order_created(order.id)
            return render(request, 'shop/orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/orders/create.html', {'cart': cart,
                                                        'form': form})


