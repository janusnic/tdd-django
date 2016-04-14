# -*- coding: UTF-8 -*-
from django import template
from shop.models import Product

register=template.Library()
 
@register.inclusion_tag('shop/product/_popular_products.html') # регистрируем тег и подключаем шаблон _popular_posts

def popular_products():
    products = Product.objects.filter(views__gte=5).filter(status='available')[:6]
    return locals()
