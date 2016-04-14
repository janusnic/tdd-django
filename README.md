# tdd-django unit_09

Настройки ModelAdmin
=====================
ModelAdmin очень гибкий. Он содержит ряд параметров для настройки интерфейса администратора. Все настройки определяются в подклассе ModelAdmin:

        from django.contrib import admin

        class ProductAdmin(admin.ModelAdmin):

            list_filter = ['updated']
            search_fields = ['name']
            ordering = ['updated']
            readonly_fields = ('created','updated')
            fieldsets = [
                        ('Item',             {'fields': [('name','slug'),'category']}),
                        ('Date information', {'fields': [('created','updated')], 'classes': ['collapse']}),
                        ('Description',      {'fields': ['description']}),
                        ('Medias',           {'fields': ['image']}),
                        ('Metas',            {'fields': ['status','price','stock']}),
                    ]
            prepopulated_fields = {"slug": ("name",)}
            date_hierarchy = 'updated'


## ModelAdmin.actions
Список действий, которые будут включены на странице списка объектов. 

Повседневный алгоритм работы с административным интерфейсом Django выглядит как “выделить объект, затем изменить его.” Он подходит для большинства случаев. Тем не менее, когда потребуется выполнить одно и то же действие над множеством объектов.

В таких случаях административный интерфейс Django позволяет вам создать и зарегистрировать “действия” – простые функции, которые вызываются для выполнения неких действий над списком объектов, выделенных на странице интерфейса.

Если вы взгляните на любой список изменений на интерфейсе администратора, вы увидите эту возможность в действии. Django поставляется с действием “удалить выделенные объекты”, которое доступно для всех моделей. 

Создание действий
==================
Общим способом использования действий в интерфейсе администратора является пакетное изменение модели. 

class Product:
--------------

        @python_2_unicode_compatible
        class Product(models.Model):
            
            STATUS_CHOICES = (
                ('available', 'Available'),
                ('sale', 'For Sale'),
                ('onstock', 'On Stock'),
                ('notavailbl', 'Not Available'),
            )
           
            status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
            created = models.DateTimeField(auto_now_add=True)



Стандартной задачей, которую мы будем выполнять с подобной моделью, будет изменение состояний с 'Not Available' на Available. 

## Создание функций для действий
Сначала нам потребуется написать функцию, которая вызывается при выполнении действия в интерфейсе администратора. Функции действий - это обычные функции, которые принимают три аргумента:

- Экземпляр класса ModelAdmin,
- Экземпляр класса HttpRequest, представляющий текущий запрос,
- Экземпляр класса QuerySet, содержащий набор объектов, которые выделил пользователь.

Наша функция make_availabled не нуждается в экземпляре ModelAdmin или в объекте реквеста, но использует выборку:

        def make_availabled(modeladmin, request, queryset):
            queryset.update(status='available')


В целях улучшения производительности, мы используем метод выборки update method. Другие типы действий могут обрабатывать каждый объект индивидуально. В таких случаях мы просто выполняем итерацию по выборке:

        for obj in queryset:
            do_something_with(obj)


Обеспечим действие “красивым” заголовком, который будет отображаться в интерфейсе администратора. По умолчанию, это действие будет отображено в списке действий как “Make availabled”, т.е. по имени функции, где символы подчёркивания будут заменены пробелами. 

make_availabled атрибут short_description:

        def make_availabled(modeladmin, request, queryset):
            queryset.update(status='available')
        make_availabled.short_description = "Mark selected products as availabled"

Добавление действий в класс ModelAdmin
---------------------------------------
Затем мы должны проинформировать наш класс ModelAdmin о новом действии. Это действие аналогично применению любой другой опции конфигурации. Таким образом, полный пример admin.py с определением действия и его регистрации будет выглядеть так:


        def make_availabled(modeladmin, request, queryset):
            queryset.update(status='available')
        make_availabled.short_description = "Mark selected products as availabled"


        class ProductAdmin(admin.ModelAdmin):

            list_filter = ['updated']
            search_fields = ['name']
            ordering = ['updated']
            readonly_fields = ('created','updated')
            fieldsets = [
                        ('Item',             {'fields': [('name','slug'),'category']}),
                        ('Date information', {'fields': [('created','updated')], 'classes': ['collapse']}),
                        ('Description',      {'fields': ['description']}),
                        ('Medias',           {'fields': ['image']}),
                        ('Metas',            {'fields': ['status','price','stock']}),
                    ]
            prepopulated_fields = {"slug": ("name",)}
            date_hierarchy = 'updated'

            actions = [make_availabled,]


Обработка ошибок в действиях
-----------------------------
При наличии предполагаемых условий возникновения ошибки, которая может возникнуть во время работы вашего действия, вы должны аккуратно проинформировать пользователя о проблеме. Это подразумевает обработку исключений и использование метода django.contrib.admin.ModelAdmin.message_user() для отображения описания проблемы в отклике.

Действия как методы ModelAdmin
------------------------------
так как действия связано с объектом Product, то правильнее будет внедрить это действие в сам объект ProductAdmin.

        class ProductAdmin(admin.ModelAdmin):
            ...

            actions = [make_availabled, 'make_not_availabled']

            def make_not_availabled(self, request, queryset):
                queryset.update(status=DRAFT)
            make_not_availabled.short_description = "Mark selected products as not availabled"

это указывает классу ModelAdmin искать действие среди своих методов.

Определение действий в виде методов предоставляет действиям более прямолинейный, идеоматический доступ к самому объекту ModelAdmin, позволяя вызывать любой метод, предоставляемый интерфейсом администратора.

мы можем использовать self для вывода сообщения для пользователя в целях его информирования об успешном завершении действия:

        class ProductAdmin(admin.ModelAdmin):
            ...

            actions = [make_availabled, 'make_not_availabled', 'make_for_sale']

            def make_not_availabled(self, request, queryset):
                queryset.update(status=DRAFT)
            make_not_availabled.short_description = "Mark selected products as not availabled"

            def make_for_sale(self, request, queryset):
                rows_updated = queryset.update(status='sale')
                if rows_updated == 1:
                    message_bit = "1 product was"
                else:
                    message_bit = "%s products were" % rows_updated
                self.message_user(request, "%s successfully marked as for sale." % message_bit)
            make_for_sale.short_description = "Mark selected stories as for sale"


Это обеспечивает действие функционалом, аналогичным встроенным возможностям интерфейса администратора

Отключение действий
--------------------
Иногда требуется отключать определённые действия, особенно зарегистрированные глобально, для определённых объектов. Существует несколько способов для этого:

Отключение глобального действия
--------------------------------
#### AdminSite.disable_action(name)
Если требуется отключить глобальное действие, вы можете вызвать метод AdminSite.disable_action().

Например, вы можете использовать данный метод для удаления встроенного действия “delete selected objects”:

        admin.site.disable_action('delete_selected')

После этого действие больше не будет доступно глобально.

Тем не менее, если вам потребуется вернуть глобально отключенное действия для одной конкретной модели, просто укажите это действия явно в списке ModelAdmin.actions:


        # Globally disable delete selected
        admin.site.disable_action('delete_selected')

        # This ModelAdmin will not have delete_selected available
        class SomeModelAdmin(admin.ModelAdmin):
            actions = ['some_other_action']
            ...

        # This one will
        class AnotherModelAdmin(admin.ModelAdmin):
            actions = ['delete_selected', 'a_third_action']
            ...

Отключение всех действия для определённого экземпляра ModelAdmin
-----------------------------------------------------------------
Если вам требуется запретить пакетные действия для определённого экземпляра ModelAdmin, просто установите атрибут ModelAdmin.actions в None:

        class MyModelAdmin(admin.ModelAdmin):
            actions = None

Это укажет экземпляру ModelAdmin не показывать и не позволять выполнения никаких действий, включая зарегистрированные глобально.

Условное включение и отключение действий
----------------------------------------
### ModelAdmin.get_actions(request)
Наконец, вы можете включать или отключать действия по некоему условию на уровне запроса (и, следовательно, на уровне каждого пользователя), просто переопределив метод ModelAdmin.get_actions().

Он возвращает словарь разрешённых действий. Ключами являются имена действий, а значениями являются кортежи вида (function, name, short_description).

Чаще всего вы будете использовать данный метод для условного удаления действия из списка, полученного в родительском классе. Например, если мне надо разрешить пакетное удаление объектов только для products с именами, начинающимися с буквы ‘S’:

        class ProductAdmin(admin.ModelAdmin):
            ...

            def get_actions(self, request):
                actions = super(ProductAdmin, self).get_actions(request)
                if request.product.name[0].upper() != 'S':
                    if 'delete_selected' in actions:
                        del actions['delete_selected']
                return actions


Действие “удалить выделенные объекты” использует метод QuerySet.delete() по соображениям эффективности, который имеет важный недостаток: метод delete() вашей модели не будет вызван.

Если вам потребуется изменить такое поведение, то просто напишите собственное действие, которое выполняет удаление в необходимой вам манере, например, вызывая Model.delete() для каждого выделенного элемента.

### ModelAdmin.actions_on_top
### ModelAdmin.actions_on_bottom
Определяет где на странице будет расположены панели с действиями. По умолчанию эта панель расположена сверху (actions_on_top = True; actions_on_bottom = False).

### ModelAdmin.actions_selection_counter
Указывает отображать ли счетчик выбранных объектов после списка действий. По умолчанию он отображается (actions_selection_counter = True).

### ModelAdmin.date_hierarchy
Укажите в date_hierarchy название DateField или DateTimeField поля вашей модели, и страница списка объектов будет содержать навигацию по датам из этого поля.

        date_hierarchy = 'updated'

Навигация учитывает значения поля, например, если все значения будут датами из одного месяца, будут отображаться только дни этого месяца.

date_hierarchy использует внутри QuerySet.datetimes() (USE_TZ = True).

## ModelAdmin.formfield_overrides
Позволяет быстро изменить настройки отображения различных типов Field в интерфейсе администратора. formfield_overrides – словарь указывающий параметры для классов полей, которые будут передаваться в конструкторы указанных полей.

Model
-----

    def was_updated_recently(self):
        return self.updated >= timezone.now() - datetime.timedelta(days=1)
    was_updated_recently.admin_order_field = 'updated'
    was_updated_recently.boolean = True
    was_updated_recently.short_description = 'Updated recently?'


admin
------

        class ProductAdmin(admin.ModelAdmin):

            list_display = ('name', 'updated', 'was_updated_recently')
            list_filter = ['updated']
            search_fields = ['name']
            ordering = ['updated']


Постраничный вывод - Paginator
==============================

Django предоставляет несколько классов, которые помогают реализовать постраничный вывод данных, т.е. данных, распределённых на несколько страниц с ссылками «Предыдущая/Следующая». Эти классы располагаются в django/core/paginator.py.

вы можете передать классу Paginator список/кортеж, QuerySet Django или любой другой объект, который имеет методы count() или __len__(). Для определения количества объектов, содержащихся в переданном объекте, Paginator сначала попробует вызвать метод count(), затем, при его отсутствии, вызывает len(). Такой подход позволяет объектам, подобным QuerySet, более эффективно использовать метод count() при его наличии.

Использование Paginator в представлении
---------------------------------------

        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
                products = products.filter(category=category)
            return render(request, 'shop/product/index.html', {'category': category,
                                                              'categories': categories,
                                                              'products': products})


В шаблоне index.html подключен блок навигации по страницам:

         <!-- Next/Prev page links  --> 
          {% if products.object_list and products.paginator.num_pages > 1 %} 
            <div class="pagination" style="margin-top: 20px; margin-left: -20px; "> 
                <span class="step-links"> 
                    {% if products.has_previous %} 
                        <a href= "?page={{ products.previous_page_number }}">newer entries &lt;&lt; </a> 
                    {% endif %} 

                    <span class="current"> 
                        &nbsp;Page {{ products.number }} of {{ products.paginator.num_pages }} 
                    </span> 

                    {% if products.has_next %} 
                        <a href="?page={{ products.next_page_number }}"> &gt;&gt; older entries</a> 
                    {% endif %} 
                </span> 
            </div> 
           {% endif %}


Объекты Paginator
------------------
У класса Paginator есть конструктор:

        class Paginator(object_list, per_page, orphans=0, allow_empty_first_page=True)

Обязательные аргументы
----------------------
- object_list
Список, кортеж, Django QuerySet, или другой контейнер, у которого есть метод count() или``__len__()``.

- per_page
Максимальное количество элементов на странице, без учёта остатка.

Необязательные аргументы
------------------------
- orphans
Минимальное количество элементов на последней странице, по умолчанию, ноль. Используйте, когда нежелательно отображать последнюю страницу почти пустой. Если последняя страница будет содержать количество элементов меньше или равно orphans, то эти элементы будут добавлены к предыдущей странице (которая станет последней). Например, для 23 элементов, per_page=10``и ``orphans=3, будет выдано две страницы; первая страница будет содержать 10 элементов, а вторая (и последняя) — 13.

- allow_empty_first_page
Позволять или нет первой странице быть пустой. Если указан False и object_list пустой, то будет вызвано исключение EmptyPage.

Методы
-------
- Paginator.page(number)
Возвращает объект Page по переданному индексу (начинается с единицы). Вызывает исключение InvalidPage, если указанная страница не существует.

Атрибуты
---------
- Paginator.count
Общее количество объектов, распределенных по всем страницам.

При определении количества объектов, содержащихся в object_list, Paginator сначала пробует вызвать object_list.count(). Если у object_list нет метода count(), то Paginator попробует вызвать len(object_list). Такой подход позволяет объектам, подобным QuerySet Django, более эффективно использовать метод count() при его наличии.

- Paginator.num_pages
Общее количество страниц.

- Paginator.page_range
Диапазон номеров страниц, начинающийся с единицы, т.е., [1, 2, 3, 4].

InvalidPage исключения
----------------------
- exception InvalidPage
Базовый класс для исключений, которые вызываются когда происходит запрос страницы по несуществующему номеру.

Метод Paginator.page() вызывает исключение, если номер запрошенной страницы является неправильным (например, не представлен целым числом) или не содержит объектов. В общем случае, достаточно обрабатывать исключение InvalidPage

- exception PageNotAnInteger
Вызывается, если page() получает значение, которое не является целым числом.

- exception EmptyPage
Вызывается, если page() получает правильное значение, но для указанной страницы нет объектов.

Эти исключения являются потомками класса InvalidPage, таким образом, вы можете обрабатывать их с помощью простого except InvalidPage.

Объекты Page
--------------
Обычно создавать объекты Page вручную не требуется, так как вы получаете их с помощью метода Paginator.page().

        class Page(object_list, number, paginator)

Страница работает как срез Page.object_list при использовании len() или итерации по ней.

Методы
------
- Page.has_next()
Возвращает True, если следующая страница существует.

- Page.has_previous()
Возвращает True, если предыдущая страница существует.

- Page.has_other_pages()
Возвращает True, если существует следующая или предыдущая страница.

- Page.next_page_number()
Возвращает номер следующей страницы. Вызывает InvalidPage если следующая страница не существует.

- Page.previous_page_number()
Возвращает номер предыдущей страницы. Вызывает InvalidPage если предыдущая страница не существует.

- Page.start_index()
Возвращает индекс (начинается с единицы) первого объекта на странице относительно списка всех объектов. Например, для списка из пяти объектов при отображении двух объектов на странице, то для второй страницы метод start_index() вернёт 3.

- Page.end_index()
Возвращает индекс (начинается с единицы) последнего объекта на странице относительно списка всех объектов. Например, для списка из пяти объектов при отображении двух объектов на странице, то для второй страницы метод end_index() вернёт 4.

Атрибуты
---------
- Page.object_list
Список объектов текущей страницы.

- Page.number
Номер (начинается с единицы) текущей страницы.

- Page.paginator
Соответствующий объект Paginator.


Собственные шаблонные теги и фильтры
====================================
Шаблонизатор Django содержит большое количество встроенных тегов и фильтров. Тем не менее, вам может понадобиться добавить собственный функционал к шаблонам. Вы можете сделать это добавив собственную библиотеку тегов и фильтров используя Python, затем добавить ее в шаблон с помощью тега {% load %}.

Добавление собственной библиотеки
---------------------------------
Собственные теги и фильтры шаблонов должны определяться в приложении Django. Если они логически связаны с каким-то приложением, есть смысл добавить их в это приложение, иначе создайте новое приложение.

Приложение должно содержать каталог templatetags на том же уровне что и models.py, views.py и др. Если он не существует, создайте его. Не забудьте создать файл __init__.py чтобы каталог мог использоваться как пакет Python. После добавления этого модуля, необходимо перезапустить сервер, перед тем как использовать теги или фильтры в шаблонах.

templatetags
------------
теги и фильтры будут находиться в модуле пакета templatetags. Название модуля будет использоваться при загрузке библиотеки в шаблоне, так что убедитесь что оно не совпадает с названиями библиотек других приложений.

Например, если теги/фильтры находятся в файле latest_products.py, ваше приложение может выглядеть следующим образом:

        shop/
            __init__.py
            models.py
            templatetags/
                __init__.py
                latest_products.py
            views.py

в шаблоне:
----------

        {% load latest_products %}

Приложение содержащее собственные теги и фильтры должно быть добавлено в INSTALLED_APPS, чтобы тег {% load %} мог загрузить его. Это сделано в целях безопасности.

Не имеет значение сколько модулей добавлено в пакет templatetags. тег {% load %} использует название модуля, а не название приложения.

Библиотека тегов должна содержать переменную register равную экземпляру template.Library, в которой регистрируются все определенные теги и фильтры. 


        # -*- coding: UTF-8 -*-
        from django import template
        from .models import Product

        register=template.Library()


Включающие теги
================
django.template.Library.inclusion_tag()
---------------------------------------
это теги, которые выполняют другой шаблон и показывают результат. Например, интерфейс администратора Django использует включающий тег для отображения кнопок под формой на страницах добавления/редактирования объектов. Эти кнопки выглядят всегда одинаково, но ссылки зависят от текущего объекта – небольшой шаблон, который выполняется с данными из текущего объекта, удобно использовать в данном случае. (В приложении администратора это тег submit_row.)

Такие теги называются “включающие теги”.
-----------------------------------------
создадим тег, который выводит список 6-и последних публикаций для объекта модели Product

создадим функцию, которая возвращает словарь с данными. 

```
def latest_products():
    products = Product.objects.order_by('-updated').filter(status='available')[:6]
    return locals()
```

Using { } 
--------------
```
def latest_products():
    return {
            'products': Product.objects.order_by('-updated').filter(status='available')[:6],
           }
```
locals():
----------
```
def latest_products():
    products = Product.objects.order_by('-updated').filter(status='available')[:6]
    return locals()
```

создадим шаблон, который будет использоваться для генерации результата. Этот шаблон полностью относится к тегу: создатель тега определяет его, не создатель шаблонов(template designer).

shop/product/_latest_products.html
------------------------

        <!-- _latest_products.html -->
        <ul>
          {% for p in products %}
            <li><a href="{% url 'shop:detail' p.slug %}">{{ p.name }}</a>
          {% endfor %}
        </ul>


создадим и зарегистрируем тег, используя метод inclusion_tag() объекта Library. 

        # -*- coding: UTF-8 -*-
        from django import template
        from .models import Product

        register=template.Library()
         
        @register.inclusion_tag('shop/product/_latest_products.html') # регистрируем тег и подключаем шаблон _latest_products

        def latest_products():
            products = Product.objects.order_by('-updated').filter(status='available')[:6]
            return locals()

shop/product/index.html
-----------------------

        {% extends "base.html" %}
        {% load latest_products %}

            <h2>Latest Products</h2>
              <div>
                  {% latest_products %}
              </div>


shop/models.py
---------------

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
                
            views = models.IntegerField(default=0)
    

views.py
----------
        def product_detail(request, id, slug):
            product = get_object_or_404(Product, id=id, slug=slug, status='available')

            try:
                product.views = product.views + 1
                product.save()
            except:
                pass

models
------
        def save(self, *args, **kwargs):
                self.slug = slugify(self.name)
                super().save(*args, **kwargs)


shop/product/detail.html
----------------

        <p class="price">${{ product.price }}</p>

        <p class="raiting">

                {% if product.views > 1 %}
                    ({{ product.views }} views)
                {% elif product.views == 1 %}
                    ({{ product.views }} view)
                {% endif %}
        </p>


popular_products
================


        # -*- coding: UTF-8 -*-
        from django import template
        from blog.models import Product

        register=template.Library()
         
        @register.inclusion_tag('shop/product/_popular_products.html') # регистрируем тег и подключаем шаблон _popular_products

        def popular_products():
            products = Product.objects.filter(views__gte=5).filter(status='available')[:6]
            return locals()


shop/product/_popular_products.html
------------------------

        <ul>
          {% for p in products %}
            <li><a href="{% url 'shop:detail' p.slug %}">{{ p.name }}</a>
          {% endfor %}
        </ul>


Templates
==========
index.html
----------

        {% extends "base.html" %}
        {% load popular_products %}

                <h2>Popular Products</h2>
                  <div>
                  {% popular_products %}
                  </div>

Install django wysiwyg redactor:
================================

Pillow
------

    pip install Pillow


CKEDITOR
=========
settings.py
-----------
```

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',

    'ckeditor',
    'ckeditor_uploader',


CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_UPLOAD_SLUGIFY_FILENAME = False
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',

        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YouCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'youcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YouCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                # you extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
    }
}

```
admin.py
--------

        from ckeditor.widgets import CKEditorWidget

        class ProductAdminForm(forms.ModelForm):
            description = forms.CharField(widget=CKEditorWidget())
            class Meta:
                model = Product
                fields = '__all__'
                
        class ProductAdmin(admin.ModelAdmin):
            

            form = ProductAdminForm


urls.py
-------

urlpatterns = [

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]


autoescape
-----------

            {% autoescape off %}
                <p> {{ item.content }} </p>
            {% endautoescape %}

