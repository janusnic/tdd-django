# tdd-django unit_12
reviews
=======
    python manage.py startapp reviews

folder structure
-----------------
        tree reviews
        ------------
                reviews
                |-- __init__.py
                |-- admin.py
                |-- migrations
                |   `-- __init__.py
                |-- models.py
                |-- tests.py
                `-- views.py

models.py
---------
        from django.db import models
        from django.contrib.auth.models import User
        from shop.models import Product

        class Review(models.Model):
            RATING_CHOICES = (
                (0, '0'),
                (1, '1'),
                (2, '2'),
                (3, '3'),
                (4, '4'),
                (5, '5'),
            )
            product = models.ForeignKey(Product)
            pub_date = models.DateTimeField('date published')
            user_name = models.CharField(max_length=100)
            comment = models.CharField(max_length=200)
            rating = models.IntegerField(choices=RATING_CHOICES, default=0)

migrations
----------

        ./manage.py makemigrations reviews
        Migrations for 'reviews':
          0001_initial.py:
            - Create model Review
        $ ./manage.py migrate
        Operations to perform:
          Apply all migrations: sessions, auth, shop, admin, userprofiles, contenttypes, reviews
        Running migrations:
          Rendering model states... DONE
          Applying reviews.0001_initial... OK


admin.py
--------
        from django.contrib import admin

        from .models import Review

        class ReviewAdmin(admin.ModelAdmin):
            model = Review
            list_display = ('product', 'rating', 'user_name', 'comment', 'pub_date')
            list_filter = ['pub_date', 'user_name']
            search_fields = ['comment']
            
        admin.site.register(Review, ReviewAdmin)


reviews URL Configuration
-------------------------
        """reviews URL Configuration

        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.review_list, name='review_list'),
            url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),

        ]

reviews/views.py
----------------
        from django.shortcuts import get_object_or_404, render

        from .models import Review

        def review_list(request):
            latest_review_list = Review.objects.order_by('-pub_date')[:9]
            context = {'latest_review_list':latest_review_list}
            return render(request, 'reviews/review_list.html', context)


        def review_detail(request, review_id):
            review = get_object_or_404(Review, pk=review_id)
            return render(request, 'reviews/review_detail.html', {'review': review})

reviews/review_list.html
------------------------
            {% extends 'base.html' %}

            {% block title %}
            <h2>Latest reviews</h2>
            {% endblock %}

            {% block content %}
            {% if latest_review_list %}
            <div class="row">
                {% for review in latest_review_list %}
                <div class="col-xs-6 col-lg-4">
                    <h4><a href="{% url 'reviews:review_detail' review.id %}">
                    {{ review.product.name }}
                    </a></h4>
                    <h6>Rated {{ review.rating }} of 5 by <a href="#" >{{ review.user_name }}</a></h6>
                    <p>{{ review.comment }}</p>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p>No reviews are available.</p>
            {% endif %}
            {% endblock %}

reviews/review_detail.html
--------------------------
        {% extends 'base.html' %}

              
        <div id="main" class="col-md-8 product-list">
            <div class="row">
                {% block title %}
                <h2><a href="{{ review.product.get_absolute_url }}">{{ review.product.name }}</a></h2>
                {% endblock %}

                <h4>Rated {{ review.rating }} of 5 by <a href="#" >{{ review.user_name }}</a></h4>
                <p>{{ review.pub_date }}</p>
                <p>{{ review.comment }}</p>

            </div>
         </div>

mysite/urls.py
--------------
        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^reviews/', include('reviews.urls', namespace='reviews')),
            
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            url(r'^users/', include('userprofiles.urls', namespace="users")),
            url(r'^admin/', admin.site.urls),
        ]

forms.py
--------

        from django.forms import ModelForm, Textarea
        from reviews.models import Review


        class ReviewForm(ModelForm):
            class Meta:
                model = Review
                fields = ['rating', 'comment']
                widgets = {
                    'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
                }

shop/views.py
-------------
        from reviews.forms import ReviewForm

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

django-bootstrap3
-----------------
         pip install django-bootstrap3
        Collecting django-bootstrap3
          Downloading django-bootstrap3-7.0.1.tar.gz
        Building wheels for collected packages: django-bootstrap3
          Running setup.py bdist_wheel for django-bootstrap3 ... done
          Stored in directory: /home/janus/.cache/pip/wheels/37/b9/48/b6eb4295aff1a7ce750cc958e7f2974096eaede35d7cec8e44
        Successfully built django-bootstrap3
        Installing collected packages: django-bootstrap3
        Successfully installed django-bootstrap3-7.0.1

settings.py
-----------
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'ckeditor',
            'ckeditor_uploader',
            'shop',
            'userprofiles',
            'bootstrap3',
            'reviews',
        ]

shop/views.py
-------------
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


shop/product/detail.html
-------------------
            {% extends "base.html" %}
            {% load bootstrap3 %}

            {% load static %}

            {% block title %}{{ product.name }}{% endblock %}

            {% block content %}
                <div class="container">
                  <!-- row of columns -->
                  <div class="row">
                    <div class="col-md-4 sidebar">
                        <h3>Categories</h3>
                        <ul>
                            <li {% if not category %}class="selected"{% endif %}>
                                <a href="{% url "shop:index" %}">All</a>
                            </li>
                        {% for c in categories %}
                            <li {% if category.slug == c.slug %}class="selected"{% endif %}>
                                <a href="{{ c.get_absolute_url }}">{{ c.name }}</a>
                            </li>
                        {% endfor %}
                        </ul>
                    </div>

                <div id="main" class="col-md-8 product-list">
                
                <div class="product-detail">
                    <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                    <h1>{{ product.name }}</h1>
                    <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
                    <p class="price">${{ product.price }}</p>

                    <p class="raiting">

                            {% if product.views > 1 %}
                                ({{ product.views }} views)
                            {% elif product.views == 1 %}
                                ({{ product.views }} view)
                            {% endif %}
                    </p>

                    <form action="{% url "shop:cart_add" product.id %}" method="post">
                        {{ cart_product_form }}
                        {% csrf_token %}
                        <input type="submit" class="btn btn-primary" value="Add to cart">
                    </form>
                    
                    {{ product.description|linebreaks }}
                </div>

                <h3>Recent reviews</h3>

                     {% if product.review_set.all %}
                        <div class="row">
                            {% for review in product.review_set.all %}
                            <div class="col-xs-6 col-lg-4">
                                <em>{{ review.comment }}</em>
                                <h6>Rated {{ review.rating }} of 5 by {{ review.user_name }}</h6>
                                <h5><a href="{% url 'reviews:review_detail' product.id %}">
                                Read more
                                </a></h5>
                            </div>
                            {% endfor %}
                        </div>
                        {% else %}
                        <p>No reviews for this wine yet</p>
                        {% endif %}
                    <h3>Add your review</h3>
                        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
                       
                        <form action="{% url 'shop:add_review' product.id %}" method="post" class="form">
                            {% csrf_token %}
                            {% bootstrap_form review_form layout='inline' %}
                            {% buttons %}
                            <button type="submit" class="btn btn-primary">
                              {% bootstrap_icon "star" %} Add
                            </button>
                            {% endbuttons %}
                        </form>
             </div>
            </div>
            <hr>

            {% endblock %}

shop/views.py
-------------
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

        def add_review(request, id):
            product = get_object_or_404(Product, id=id, status='available')
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                comment = form.cleaned_data['comment']
                user_name = request.user.username
                review = Review()
                review.product = product
                review.user_name = user_name
                review.rating = rating
                review.comment = comment
                review.pub_date = datetime.datetime.now()
                review.save()
                
                return HttpResponseRedirect('/shop')

shop/urls.py
------------

        """shop URL Configuration

        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^cart/$', views.cart_detail, name='cart_detail'),
            url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
            url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
            url(r'^create/$', views.order_create, name='order_create'),
            url(r'^add_review/(?P<id>\d+)/$', views.add_review, name='add_review'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),

        ]


Вспомогательные функции
=======================
Пакет django.shortcuts содержит вспомогательные функции и классы “влияющие” на несколько уровней MVC. Другими словами, эти функции упрощают разработку и код.

render
------
    render(request, template_name, context=None, context_instance=_context_instance_undefined, content_type=None, status=None, current_app=_current_app_undefined, dirs=_dirs_undefined, using=None)
Выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.

Функция render() аналогична вызову функции render_to_response() с аргументом context_instance, который указывает использовать RequestContext.

Django не предоставляет функции для создания TemplateResponse т.к. конструктор TemplateResponse принимает аргументы аналогичные аргументам render().

Обязательные аргументы
----------------------
- request
Объект обрабатываемого запроса

- template_name
Полное название шаблона, который должен использоваться, или список названий шаблонов. Если передать список, будет использован первый существующий шаблон. Информацию о том, как ищутся шаблоны, смотрите раздел о загрузчике шаблонов.

Необязательные аргументы
------------------------
- context
Словарь переменных для контекста шаблона. По умолчанию, этот словарь пустой. Если значение ключа словаря это функция, она будет вызвана перед выполнением шаблона.

- content_type
MIME-тип результата. По умолчанию используется значение настройки DEFAULT_CONTENT_TYPE.

- status
Код HTTP статуса ответа. По умолчанию 200.


Следующий пример выполняет шаблон myapp/index.html и возвращает ответ с MIME-типом application/xhtml+xml:

        from django.shortcuts import render

        def my_view(request):
            # View code here...
            return render(request, 'myapp/index.html', {"foo": "bar"},
                content_type="application/xhtml+xml")
Этот пример аналогичен:

        from django.http import HttpResponse
        from django.template import RequestContext, loader

        def my_view(request):
            # View code here...
            t = loader.get_template('myapp/index.html')
            c = RequestContext(request, {'foo': 'bar'})
            return HttpResponse(t.render(c),
                content_type="application/xhtml+xml")
        render_to_response

render_to_response
------------------
    render_to_response(template_name, context=None, context_instance=_context_instance_undefined, content_type=None, status=None, dirs=_dirs_undefined, using=None)

Выполняет указанный шаблон с переданным словарем контекста и возвращает HttpResponse с полученным содержимым.

Обязательные аргументы
----------------------
- template_name
Полное название шаблона, который должен использоваться, или список названий шаблонов. Если передать список, будет использован первый существующий шаблон. 

Необязательные аргументы
------------------------
- context
Словарь переменных для контекста шаблона. По умолчанию, этот словарь пустой. Если значение ключа словаря это функция, она будет вызвана перед выполнением шаблона.

- content_type
MIME-тип результата. По умолчанию используется значение настройки DEFAULT_CONTENT_TYPE.

- status
Код HTTP статуса ответа. По умолчанию 200.

- using
Параметр конфигурации NAME используется шаблонным движком для загрузки шаблона.

Следующий пример выполняет шаблон myapp/index.html и возвращает ответ с MIME-типом application/xhtml+xml:

        from django.shortcuts import render_to_response

        def my_view(request):
            # View code here...
            return render_to_response('myapp/index.html', {"foo": "bar"},
                content_type="application/xhtml+xml")
Этот пример аналогичен:

        from django.http import HttpResponse
        from django.template import Context, loader

        def my_view(request):
            # View code here...
            t = loader.get_template('myapp/index.html')
            c = Context({'foo': 'bar'})
            return HttpResponse(t.render(c),
                content_type="application/xhtml+xml")
redirect
--------
        redirect(to, permanent=False, *args, **kwargs)
Возвращает перенаправление(HttpResponseRedirect) на URL указанный через аргументы.

В аргументах можно передать:

- Экземпляр модели: как URL будет использоваться результат вызова метода get_absolute_url().

- Название представления, возможно с аргументами: для вычисления URL-а будет использоваться функция urlresolvers.reverse.

- Абсолютный или относительный URL, который будет использован для перенаправления на указанный адрес.

- По умолчанию использует временное перенаправление, используйте аргумент permanent=True для постоянного перенаправления.

Функцию redirect() можно использовать несколькими способами.

Передавая объект; в качестве URL-а для перенаправления будет использоваться результат вызова метода get_absolute_url():

        from django.shortcuts import redirect

        def my_view(request):
            ...
            object = MyModel.objects.get(...)
            return redirect(object)

Передавая название представления и необходимые позиционные или именованные аргументы; URL будет вычислен с помощью функции reverse():

        def my_view(request):
            ...
            return redirect('some-view-name', foo='bar')
Передавая непосредственно URL:

        def my_view(request):
            ...
            return redirect('/some/url/')
Работает также с полным URL-ом:

        def my_view(request):
            ...
            return redirect('https://example.com/')

По умолчанию, redirect() возвращает временное перенаправление. Все варианты выше принимают аргумент permanent; если передать True будет использоваться постоянное перенаправление:

        def my_view(request):
            ...
            object = MyModel.objects.get(...)
            return redirect(object, permanent=True)

get_object_or_404
-----------------
        get_object_or_404(klass, *args, **kwargs)

Вызывает get() для переданного менеджера модели и возвращает полученный объект. Но вызывает исключение Http404 вместо DoesNotExist.

Обязательные аргументы
----------------------
- klass
Класс Model, экземпляр Manager или QuerySet, который будет использован для получения объекта.

- **kwargs
Параметры поиска в формате принимаемом методами get() и filter().


Этот пример получает объект модели MyModel с первичным ключом равным 1:

        from django.shortcuts import get_object_or_404

        def my_view(request):
            my_object = get_object_or_404(MyModel, pk=1)
Этот пример аналогичен:

        from django.http import Http404

        def my_view(request):
            try:
                my_object = MyModel.objects.get(pk=1)
            except MyModel.DoesNotExist:
                raise Http404("No MyModel matches the given query.")

Обычно используется Model, как в примере выше. Но можно передать и объект QuerySet:

        queryset = Book.objects.filter(title__startswith='M')
        get_object_or_404(queryset, pk=1)

Приведенный пример немного надуманный, так как это равносильно:

        get_object_or_404(Book, title__startswith='M', pk=1)
но может быть полезен, если queryset передается из другого места.

Также можно использовать Manager. Это полезно, если, например, вы используете собственный менеджер:

        get_object_or_404(Book.dahl_objects, title='Matilda')
Можно использовать менеджер отношений между моделями:

        author = Author.objects.get(name='Roald Dahl')
        get_object_or_404(author.book_set, title='Matilda')
так как используется метод get(), может быть вызвано исключение MultipleObjectsReturned, если запрос вернет несколько объектов.

get_list_or_404
---------------
    get_list_or_404(klass, *args, **kwargs)
Возвращает результат метода filter() для переданного менеджера модели, вызывает Http404 если получен пустой список.

Обязательные аргументы
----------------------
- klass
Экземпляр Model, Manager или QuerySet, который будет использован для получения списка объектов.

- **kwargs
Параметры поиска в формате принимаемом методами get() и filter().

Этот пример получает все опубликованные объекты модели``MyModel``:

        from django.shortcuts import get_list_or_404

        def my_view(request):
            my_objects = get_list_or_404(MyModel, published=True)
Этот пример аналогичен:

        from django.http import Http404

        def my_view(request):
            my_objects = list(MyModel.objects.filter(published=True))
            if not my_objects:
                raise Http404("No MyModel matches the given query.")


shop/views.py
-------------

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
                return redirect('shop:product_detail',id=product.id,slug=product.slug)
            
            return render(request, 'shop/product/detail.html', {'product': product, 'form': form})


shop/product.detail.html
------------------------

            {% if user.is_authenticated %}
               <h3>Add your review</h3>
                {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
               
                <form action="{% url 'shop:add_review' product.id %}" method="post" class="form">
                    {% csrf_token %}
                    {% bootstrap_form review_form layout='inline' %}
                    {% buttons %}
                    <button type="submit" class="btn btn-primary">
                      {% bootstrap_icon "star" %} Add
                    </button>
                    {% endbuttons %}
                </form>
            {% else %}
            <p>Login required <a href="{% url 'users:login' %}">Login</a></p> 
            {% endif %}

reviews/viewx.py
----------------
        from django.shortcuts import get_object_or_404, render

        from .models import Review

        def review_list(request):
            latest_review_list = Review.objects.order_by('-pub_date')[:9]
            context = {'latest_review_list':latest_review_list}
            return render(request, 'reviews/review_list.html', context)


        def review_detail(request, review_id):
            review = get_object_or_404(Review, pk=review_id)
            return render(request, 'reviews/review_detail.html', {'review': review})

        def user_review_list(request, username=None):
            if not username:
                username = request.user.username
            latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
            context = {'latest_review_list':latest_review_list, 'username':username}
            return render(request, 'reviews/user_review_list.html', context)

reviews.py/urls.py
------------------
        """reviews URL Configuration

        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.review_list, name='review_list'),
            url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
            url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
            url(r'^review/user/$', views.user_review_list, name='user_review_list'),

        ]

reviews/user_review_list.html
-----------------------------
        {% extends 'reviews/review_list.html' %}

        {% block title %}
        <h2>Reviews by {{ user.username }}</h2>
        {% endblock %}

userprofile/profile.html
-------------------------

        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Profile {% endblock %}
          {% block content %}
            {% block main %}
            {% endblock main %}
            {% block aside %}
                   <h2>Menu</h2>
                    <ul>
                      <li><a href="{% url 'reviews:user_review_list' user.username %}">Hello {{ user.username }}</a></li>
                      <li><a href='{% url "users:profile" user.username %}'>My profile</a></li>
                      <li><a href='{% url "users:edit_profile" %}'>Edit my profile</a></li>
                    </ul>
            {% endblock aside %}
        {% endblock content %}
