# -*- coding: UTF-8 -*-
from django import template
from shop.models import Product

register=template.Library()
 
@register.inclusion_tag('shop/product/_latest_products.html') # регистрируем тег и подключаем шаблон _latest_posts

def latest_products():
    products = Product.objects.order_by('-updated').filter(status='available')[:6]
    return locals()
