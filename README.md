# tdd-django unit_07

Django сессии
=============
Django полностью поддерживает сессии для анонимных пользователей, позволяет сохранять и получать данные для каждой посетителя сайта. Механизм сессии сохраняет данные на сервере и самостоятельно управляет сессионными куками. Куки содержат ID сессии,а не сами данные (если только вы не используете бэкенд на основе кук).

Активируем сессии
------------------
Сессии реализованы через промежуточный слой.

Чтобы активировать сессии, выполните следующие действия:

Убедитесь что MIDDLEWARE_CLASSES содержит 'django.contrib.sessions.middleware.SessionMiddleware'. settings.py по умолчанию, созданный django-admin startproject, уже содержит SessionMiddleware.

Есди вы не собираетесь использовать сессии, вы можете удалить SessionMiddleware из MIDDLEWARE_CLASSES и 'django.contrib.sessions' из INSTALLED_APPS. Это немного повысит производительность.

Настройка сессий
----------------
По умолчанию Django хранит сессии в базе данных (используя модель django.contrib.sessions.models.Session). В некоторых случаях лучше хранить данные сессии в других хранилищах, поэтому Django позволяет использовать файловую систему или кэш.

Использование базы данных для хранения сессии
---------------------------------------------
Если вы хотите использовать базу данных для хранения сесиии, укажите 'django.contrib.sessions' в настройке INSTALLED_APPS.

После настройки выполните manage.py migrate, чтобы добавить таблицу в базу данных.

Использование кэша для хранения сессии
---------------------------------------
Для улучшения производительности вы можете использовать кэш для хранения сессии.

Для этого вы должны настроить кэш.

Вам следует использовать кэш только при использовании Memcached. Кэш в памяти не хранит данные достаточно долго, и лучше использовать файлы или базу данных для сессии, чем каждый раз обращаться к кэшу в файловой системе или базе данных. Также кэш в памяти использует различные экземпляры кэша для разных процессов.
Если вы указали несколько кэшей в CACHES, Django будет использовать кэш по умолчанию. Чтобы использовать другой кэш, укажите его название в SESSION_CACHE_ALIAS.

После настройки кэша у вас есть две опции, как хранить данные в кэше:

Указать "django.contrib.sessions.backends.cache" в SESSION_ENGINE. Данные сессии будут храниться непосредственно в кэше. Однако, данные могут быть удалены при переполнении кэша или перезагрузке сервера кэша.

Для постоянно хранения закэшированных данных укажите "django.contrib.sessions.backends.cached_db" в SESSION_ENGINE. Все записи в кэш будут продублированы в базу данных. База данных будет использоваться, если данные не найдены в кэше.

Оба варианта работают достаточно быстро, но первый немного быстрее. Для большинства случаев cached_db будет достаточно быстрым, но если производительность для вас важнее, чем надежное хранение сессии, используйте бэкенд cache.

Если вы используете cached_db, вам необходимо настроить и бэкенд базы данных.

Использование файловой системы для хранения сессии
--------------------------------------------------
Чтобы использовать файловую систему, укажите "django.contrib.sessions.backends.file" в SESSION_ENGINE.

Вы также можете указать SESSION_FILE_PATH (по умолчанию tempfile.gettempdir(), обычно это /tmp), чтобы указать Django, где сохранять сессионные файлы. Убедитесь, что ваш сервер имеет права на чтение и запись указанного каталога.

Хранение сессии в куках
-----------------------
Чтобы хранить сессию в куках, укажите "django.contrib.sessions.backends.signed_cookies" в SESSION_ENGINE. Данные сессии будут сохранены в куках, используя криптографическую подпись и значение SECRET_KEY.

Рекомендуем указать True в SESSION_COOKIE_HTTPONLY, чтобы запретить доступ JavaScript к кукам.

Если SECRET_KEY не хранить в безопасности при использовании PickleSerializer, можно пострадать от атаки удаленного выполнения кода.

Злоумышленник, узнав SECRET_KEY, может не только подделать данные сессии, но и выполнить удаленный код т.к. данные сессии используют pickle.

Если вы храните сессию в куках, храните ваш секретный ключ максимально надежно для всех систем, которые используются пользователем.

Сессионные данные подписаны, но не закодированы
-----------------------------------------------
Клиент может прочитать данные сессии, если вы храните их в куках.

MAC (Message Authentication Code) используется для защиты данных от подделки пользователем. Данные будут недействительными, если пользователь попытается их поменять. Аналогичное происходит, если клиент, который хранит коки (например, браузер пользователя), не может сохранить сессионную куку и удаляет её. Несмотря на то , что Django сжимает данные, вполне возможно превысить принятый лимит 4096 байтов на куку.

Актуальность не гарантируется
-----------------------------
Обратите внимание, хотя MAC может гарантировать авторизацию данных (что они были созданы вашим сайтом, а не кем-то другим), и целостность данных (данные не менялись и правильны), он не может гарантировать актуальность, то есть, что полученные данные последние, которые вы отсылали клиенту. Это означает, что при определенном использовании кук для сессии, ваш сайт может быть подвержен replay атакам. В отличии от других бэкендов сессии, которые хранят данные на сервере и очищают их при выходе пользователя(log out), сессия в куках не очищается, когда пользователь выходит. По этому, если атакующий украдет куки пользователя, он может использовать их для входа даже после того, как пользователь вышел с сайта. Куки будут определены как устаревшие, если только они старее чем SESSION_COOKIE_AGE.

Производительность
------------------
Наконец, размер кук может повлиять на производительность вашего сайта.
Использование сессии в представлениях
-------------------------------------
Когда SessionMiddleware активный, каждый объект HttpRequest – первый аргумент представления в Django – будет содержать атрибут session, который является объектом с интерфейсом словаря.

Вы можете читать и менять request.session в любом месте вашего представления множество раз.

            def __init__(self, request):
                """
                Initialize the cart.
                """
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                if not cart:
                    # save an empty cart in the session
                    cart = self.session[settings.CART_SESSION_ID] = {}
                self.cart = cart

class backends.base.SessionBase
-------------------------------
Это базовый класс для всех объектов сессии. Он предоставляет набор стандартных методов словаря:

__getitem__(key)
Например: fav_color = request.session['fav_color']

__setitem__(key, value)
Например: request.session['fav_color'] = 'blue'

__delitem__(key)
Например: del request.session['fav_color']. Вызовет KeyError, если key еще не в сессии.

__contains__(key)
Например: 'fav_color' in request.session

get(key, default=None)
Например: fav_color = request.session.get('fav_color', 'red')

pop(key)
Например: fav_color = request.session.pop('fav_color')

keys()
items()
setdefault()
clear()

            def clear(self):
                # empty cart
                self.session[settings.CART_SESSION_ID] = {}
                self.session.modified = True

Также содержит следующие методы:
--------------------------------
flush()
Удаляет данные текущей сессии и сессионную куку. Можно использовать, если необходимо убедиться, что старые данные не доступны с браузера пользователя (например, функция django.contrib.auth.logout() вызывает этот метод).

set_test_cookie()
Устанавливает тестовую куку, чтобы проверить, что браузер пользователя поддерживает куки. Из-за особенностей работы кук вы не сможете проверить тестовую куку, пока пользователь не запросит следующую страницу.

test_cookie_worked()
Возвращает True или False, в зависимости от того, принял ли бразуер пользователя тестовую куку. Из-за особенностей работы кук вам необходимо вызывать в предыдущем запросе set_test_cookie().

delete_test_cookie()
Удаляет тестовую куку. Используйте, чтобы убрать за собой.

set_expiry(value)
Указывает время жизни сессии. Вы можете передать различные значения:

Если value целое число, сессия истечет после указанного количества секунд не активности пользователя. Например, request.session.set_expiry(300) установит время жизни равное 5 минутам.

Если value это datetime или timedelta, сессия истечет в указанное время. Обратите внимание, datetime и timedelta сериализуются только при использовании PickleSerializer.

Если value равно 0, сессионная кука удалится при закрытии браузера.

Если value равно None, сессия будет использовать глобальное поведение.

Чтение сессии не обновляет время жизни сессии. Время жизни просчитывается с момента последнего изменения.

            def save(self):
                # update the session cart
                self.session[settings.CART_SESSION_ID] = self.cart
                # mark the session as "modified" to make sure it is saved
                self.session.modified = True

метод __init__
==============
Вызов класса происходит, когда создается объект.
------------------------------------------------
Метод __init__ вызывается сразу после создания экземпляра класса. Соблазнительно, но не правильно называть этот метод конструктором, потому что он выглядит как конструктор (принято, чтобы __init__ был первым методом, определенным в классе), ведет себя как коструктор (это перый кусок кода, вызываемый в созданном экземпляре класса) и даже называется как коструктор. Неправильно, так как к тому времени, когда вызывается метод __init__, объект уже создан и вы имеете ссылку на созданный экземпляр класса. Но метод __init__ — это самое близкое к конструктору, из того что есть в языке Python.

Первым аргументом каждого метода класса, включая __init__, всегда является текущий экземпляр класса. Общепринято всегда называть этот аргумент self. В методе __init__ self ссылается на только что созданный объект, в других методах — на экземпляр класса, для которого метод вызывается. Хотя и необходимо явно указывать self при определении метода, вы его не указываете, когда вызываете метод; Python добавит его автоматически.

Метод __init__ может иметь несколько аргументов. Аргументы могут иметь значения по умолчанию, что сделает их необязательными. В данном случае аргумент filename имеет значение по умолчанию None.

Первый аргумент метода класса (ссылка на текущий экземпляр) принято называть self. Этот аргумент играет роль зарезервированного слова this в C++ и Java, но self не является зарезервированным словом — просто соглашение. Несмотря на это, не стоит называть его иначе, чем self.

Итераторы
=========
Когда вы создаёте список, вы можете считывать его элементы один за другим — это называется итерацией:

            >>> mylist = [1, 2, 3]
            >>> for i in mylist :
            ...    print(i)


Mylist является итерируемым объектом. Когда вы создаёте список, используя генераторное выражение, вы создаёте также итератор:

            >>> mylist = [x*x for x in range(3)]
            >>> for i in mylist :
            ...    print(i)

Всё, к чему можно применить конструкцию «for… in...», является итерируемым объектом: списки, строки, файлы… Это удобно, потому что можно считывать из них значения сколько потребуется — однако все значения хранятся в памяти, а это не всегда желательно, если у вас много значений.

Генераторы
==========
Генераторы это тоже итерируемые объекты, но прочитать их можно лишь один раз. Это связано с тем, что они не хранят значения в памяти, а генерируют их на лету:
            
            >>> mygenerator = (x*x for x in range(3))
            >>> for i in mygenerator :
            ...    print(i)

Всё то же самое, разве что используются круглые скобки вместо квадратных. НО: нельзя применить конструкцию for i in mygenerator второй раз, так как генератор может быть использован только единожды: он вычисляет 0, потом забывает про него и вычисляет 1, завершаяя вычислением 4 — одно за другим.

Yield
=====
Yield это ключевое слово, которое используется примерно как return — отличие в том, что функция вернёт генератор.
            
            >>> def createGenerator() :
            ...    mylist = range(3)
            ...    for i in mylist :
            ...        yield i*i
            ...
            >>> mygenerator = createGenerator() # создаём генератор
            >>> print(mygenerator) # mygenerator является объектом!
            <generator object createGenerator at 0xb7555c34>
            >>> for i in mygenerator:
            ...     print(i)

когда вы вызываете функцию, код внутри тела функции не исполняется. Функция только возвращает объект-генератор

Ваш код будет вызываться каждый раз, когда for обращается к генератору.

В первый запуск функции, она будет исполняться от начала до того момента, когда она наткнётся на yield — тогда она вернёт первое значение из цикла. На каждый следующий вызов будет происходить ещё одна итерация написанного цикла, возвращаться будет следующее значение — и так пока значения не кончатся.

Генератор считается пустым, как только при исполнении кода функции не встречается yield. Это может случиться из-за конца цикла, или же если не выполняется какое-то из условий «if/else».


shop/cart.py
--------------

        from decimal import Decimal
        from django.conf import settings
        from .models import Product

        class Cart(object):

            def __init__(self, request):
                """
                Initialize the cart.
                """
                self.session = request.session
                cart = self.session.get(settings.CART_SESSION_ID)
                if not cart:
                    # save an empty cart in the session
                    cart = self.session[settings.CART_SESSION_ID] = {}
                self.cart = cart

            def __len__(self):
                """
                Count all items in the cart.
                """
                return sum(item['quantity'] for item in self.cart.values())

            def __iter__(self):
                """
                Iterate over the items in the cart and get the products from the database.
                """
                product_ids = self.cart.keys()
                # get the product objects and add them to the cart
                products = Product.objects.filter(id__in=product_ids)
                for product in products:
                    self.cart[str(product.id)]['product'] = product

                for item in self.cart.values():
                    item['price'] = Decimal(item['price'])
                    item['total_price'] = item['price'] * item['quantity']
                    yield item

            def add(self, product, quantity=1, update_quantity=False):
                """
                Add a product to the cart or update its quantity.
                """
                product_id = str(product.id)
                if product_id not in self.cart:
                    self.cart[product_id] = {'quantity': 0,
                                              'price': str(product.price)}
                if update_quantity:
                    self.cart[product_id]['quantity'] = quantity
                else:
                    self.cart[product_id]['quantity'] += quantity
                self.save()

            def remove(self, product):
                """
                Remove a product from the cart.
                """
                product_id = str(product.id)
                if product_id in self.cart:
                    del self.cart[product_id]
                    self.save()

            def save(self):
                # update the session cart
                self.session[settings.CART_SESSION_ID] = self.cart
                # mark the session as "modified" to make sure it is saved
                self.session.modified = True

            def clear(self):
                # empty cart
                self.session[settings.CART_SESSION_ID] = {}
                self.session.modified = True

            def get_total_price(self):
                return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

shop/forms.py
-------------

            from django import forms


            PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


            class CartAddProductForm(forms.Form):
                quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                                  coerce=int)
                update = forms.BooleanField(required=False,
                                            initial=False,
                                            widget=forms.HiddenInput)


shopt/urls.py
-------------

        """shop URL Configuration
        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^cart/$', views.cart_detail, name='cart_detail'),
            url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
            url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),

        ]

shopt/views.py
-------------

        from django.shortcuts import render, get_object_or_404
        from .models import Category, Product
        from .forms import CartAddProductForm


        def product_list(request, category_slug=None):
            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)
            return render(request, 'shop/product/INDEX.html', {'category': category,
                                                              'categories': categories,
                                                              'products': products})

        def product_detail(request, id, slug):
            product = get_object_or_404(Product, id=id, slug=slug, available=True)
            cart_product_form = CartAddProductForm()
            return render(request,
                          'shop/product/detail.html',
                          {'product': product,
                           'cart_product_form': cart_product_form})

Система шаблонов
================

Django использует высокоуровневый API, который не привязан к конкретному бэкенду:

- Для каждого бэкенда DjangoTemplates из настройки the TEMPLATES, Django создает экземпляр Engine. DjangoTemplates оборачивает Engine, чтобы адаптировать его под API конкретного бэкенда шаблонов.
- Модуль django.template.loader предоставляет функции, такие как get_template(), для загрузки шаблонов. Они возвращают django.template.backends.django.Template, который оборачивает django.template.Template.
- Template, полученный на предыдущем шаге, содержит метод render(), который оборачивает контекст и запрос в Context и делегирует рендеринг основному объекту Template.

Настройка бэкенда
------------------

При создании Engine все аргументы должны передаваться как именованные:

- dirs – это список каталого, в которых бэкенд ищет файлы шаблонов. Используется для настройки filesystem.Loader. По умолчанию равен пустому списку.
- app_dirs влияет только на значение loaders по умолчанию. По умолчанию False.
- context_processors – список путей Python для импорта функций, которые используются для наполнения контекста шаблонов, если он рендерится с объектом запроса. Эти функции принимают объект запроса и возвращают dict значений, которые будут добавлены в контекст. По умолчанию равен пустому списку.
- debug – булево значение, которое включает и выключает режим отладки. При True шаблонизатор сохраняет дополнительную отладочную информацию, которая может использоваться для отображения информации ошибки, которая возникла во время рендеринга. По умолчанию False.
- loaders – список загрузчиков шаблонов, указанных строками. Каждый класс Loader знает как загрузить шаблоны из определенного источника. Вместо строки можно указать кортеж. Первым элементом должен быть путь к классу Loader, вторым – параметры, которые будут переданы в Loader при инициализации.
По умолчанию содержит список:
```
'django.template.loaders.filesystem.Loader'
'django.template.loaders.app_directories.Loader', только если app_dirs равен True.
```
- string_if_invalid значение, которые шаблонизатор выведет вместо неправильной переменной(например, с опечаткой в назчании). По умолчанию – пустая строка.
- file_charset – кодировка, которая используется при чтении файла шаблона с диска. По умолчанию 'utf-8'.


shop/views.py
-------------

        from django.shortcuts import render, redirect, get_object_or_404
        from django.views.decorators.http import require_POST
        from .models import Product
        from .cart import Cart
        from .forms import CartAddProductForm


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

Процессоры контекста
====================
список процессоров контекста по умолчанию:
------------------------------------------
1. django.contrib.auth.context_processors.auth
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- user – объект auth.User текущего авторизованного пользователя или объект AnonymousUser, если пользователь не авторизованный).
- perms – объект django.contrib.auth.context_processors.PermWrapper, которые содержит права доступа текущего пользователя.

2. django.template.context_processors.debug
Если включить этот процессор, в RequestContext будут добавлены следующие переменные, но только при DEBUG равном True и, если IP адрес запроса (request.META['REMOTE_ADDR']) указан в INTERNAL_IPS:
- debug – True. Вы можете использовать эту переменную, чтобы определить DEBUG режим в шаблоне.
- sql_queries – список словарей {'sql': ..., 'time': ...}, который содержит все SQL запросы и время их выполнения, которые были выполнены при обработке запроса. Список отсортирован в порядке выполнения SQL запроса.

3. django.template.context_processors.i18n
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- LANGUAGES – значение настройки LANGUAGES.
- LANGUAGE_CODE – request.LANGUAGE_CODE, если существует. Иначе значение LANGUAGE_CODE.

4. django.template.context_processors.media
Если включить этот процессор, в RequestContext будет добавлена переменная MEDIA_URL, которая содержит значение MEDIA_URL.

5. django.template.context_processors.static
Если включить этот процессор, в RequestContext будет добавлена переменная STATIC_URL, которая содержит значение STATIC_URL.

6. django.template.context_processors.csrf
Этот процессор добавляет токен, который используется тегом csrf_token для защиты от CSRF атак.

7. django.template.context_processors.request
Если включить этот процессор, в RequestContext будет добавлена переменная request, содержащая текущий HttpRequest.

8. django.contrib.messages.context_processors.messages
Если включить этот процессор, в RequestContext будут добавлены следующие переменные:
- messages – список сообщений (строки), которые были добавлены с помощью фреймворка сообщений.
- DEFAULT_MESSAGE_LEVELS – словарь приоритетов сообщений и их числовых кодов.

Как создать свой процессор контекста
------------------------------------
Интерфейс процессора контекста - это функция Python, которая принимает один аргумент, объект HttpRequest, и возвращает словарь, которая будет добавлен в контекст шаблона. Процессор контекста обязательно должен возвращать словарь.

Код процессора может находится где угодно. Главное не забыть указать его в опции 'context_processors' настройки:setting:TEMPLATES, или передать аргументом context_processors в Engine.


shop/processors/context_processors.py
-------------------------------------

        from ..cart import Cart

        def cart(request):
            return {'cart': Cart(request) }


settings.py
-----------
        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR, "templates")],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        'shop.processors.context_processors.cart',
                    ],
                },
            },
        ]


shop/product/cart.html
------------------------

        {% extends "base.html" %}
        {% load static %}

        {% block title %}Your shopping cart{% endblock %}

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
            
            <h1>Your shopping cart</h1>
            <table class="cart">
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Remove</th>
                        <th>Unit price</th>                
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                {% for item in cart %}
                    {% with product=item.product %}
                    <tr>
                        <td>
                            <a href="{{ product.get_absolute_url }}">
                                <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                            </a>
                        </td>
                        <td>{{ product.name }}</td>
                        <td>
                            <form action="{% url "shop:cart_add" product.id %}" method="post">
                                {{ item.update_quantity_form.quantity }}
                                {{ item.update_quantity_form.update }}
                                <input type="submit" value="Update">
                                {% csrf_token %}
                            </form>
                        </td>
                        <td><a href="{% url "shop:cart_remove" product.id %}">Remove</a></td>
                        <td class="num">${{ item.price }}</td>
                        <td class="num">${{ item.total_price }}</td>
                    </tr>
                    {% endwith %}
                {% endfor %}
                <tr class="total">
                    <td>Total</td>
                    <td colspan="4"></td>
                    <td class="num">${{ cart.get_total_price }}</td>
                </tr>
                </tbody>
            </table>
            <p class="text-right">
                <a href="{% url "shop:index" %}" class="button light">Continue shopping</a>
                <a href="#" class="button">Checkout</a>
            </p>

         </div>
        </div>
        <hr>

        {% endblock %}


redirect
========
redirect(to, [permanent=False, ]*args, **kwargs)
Возвращает перенаправление(HttpResponseRedirect) на URL указанный через аргументы.

В аргументах можно передать:

- Экземпляр модели: как URL будет использоваться результат вызова метода get_absolute_url().

- Название представления, возможно с аргументами: для вычисления URL-а будет использоваться функция urlresolvers.reverse.

- Абсолютный или относительный URL, который будет использован для перенаправления на указанный адрес.

По умолчанию использует временное перенаправление, используйте аргумент permanent=True для постоянного перенаправления.

Функцию redirect() можно использовать несколькими способами.
------------------------------------------------------------
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
            return redirect('http://example.com/')
По умолчанию, redirect() возвращает временное перенаправление. Все варианты выше принимают аргумент permanent; если передать True будет использоваться постоянное перенаправление:

        def my_view(request):
            ...
            object = MyModel.objects.get(...)
            return redirect(object, permanent=True)

Form.is_valid()
---------------
Главной задачей объекта Form является проверка данных. У заполненного экземпляра Form вызовите метод is_valid() для выполнения проверки и получения её результата:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
Начнём с неправильных данных. В этом случае поле subject будет пустым (ошибка, так как по умолчанию все поля должны быть заполнены), а поле sender содержит неправильный адрес электронной почты:

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False
Form.errors
-----------
Обратитесь к атрибуту errors для получения словаря с сообщениями об ошибках:

        >>> f.errors
        {'sender': ['Enter a valid email address.'], 'subject': ['This field is required.']}
В этом словаре, ключами являются имена полей, а значениями – списки юникодных строк, представляющих сообщения об ошибках. Сообщения хранятся в виде списков, так как поле может иметь множество таких сообщений.

Обращаться к атрибуту errors можно без предварительного вызова методе call is_valid(). Данные формы будут проверены при вызове метода is_valid() или при обращении к errors.

Процедуры проверки выполняются один раз, независимо от количества обращений к атрибуту errors или вызова метода is_valid(). Это означает, что если проверка данных имеет побочное влияние на состояние формы, то оно проявится только один раз.


Доступ к “чистым” данным
========================
Form.cleaned_data
-----------------
Каждое поле в классе Form отвечает не только за проверку, но и за нормализацию данных. Это приятная особенность, так как она позволяет вводить данные в определённые поля различными способами, всегда получая правильный результат.

После создания экземпляра Form, привязки данных и их проверки, вы можете обращаться к “чистым” данным через атрибут cleaned_data:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data
        {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
Следует отметить, что любое текстовое поле, такое как CharField или EmailField, всегда преобразует текст в юникодную строку. Мы рассмотрим применения кодировок далее.

Если данные не прошли проверку, то атрибут cleaned_data будет содержать только значения тех полей, что прошли проверку:

        >>> data = {'subject': '',
        ...         'message': 'Hi there',
        ...         'sender': 'invalid email address',
        ...         'cc_myself': True}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        False
        >>> f.cleaned_data
        {'cc_myself': True, 'message': 'Hi there'}
Атрибут cleaned_data всегда содержит только данные для полей, определённых в классе Form, даже если вы передали дополнительные данные при определении Form. В этом примере, мы передаём набор дополнительных полей в конструктор ContactForm, но cleaned_data содержит только поля формы:

        >>> data = {'subject': 'hello',
        ...         'message': 'Hi there',
        ...         'sender': 'foo@example.com',
        ...         'cc_myself': True,
        ...         'extra_field_1': 'foo',
        ...         'extra_field_2': 'bar',
        ...         'extra_field_3': 'baz'}
        >>> f = ContactForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data # Doesn't contain extra_field_1, etc.
        {'cc_myself': True, 'message': 'Hi there', 'sender': 'foo@example.com', 'subject': 'hello'}
Если Form прошла проверку, то cleaned_data будет содержать ключ и значение для всех полей формы, даже если данные не включают в себя значение для некоторых необязательных полей. В данном примере, словарь данных не содержит значение для поля nick_name, но cleaned_data содержит пустое значение для него:

        >>> from django.forms import Form
        >>> class OptionalPersonForm(Form):
        ...     first_name = CharField()
        ...     last_name = CharField()
        ...     nick_name = CharField(required=False)
        >>> data = {'first_name': 'John', 'last_name': 'Lennon'}
        >>> f = OptionalPersonForm(data)
        >>> f.is_valid()
        True
        >>> f.cleaned_data
        {'nick_name': '', 'first_name': 'John', 'last_name': 'Lennon'}


