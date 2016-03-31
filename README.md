# tdd-django unit_05

методы модели
=============
__unicode__
------------

Метод __unicode__() вызывается когда вы применяете функцию unicode() к объекту. Django использует unicode(obj) (или функцию str(obj)) в нескольких местах. В частности, для отображения объектов в интерфейсе администратора Django и в качестве значения, вставляемого в шаблон, при отображении объекта. 

models.py:
-----------

        from django.db import models

        class Category(models.Model):
            name = models.CharField(max_length=100)
            description = models.TextField(max_length=4096)

            def __unicode__(self):
                return u'%s' % (self.name)


Если вы определили метод __unicode__() и не определили __str__(), Django самостоятельно добавит метод __str__() который вызывает __unicode__(), затем преобразует результат в строку в кодировке UTF-8. Это рекомендуемый подход: определить только __unicode__() и позволить Django самостоятельно преобразовать в строку при необходимости.

__str__
--------

Метод __str__() вызывается когда вы применяете функцию str() к объекту. В Python 3 Django использует str(obj) в нескольких местах. В частности, для отображения объектов в интерфейсе администратора Django и в качестве значения, вставляемого в шаблон, при отображении объекта. 

models.py:
-----------

        from django.db import models

        class Category(models.Model):
            name = models.CharField(max_length=100)
            description = models.TextField(max_length=4096)

            def __str__(self):
                return '%s' % (self.name)

В Python 2 Django использует __str__, если нужно вывести результат функции repr(). Определять метод __str__() не обязательно, если вы определили метод __unicode__().

метод __unicode__() может аналогично использоваться и в __str__():

        from django.db import models
        from django.utils.encoding import force_bytes

        class Category(models.Model):
            name = models.CharField('Categories Name', max_length=100)
            
            description = models.TextField(max_length=4096, default='')

            def __str__(self):
                return force_bytes('%s' % (self.name))


В Python 3, так как все строки являются Unicode строками, используйте только метод __str__(). Если вам необходима совместимость с Python 2, Можете декорировать ваш класс модели декоратором python_2_unicode_compatible().

django.utils.encoding
======================

Django предоставляет простой способ определить __str__() и  __unicode__() методы, которые работают на Python 2 и 3: необходимо определить метод __str__(), возвращающий текст и применить декоратор python_2_unicode_compatible().

В Python 3, декоратор ничего не выполняет. В Python 2, он определяет соответствующие методы  __unicode__() и __str__() ( в процессе замены оригинального __str__()).

python_2_unicode_compatible()
------------------------------

        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible

        @python_2_unicode_compatible
        class Category(models.Model):
            name = models.CharField('Categories Name', max_length=100)
            
            description = models.TextField(max_length=4096, default='')

            def __str__(self):
                return '%s' % (self.name)

        @python_2_unicode_compatible
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
                return '%s' % (self.name)

            def __str__(self):
                return '%s' % (self.title)


SlugField
----------

        class SlugField([max_length=50, **options])

- Slug – газетный термин. “Slug” – это короткое название-метка, которое содержит только буквы, числа, подчеркивание или дефис. В основном используются в URL.
- Как и для CharField, можно указать max_length. Если max_length не указан, Django будет использовать значение 50.
- Устанавливает Field.db_index в True, если аргумент явно не указан.


Вставляем в нашу модель slug:
-----------------------------

        slug = models.SlugField(max_length=200, db_index=True, unique=True)

models.py
---------
        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible

        @python_2_unicode_compatible
        class Category(models.Model):
            name = models.CharField('Categories Name', max_length=100)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)
            description = models.TextField(max_length=4096, default='')

            def __str__(self):
                return self.name

        @python_2_unicode_compatible
        class Product(models.Model):

            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)

            image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
            description = models.TextField(blank=True)
            price = models.DecimalField(max_digits=10, decimal_places=2)
            stock = models.PositiveIntegerField()
            available = models.BooleanField(default=True)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

            def __str__(self):
                return self.name


Параметр unique=True отвечает за то, чтоб название было уникальным.
--------------------------------------------------------------------
## Подключение к админке. 

### ModelAdmin.prepopulated_fields

Обычно значение SlugField создается на основе какого-то другого значения(например, название статьи). Это может работать автоматически в интерфейсе администрации благодаря параметру prepopulated_fields.

prepopulated_fields 
-------------------
позволяет определить поля, которые получают значение основываясь на значениях других полей:

        class CategoryAdmin(admin.ModelAdmin):
            prepopulated_fields = {"slug": ("name",)}

Указанные поля будут использовать код JavaScript для заполнения поля значением на основе значений полей-источников. Основное применение - это генерировать значение для полей SlugField из значений другого поля или полей. Процесс генерирования состоит в объединении значений полей-источников и преобразованию результата в правильный “slug” (например, заменой пробелов на дефисы).

prepopulated_fields не принимает поля DateTimeField, ForeignKey или ManyToManyField.

# Настройки ModelAdmin
ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:

        from django.contrib import admin

        class ProductAdmin(admin.ModelAdmin):
            date_hierarchy = 'updated'

admin.py:
---------

        from django.contrib import admin

        from .models import Category, Product

        class CategoryAdmin(admin.ModelAdmin):

            list_display = ('name', 'slug')
            prepopulated_fields = {"slug": ("name",)}

        admin.site.register(Category,CategoryAdmin)


        class ProductAdmin(admin.ModelAdmin):

            prepopulated_fields = {"slug": ("name",)}

        admin.site.register(Product, ProductAdmin)


API для доступа к данным 
========================

ForeignKey, ManyToManyField и OneToOneField
-------------------------------------------

связь между моделями определяется с помощью ForeignKey.  Django поддерживает все основные типы связей: многие-к-одному, многие-ко-многим и один-к-одному.

Поля отношений
===============
Django предоставляет набор полей для определения связей между моделями.

ForeignKey
-----------

        class ForeignKey(othermodel[, **options])

Связь многое-к-одному. Принимает позиционный аргумент: класс связанной модели.

Для создания рекурсивной связи – объект со связью многое-к-одному на себя – используйте models.ForeignKey('self').

Если вам необходимо добавить связь на модель, которая еще не определена, вы можете использовать имя модели вместо класса:

            from django.db import models

            class Article(models.Model):
                user = models.ForeignKey('User')
                # ...

            class User(models.Model):
                # ...
                pass

Для связи на модель из другого приложения используйте название модели и приложения. Например, если модель User находится в приложении auth, используйте:

        class Article(models.Model):
            user = models.ForeignKey('auth.User')

Такой способ позволяет создать циклическую зависимость между моделями из разных приложений.

В базе данных автоматом создается индекс для ForeignKey. Можно указать для db_index False, чтобы отключить такое поведение. Это может пригодиться, если внешний ключ используется для согласованности данных, а не объединения(join) в запросах, или вы хотите самостоятельно создать альтернативный индекс или индекс на несколько колонок.

Не рекомендуется использовать ForeignKey из приложения без миграций к приложению с миграциями. 

## Представление в базе данных
Django добавляет "_id" к названию поля для создания названия колонки. 

### ForeignKey.related_name
Название, используемое для обратной связи от связанной модели. Также значение по умолчанию для related_query_name (название обратной связи используемое при фильтрации результата запроса). 

Если вы не хотите, чтобы Django создавал обратную связь, установите related_name в '+' или добавьте в конце '+'. Например, такой код создаст связь, но не добавит обратную связь в модель Category:

        category = models.ForeignKey(Category, verbose_name="the related category", related_name='+')

первым аргументом принимает класс модели, поэтому используется keyword аргумент verbose_name
Django не делает первую букву прописной для verbose_name - только там, где это необходимо.

ForeignKey.related_query_name
-----------------------------
Название обратной связи используемое при фильтрации результата запроса. По умолчанию используется related_name, или название модели:

# Declare the ForeignKey with related_query_name

        class Product(models.Model):

            category = models.ForeignKey(Category, related_name='products')
            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)


            def __str__(self):
                return '%s' % (self.name)


## ForeignKey.to_field
Поле связанной модели, которое используется для создания связи между таблицами. По-умолчанию, Django использует первичный ключ.

## ForeignKey.db_constraint
Указывает создавать ли “constraint” для внешнего ключа в базе данных. По умолчанию True и в большинстве случает это то, что вам нужно. Указав False вы рискуете целостностью данных. Некоторые ситуации, когда вам может быть это необходимо:

- Вам досталась в наследство нецелостная база данных
- Вы используете шардинг базы данных.

При False, если связанный объект не существует, при обращении к нему будет вызвано исключение DoesNotExist.

## ForeignKey.on_delete
Когда объект, на который ссылается ForeignKey, удаляется, Django по-умолчанию повторяет поведение ограничения ON DELETE CASCADE в SQL и удаляет объекты, содержащие ForeignKey. Такое поведение может быть переопределено параметром on_delete. Например, если ваше поле ForeignKey может содержать NULL и вы хотите, чтобы оно устанавливалось в NULL после удаления связанного объекта:
```
category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
```
Возможные значения для on_delete находятся в django.db.models:

- CASCADE
Каскадное удаление, значение по умолчанию.

- PROTECT
Препятствует удалению связанного объекта вызывая исключение django.db.models.ProtectedError`(подкласс :exc:`django.db.IntegrityError).

- SET_NULL
Устанавливает ForeignKey в NULL; возможно только если null равен True.

- SET_DEFAULT
Устанавливает ForeignKey в значение по умолчанию; значение по-умолчанию должно быть указано для ForeignKey.

- SET()
Устанавливает ForeignKey в значение указанное в SET(). Если указан выполняемый объект, результат его выполнения. Вызываемый объект можно использовать, чтобы избежать запросов во время импорта 

- DO_NOTHING
Ничего не делать. Если используемый тип базы данных следит за целостностью связей, будет вызвано исключение IntegrityError, за исключением, когда вы самостоятельно добавите SQL правило ON DELETE для поля таблицы (возможно используя загрузочный sql).

## ManyToManyField
class ManyToManyField(othermodel[, **options])

Связь многие-ко-многим. Принимает позиционный аргумент: класс связанной модели. Работает так же как и ForeignKey, включая рекурсивную и ленивую связь.

Связанные объекты могут быть добавлены, удалены или созданы с помощью RelatedManager.

Не рекомендуется использовать ManyToManyField из приложения без миграций к приложению с миграциями.

### Представление в базе данных
Django самостоятельно создаст промежуточную таблицу для хранения связи многое-ко-многим. По-умолчанию, название этой таблицы создается из названия поля и связанной модели. Так как некоторые базы данных не поддерживают длинные названия таблиц, оно будет обрезано до 64 символов и будет добавлен уникальный хеш. Это означает что вы можете увидеть такие названия таблиц author_books_9cdf4; это нормально. Вы можете указать название промежуточной таблицы, используя параметр db_table.

## Параметры
ManyToManyField принимает дополнительные аргументы – все не обязательны – которые определяют как должна работать связь.

- ManyToManyField.related_name
Аналогично ForeignKey.related_name.

- ManyToManyField.related_query_name
Аналогично ForeignKey.related_query_name.

- ManyToManyField.limit_choices_to
Аналогично ForeignKey.limit_choices_to.

- limit_choices_to``не работает для ``ManyToManyField переопределенной через through промежуточной моделью.

## ManyToManyField.symmetrical
Используется только при рекурсивной связи.

## ManyToManyField.through
Django автоматически создает промежуточную таблицу для хранения связи. Однако, если вы хотите самостоятельно определить промежуточную таблицу, используйте параметр through указав модель Django, которая будет хранить связь между моделями.

Обычно используют для хранения дополнительных данных.

Если вы не указали through модель, вы все равно может обратиться к неявно промежуточной модели, которая была автоматически создана. Она содержит три поля, связывающие модели.

Если связанные модели разные, создаются следующие поля:
```
id: первичный ключ для связи.

<containing_model>_id: id модели, которая содержит поле ManyToManyField.

<other_model>_id: id модели, на которую ссылается ManyToManyField.
```
Если ManyToManyField ссылается на одну и ту же модель, будут созданы поля:
```
id: первичный ключ для связи.

from_<model>_id: id объекта основной модели (исходный объект).

to_<model>_id: id объекта, на который указывает связь (целевой объект).
```
Этот класс может использоваться для получения связей.

## ManyToManyField.db_table
Имя промежуточной таблицы для хранения связей многое-ко-многим. Если не указан, Django самостоятельно создаст название по умолчанию используя название таблицы определяющей связь и название поля.

## ManyToManyField.db_constraint
Указывает создавать ли “constraint” для внешних ключей в промежуточной таблице в базе данных. По умолчанию True и в большинстве случает это то, что вам нужно. Указав False вы рискуете целостностью данных. Некоторые ситуации, когда вам может быть это необходимо:

- Вам досталась в наследство нецелостная база данных
- Вы используете шардинг базы данных.

Нельзя указать db_constraint и through одновременно.

## ManyToManyField.swappable

Управляет поведением миграций, если ManyToManyField ссылается на подменяемую(swappable) модель. При True - значение по умолчанию - если ManyToManyField ссылается на модель, указанную через settings.AUTH_USER_MODEL (или другую настройку, определяющую какую модель использовать), связь в миграции будет использовать настройку, а не саму модель.

Вам может понадобится значение False только, если связь должна указывать на какую-то конкретную модель, игнорируя настройку - например, если это модель профиля пользователя для какой-то конкретной модели пользователя и не будет работать с любой моделью из настройки.

Если вы не уверены какое значение выбрать, используйте значение по умолчанию True.

## ManyToManyField.allow_unsaved_instance_assignment

Работает аналогично ForeignKey.allow_unsaved_instance_assignment.

ManyToManyField не поддерживает validators.

null не влияет на работу поля т.к. нет способа сделать связь обязательной на уровне базы данных.

shop/models.py
--------------
        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible

        @python_2_unicode_compatible
        class Category(models.Model):
            name = models.CharField('Categories Name', max_length=100)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)
            description = models.TextField(max_length=4096, default='')

            def __str__(self):
                return self.name

        @python_2_unicode_compatible
        class Product(models.Model):

            category = models.ForeignKey(Category, related_name='products')
            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)

            image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
            description = models.TextField(blank=True)
            price = models.DecimalField(max_digits=10, decimal_places=2)
            stock = models.PositiveIntegerField()
            available = models.BooleanField(default=True)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

            def __str__(self):
                return self.name


Функция get_object_or_404()
----------------------------

Одна из распространенных идиом – вызвать метод get() и возбудить исключение Http404, если объект не существует. Она инкапсулирована в функции get_object_or_404(), которая принимает в первом аргументе модель Django, а также произвольное количество именованных аргументов, которые передает функции get() менеджера, подразумеваемого по умолчанию. Если объект не существует, функция возбуждает исключение Http404. 
Например:

Получить объект Category с первичным ключом 3 

        category = get_object_or_404(Category, pk=3)

Когда этой функции передается модель, для выполнения запроса get() она использует менеджер, подразумеваемый по умолчанию. 

shop/views.py:
--------------

def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise Http404("Product does not exist")
    return render(request,
                          'shop/product/detail.html',
                          {'product': product})

shop/views.py:
--------------

from django.shortcuts import get_object_or_404, render

        def product_detail(request, id):
            product = get_object_or_404(Product, id=id, available=True)
            
            return render(request,
                          'shop/product/detail.html',
                          {'product': product})

shop/views.py
-------------
        from django.shortcuts import render, get_object_or_404
        from .models import Product

        def index(request, category_slug=None):
            category = None
            categories = Category.objects.all()
            products = Product.objects.filter(available=True)
            if category_slug:
                category = get_object_or_404(Category, slug=category_slug)
                products = products.filter(category=category)
            return render(request, 'shop/product/index.html', {'category': category,
                                                              'categories': categories,
                                                              'products': products})


        def product_detail(request, id, slug):
            product = get_object_or_404(Product, id=id, slug=slug, available=True)
            
            return render(request,
                          'shop/product/detail.html',
                          {'product': product})

shop/urls.py
------------
        """shop URL Configuration

        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
        ]

get_absolute_url
=================
        Model.get_absolute_url()
Определите метод get_absolute_url(), чтобы указать Django как вычислить URL для объекта. Метод должен вернуть строку, которая может быть использована в HTTP запросе.

        def get_absolute_url(self):
            return "/people/%i/" % self.id
(Хотя это код правильный и простой, но такой подход не самый лучший для создания подобных методов. Лучше использовать функцию reverse().)

        def get_absolute_url(self):
            from django.core.urlresolvers import reverse
            return reverse('people.views.details', args=[str(self.id)])

Django использует get_absolute_url() в интерфейсе администратора. Если объект содержит этот метод, страница редактирования объекта будет содержать ссылку “Показать на сайте”, которая приведет к странице отображения объекта, ссылку на которую возвращает get_absolute_url().

Кроме того, несколько приложений Django также используют этот метод, например syndication feed framework. Если объект модели представляет какой-то уникальный URL, вам стоит определить метод get_absolute_url().

При создания URL не используйте непроверенные данные от пользователя, чтобы избежать подделки ссылок или перенаправлений:

        def get_absolute_url(self):
            return '/%s/' % self.name
Если self.name равен '/example.com', будет возвращен '//example.com/', являющимся правильным URL-ом относительно протокола, вместо ожидаемого '/%2Fexample.com/'.


shop/models.py
--------------

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

            category = models.ForeignKey(Category, related_name='products')
            name = models.CharField(max_length=200, db_index=True)
            slug = models.SlugField(max_length=200, db_index=True, unique=True)

            image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
            description = models.TextField(blank=True)
            price = models.DecimalField(max_digits=10, decimal_places=2)
            stock = models.PositiveIntegerField()
            available = models.BooleanField(default=True)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True, help_text="Please use the following format: <em>YYYY-MM-DD</em>.")

            def __str__(self):
                return self.name

            def get_absolute_url(self):
                return reverse('shop:product_detail', args=[self.id, self.slug])

get_absolute_url() в шаблонах
------------------------------
вместо того, чтобы “хардкодить” URL-ы. Например, это плохой подход:

        <!-- BAD template code. Avoid! -->
        <a href="/shop/{{ object.id }}/">{{ object.name }}</a>

Этот шаблон значительно лучше:

        <a href="{{ object.get_absolute_url }}">{{ object.name }}</a>

Идея в том что, если вы измените структуру URL-а для объекта, или просто исправите опечатку, вам не нужно исправлять его во всех местах, где этот URL используется. Просто определите его один раз в методе get_absolute_url(), и пусть остальной код использует его.

Строка, которую возвращает get_absolute_url(), должна состоять только из ASCII символов (требуется спецификацией URI, RFC 2396) и быть закодированной для URL, если необходимо.

Код и шаблоны, использующие get_absolute_url(), должны иметь возможность использовать результат без обработки. Вы можете использовать функцию django.utils.encoding.iri_to_uri(), если используете unicode-строку, которая содержит не ASCII символы.


templates/shop/product/index.html
---------------------------------
        {% extends "base.html" %}
        {% load static %}
        {% block title %}Products {% endblock %}

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
                    <h1>{% if category %}{{ category.name }}{% else %}Products{% endif %}</h1>
                {% for product in products %}
                    <div class="item">
                        <a href="{{ product.get_absolute_url }}">
                            <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                        </a>
                        <a href="{{ product.get_absolute_url }}">{{ product.name }}</a><br>
                        ${{ product.price }}
                    </div>
                {% endfor %}
                
                </div>
              </div>
             <hr>
        {% endblock %}

templates/shop/product/detail.html
----------------------------------
        
        {% extends "base.html" %}
        {% load static %}

        {% block title %}{{ product.name }}{% endblock %}

        {% block content %}
            <div class="product-detail">
                <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
                <h1>{{ product.name }}</h1>
                <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
                <p class="price">${{ product.price }}</p>
                
                {{ product.description|linebreaks }}
            </div>
        {% endblock %}


STATUS_CHOICES
============== 

choices
-------
Итератор (например, список или кортеж) 2-х элементных кортежей, определяющих варианты значений для поля. При определении, виджет формы использует select вместо стандартного текстового поля и ограничит значение поля указанными значениями.

Список значений выглядит:
-------------------------

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sale', 'For Sale'),
        ('onstock', 'On Stock'),
        ('notavailbl', 'Not Available'),
    )


Первый элемент в кортеже - значение хранимое в базе данных, второй элемент - отображается виджетом формы, или в ModelChoiceField. Для получения отображаемого значения используется метод get_status_display экземпляра модели. Значения лучше указать в константах внутри модели:

        from django.db import models

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

            def __str__(self):
                return self.name

            def get_absolute_url(self):
                return reverse('shop:product_detail', args=[self.id, self.slug])


Значение по умолчанию для этого поля. 
-------------------------------------
Это может быть значение или функция. Если это функция - она будет вызвана при каждом создании объекта.

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('sale', 'For Sale'),
        ('onstock', 'On Stock'),
        ('notavailbl', 'Not Available'),
    )
           
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    

ModelAdmin.fields
==================
Если вам необходимо внести небольшие изменения форму на странице редактирования и добавления, например, изменить список отображаемых полей, их порядок или сгруппировать их, вы можете использовать настройку fields (сложные изменения можно выполнить используя настройку fieldsets). 

порядок полей в форме. 
----------------------

        class ProductAdmin(admin.ModelAdmin):

            list_display = ('name', 'updated')
            fields = ['name','category','description','created','updated','status']
            
            prepopulated_fields = {"slug": ("name",)}

        admin.site.register(Product, ProductAdmin)

fields может содержать поля указанные в ModelAdmin.readonly_fields, они не будут доступны для редактирования.

Параметр fields, в отличии от list_display, может содержать только названия полей модели или полей определенных в form. Можно указать названия функций, если они указаны в readonly_fields.

Чтобы поля отображались в одной строке, укажите их в кортеже вместе.

        fieldsets = [
                ('Item',             {'fields': [('name','slug'),'category','description']}),
                ('Date information', {'fields': [('created','updated')], 'classes': ['collapse']}),
                ('Medias',           {'fields': ['image']}),
                ('Metas',            {'fields': [('status','price','stock']}),
            ]


Первый элемент кортежа в fieldsets – название группы полей.

Если не определен ни атрибут fields, ни fieldsets, Django покажет все поля с editable=True кроме AutoField, в одном наборе полей в порядке, в котором они указанные в модели.

Словарь field_options может содержать следующие ключи:
-------------------------------------------------------
- fields
--------
Кортеж с названиями полей. Этот ключ обязателен.

        {'fields': [('title','slug'),'category','content']}),

Как и в атрибуте fields, чтобы отобразить поля в одной строке, добавьте их в один кортеж. 

fields может содержать значения из ModelAdmin.readonly_fields, чтобы отображать поля без возможности их редактирования.

Добавление функции в fields аналогично добавлению в параметр fields - функция должна быть указанна в readonly_fields.
- classes
---------
Список содержащий CSS классы, которые будут добавлены в группу полей.

        {
        'classes': ('wide', 'extrapretty'),
        }

Django предоставляет два класса для использования: collapse и wide. Группа полей с классом collapse будет показа в свернутом виде с кнопкой “развернуть”. Группа полей с классом wide будет шире по горизонтали.

- description
-------------
Необязательный текст, который будет отображаться под названием группы полей. Этот текст не отображается для TabularInline.

текст не будет экранирован. Это позволяет добавить HTML на страницу.

добавить HTML классы для каждой группы полей. 
---------------------------------------------
класс "collapse", который отображает группу полей изначально скрытой. Это полезно, если форма содержит поля, которые редко редактируются:

            fieldsets = [
                ('Item',             {'fields': [('name','slug'),'category','description']}),

                ('Date information', {'fields': [('created','updated')], 'classes': ['collapse']}),

                ('Medias',           {'fields': ['image']}),
                ('Metas',            {'fields': [('status','price','stock']}),
            ]

### ModelAdmin.list_display_links
Используйте list_display_links, чтобы указать какие поля в list_display будут ссылками на страницу редактирования объекта.

По умолчанию, на страницу редактирования объекта будет вести ссылка в первой колонке – первое поле в list_display. Но list_display_links позволяет изменить это поведение:

Можно указать None, чтобы убрать ссылки.

Укажите список или кортеж полей (так же как и в list_display) чьи колонки должны быть ссылками на страницу редактирования.

Вы можете указывать одно или несколько полей. Пока указанные поля входят в list_display, Django безразлично сколько их. Единственное требование: для использования list_display_links вы должны указать list_display.


    class CategoryAdmin(admin.ModelAdmin):

        list_display = ('name', 'slug')
        list_display_links = ('name',)

В этом примере список объектов будет без ссылок:

    class CategoryAdmin(admin.ModelAdmin):

        list_display = ('name', 'slug')

        list_display_links = None


## ModelAdmin.readonly_fields
По умолчанию интерфейс администратора отображает все поля как редактируемые. Поля указанные в этой настройке (которая является list или tuple) будут отображаться значение без возможности редактировать, они также будут исключены из ModelForm используемой для создания и редактирования объектов. Однако, если вы определяете аргумент ModelAdmin.fields или ModelAdmin.fieldsets поля для чтения должны быть в них указаны (иначе они будут проигнорированы).

Если readonly_fields используется без определения порядка полей через атрибуты ModelAdmin.fields или ModelAdmin.fieldsets, поля из этой настройки будут отображаться после редактируемых полей.


        readonly_fields = ('created','updated')

Добавление связанных объектов
=============================

Django знает, что поле ForeignKey должно быть представлено как select. 

Обратите внимание на ссылку “Add Another category” возле поля Category. При нажатии на “Add Another category” будет показано всплывающее окно с формой добавления category. 

Настройка страницы списка объектов
----------------------------------
По умолчанию Django отображает результат выполнения str() для каждого объекта. Но чаще всего хочется показывать список полей. Для этого используйте параметр list_display, который является кортежем состоящим из названий полей модели:


    list_display = ('name', 'updated', 'status')


ModelAdmin.list_filter
======================
Укажите list_filter, чтобы определить фильтры данных в правой панели страницы списка объектов

list_filter - это список элементов, которые могу быть одного из следующих типов:
--------------------------------------------------------------------------------
- название поля следующего типа: BooleanField, CharField, DateField, DateTimeField, IntegerField, ForeignKey или ManyToManyField.:


        list_filter = ['updated']

Это добавляет “Фильтр” по полю updated в боковой панели

Тип фильтра зависит от типа поля. Так как updated является DateTimeField, Django отображает соответствующие варианты для фильтрации: “Any date,” “Today,” “Past 7 days,” “This month,” “This year.”


добавим поиск:
--------------

    search_fields = ['name']

Это добавляет поле для поиска в верхней части страницы. При вводе запроса, Django будет искать по полю name. Вы можете использовать любое количество полей – используется запрос LIKE, так что постарайтесь не перегрузить вашу базу данных.

Страница списка объектов также содержит постраничное отображение. По умолчанию отображается 100 объектов на страницу. 


admin.py:
---------

        cfrom django.contrib import admin

        from .models import Category, Product

        class CategoryAdmin(admin.ModelAdmin):

            list_display = ('name', 'slug')
            list_display_links = ('name',)
            search_fields = ['name', 'slug', 'description']
            prepopulated_fields = {"slug": ("name",)}

        admin.site.register(Category,CategoryAdmin)


        class ProductAdmin(admin.ModelAdmin):

            list_display = ('name', 'updated')
            list_filter = ['updated']
            search_fields = ['name']
            ordering = ['updated']
            prepopulated_fields = {"slug": ("name",)}
            date_hierarchy = 'updated'

        admin.site.register(Product, ProductAdmin)


Именованные группы
===================
Для регулярных выражений в Python синтаксис для именованных совпадений выглядит таким образом

     (?P<name>pattern)

где name это название группы, а pattern – шаблон.

Комбинирование URLconfs
=======================
В любой момент, ваш urlpatterns может “включать” другие модули URLconf.

mysite/urls.py
--------------
        from django.conf.urls import url, include
        from django.contrib import admin

        from home import views

        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^admin/', admin.site.urls),
        ]

регулярные выражения не содержат $ (определитель конца строки), но содержит косую черту в конце. Каждый раз, когда Django встречает include() (django.conf.urls.include()), из URL обрезается уже совпавшая часть, остальное передается во включенный URLconf для дальнейшей обработки.

shop/urls.py
------------
        """shop URL Configuration
        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
        ]

Что использует URLconf при поиске нужного шаблона URL
------------------------------------------------------
- URLconf использует запрашиваемый URL как обычную строку Python. Он не учитывает параметры GET, POST и имя домена.
URLconf не учитывает тип запроса. POST, GET, HEAD, и др. – будут обработаны одним представлением при одинаковом URL.

Найденные аргументы – всегда строки
------------------------------------
Каждый найденный аргумент передается в представление как строка, независимо от того, какое совпадение определено в регулярном выражении. Например, URLconf содержит такую строку:

            url(r'^(?P<id>\d+)/$', views.product_detail, name='product_detail'),

аргумент id для views.product_detail() будет строкой, несмотря на то, что d+ отлавливает только числа.

MEDIA
=====

MEDIA_URL
=========
По умолчанию: '' (Пустая строка)

URL который указывает на каталог MEDIA_ROOT, используется для работы с файлами. Должен оканчиваться слешом при не пустом значении. Вам необходимо настроить раздачу этих файлов как dev-сервером, так и боевым.

Если вы хотите использовать {{ MEDIA_URL }} в шаблонах, добавьте 'django.template.context_processors.media' в опцию 'context_processors' настройки TEMPLATES.

Например: "http://media.example.com/"

MEDIA_URL и STATIC_URL должны отличаться.

MEDIA_ROOT
==========
По умолчанию: '' (Пустая строка)

Абсолютный путь к каталогу, в котором хранятся медиа-файлы, используется для работы с файлами.

Например: "/var/www/example.com/media/"

MEDIA_ROOT и STATIC_ROOT должны отличаться. Когда STATIC_ROOT только добавили, нормальным было указать MEDIA_ROOT на те самые файлы, однако, т.к. это потенциально не безопасно, добавлена проверка этих значений.

mysite/settiings.py
-------------------

        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

mysite/urls.py
--------------
        from django.conf.urls import url, include
        from django.contrib import admin
        from django.conf import settings
        from django.conf.urls.static import static

        from home import views

        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^admin/', admin.site.urls),
        ]
        if settings.DEBUG:
            urlpatterns += static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)


Раздача файлов, загруженных пользователем, при разработке
---------------------------------------------------------
При разработке медиа файлы из MEDIA_ROOT можно раздавать используя представление django.contrib.staticfiles.views.serve().

Не используйте его на боевом сервере!

Например, если MEDIA_URL равна /media/, вы можете добавить следующий код в urls.py:

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Это представление работает только при включенной отладке и для локальных префиксов (например /media/), а не полных URL-ов (e.g. http://media.example.com/).

Раздача статических файлов при разработке.
------------------------------------------
Если вы используете django.contrib.staticfiles, runserver все сделает автоматически, если DEBUG равна True. Если django.contrib.staticfiles не добавлено в INSTALLED_APPS, вы можете раздавать статические файлы используя представление django.contrib.staticfiles.views.serve().

Не используйте его на боевом сервере!

Например, если STATIC_URL равна /static/, вы можете добавить следующий код в urls.py:

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

Это представление работает только при включенной отладке и для локальных префиксов (например /static/), а не полных URL-ов (e.g. http://static.example.com/).

Также эта функция раздает файлы из каталога STATIC_ROOT не выполняя поиск всех статических файлов, как это делает django.contrib.staticfiles.

Настройка статики
=================
Убедитесь что django.contrib.staticfiles добавлено INSTALLED_APPS.

В настройках укажите STATIC_URL, например:

        STATIC_URL = '/static/'
В шаблоне или “захардкодьте” URL /static/my_app/myexample.jpg, или лучше использовать тег static для генерация URL-а по указанному относительному пути с использованием бэкенда, указанного в STATICFILES_STORAGE (это позволяет легко перенести статические файлы на CDN).

        {% load staticfiles %}
        <img src="{% static "my_app/myexample.jpg" %}" alt="My image"/>
Сохраните статические файлы в каталоге static вашего приложения. Например my_app/static/my_app/myimage.jpg.

Раздача файлов
--------------
Кроме конфигурации, необходимо настроить раздачу статических файлов.

При разработке, если вы используете django.contrib.staticfiles, это все происходит автоматически через runserver, при DEBUG равной True. Оно предназначено только для разработки, и не должно использоваться на боевом сервере.

Ваш проект, возможно, будет содержать статические файлы, которые не относятся ни к одному из приложений. Настройка STATICFILES_DIRS указывает каталоги, которые проверяются на наличие статических файлов. По умолчанию эта настройка пустая. Например:

        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
            '/var/www/static/',
        )
Пространства имен для статических файлов
----------------------------------------
Вы можете добавлять статические файлы непосредственно в каталог my_app/static/ (не создавая подкаталог my_app), но это плохая идея. Django использует первый найденный по имени файл и, если у вас есть файлы с одинаковым названием в разных приложениях, Django не сможет использовать оба. Необходимо как-то указать, какой файл использовать, и самый простой способ – это пространство имен. Просто положите их в каталог с названием приложения(my_app/static/my_app).