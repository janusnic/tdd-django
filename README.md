# tdd-django unit_06

Менеджеры
=========
class Manager
Менеджер(Manager) - это интерфейс, через который создаются запросы к моделям Django. Каждая модель имеет хотя бы один менеджер.

Имя менеджера
--------------
По умолчанию Django добавляет Manager с именем objects для каждого класса модели. Однако, если вы хотите использовать objects, как имя поля, или хотите использовать название, отличное от objects для Manager, вы можете переименовать его для модели. Чтобы переименовать Manager добавьте в класс атрибут, значение которого экземпляр models.Manager():

from django.db import models

class MyClass(models.Model):
    #...
    item = models.Manager()

Обращение к MyClass.objects вызовет исключение AttributeError, в то время как MyClass.item.all() вернет список всех объектов MyClass.

Собственные менеджеры
---------------------
Вы можете использовать собственный менеджер, создав его через наследование от основного класса Manager и добавив его в модель.

Есть две причины, почему вам может понадобиться изменить Manager: добавить дополнительные методы, и/или изменить базовый QuerySet, который возвращает Manager.

Добавление методов в менеджер
-----------------------------
Добавление дополнительных методов в Manager - лучший способ добавить “table-level” функционал в вашу модель. (Для “row-level” функционала – то есть функции, которые работают с одним экземпляром модели – используйте методы модели, а не методы менеджера.)

Методы Manager могут возвращать что угодно. И это не обязательно должен быть QuerySet.

Вызов собственных методов QuerySet из Manager
---------------------------------------------
Т.к. большинство методом стандартного QuerySet доступны из Manager, следующий подход необходимо использовать только для собственных методов переопределенного QuerySet:

shop/models.py
--------------
        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible
        from django.core.urlresolvers import reverse

        class AvailabledManager(models.Manager):
            def get_queryset(self):
                return super(AvailabledManager, self).get_queryset().filter(status='available')


Изменение базового QuerySets менеджера
--------------------------------------
Базовый QuerySet менеджера возвращает все объекты модели.

Менеджеры по умолчанию
----------------------
При использовании собственного объекта Manager первый Manager, который заметит Django (в том порядке, в котором они определяются в модели) имеет особый статус. Для Django первый Manager будет Manager “по умолчанию”, и некоторые компоненты Django (включая dumpdata) будут использовать этот Manager. Поэтому нужно быть осторожным при выборе менеджера по умолчанию, чтобы, переопределив get_queryset(), не попасть в ситуацию, когда вы не можете получить нужный объект.

shop/models.py
--------------
        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible
        from django.core.urlresolvers import reverse

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

Параметры модели
================
Параметры Meta
--------------
app_label
---------
Если модель находится не в стандартной локации (models.py или пакет models приложения), модель должна определять к какому приложению она принадлежит

app_label = 'myapp'
------------------
app_label больше не обязательный параметр для моделей, которые находятся вне модуля models приложения.

db_table
--------
Название таблицы в базе данных для этой модели:

Название таблицы
----------------
Экономя ваше время, Django автоматически создаст название таблицы из названия модели и приложения. Название таблицы состоит из названия приложения(“app label”) – название используемое для команды manage.py startapp – и названия модели, объединенные нижним подчеркиванием.

Для переопределения названия таблицы используйте атрибут db_table class Meta.

Если имя колонки это зарезервированное SQL слово, или содержит символы запрещенные в названиях переменной в Python – в частности, дефис – все нормально. Django автоматически экранирует название колонок и таблиц.

Используйте нижний регистр для названий таблиц в MySQL
------------------------------------------------------
Настоятельно рекомендуем использовать нижний регистр при переопределении названия таблицы через db_table, особенно при использовании MySQL. 
Названия таблиц в кавычках для Oracle
-------------------------------------
Т.к в Oracle есть ограничение в 30 символов на название таблиц, и для соблюдения соглашений работы с Oracle, Django может ограничить название таблицы и преобразовать его в верхний регистр. Чтобы избежать этого, укажите название в кавычках в настройке db_table:

    db_table = '"name_left_in_lowercase"'

Кавычки можно использовать для других типов базы данных, не только Oracle, однако, они не будут иметь никакого эффекта.

db_tablespace
-------------
Имя “tablespace” базы данных для этой модели. По умолчанию используется настройка DEFAULT_TABLESPACE, если она определена. Если база данных не поддерживает “tablespace” для индексов, этот параметр будет проигнорирован.

default_related_name
--------------------
Название, которое будет использоваться для обратных связей к этой модели. По умолчанию 
    
    <model_name>_set.

Т.к. название поля обратной связи должно быть уникальным, будьте осторожны, если собираетесь наследоваться от модели. Чтобы избежать коллизий в названиях, можно добавить '%(app_label)s' и '%(model_name)s', которые будут заменены соответственно на название приложения модели и название модели в нижнем регистре. Смотрите именование обратных связей для абстрактных моделей.

get_latest_by
-------------
Название сортируемого поля модели, обычно DateField, DateTimeField или IntegerField. Определяет поле по умолчанию, которое будет использовано методами latest() и earliest() Manager-а модели.

managed
-------
По умолчанию True, означает что Django создаст необходимые таблицы в базе данных при выполнении команды migrate и удалит их при выполнении flush. То есть Django управляет таблицами.

При False, таблицы модели не будет создаваться или удаляться. Это полезно, если модель отображает существующую таблицу или “VIEW” в базе данных, которая была создана другим способом. Это единственная разница при managed=False. Все остальные этапы работы с моделью не изменяются. Они включают

Автоматическое добавление первичного ключа, если он не был определен. Для ясности лучше определить в модели все поля таблицы, которую отображает модель с managed=False`.

Если модель с managed=False содержит ManyToManyField на другую неуправляемую модель, промежуточная таблица для хранения связи многое-ко-многим не будет создана. Однако, промежуточная таблица между управляемой и не управляемой моделью будет создана.

Если вы хотите переопределить такое поведение по умолчанию, создайте модель для промежуточной таблицы (с необходимым managed) и укажите использование этой модели через параметр ManyToManyField.through.

Правильное создание таблиц при тестировании в тестовой базе данных для модели с managed=False ложится на ваши плечи.

Если вы хотите переопределить поведение модели на уровне Python, вы можете использовать managed=False и создать копию существующей модели. Однако, есть лучшее решение для такой ситуации: Proxy-модели.

order_with_respect_to
---------------------
Объекты модели будут отсортированы относительно указанного поля. Почти всегда используется для связанных объектов.

При добавлении order_with_respect_to, будет добавлено два дополнительных метода для получения и установки порядка связанных объектов: get_RELATED_order() и set_RELATED_order(), где RELATED название модели в нижнем регистре. 

ordering
--------
Сортировка по умолчанию используемая при получении объектов:

    ordering = ['-order_date']
Это кортеж или список строк. Каждая строка это название поля с необязательным префиксом “-”, который указывает на нисходящую сортировку. Поля без “-” будут отсортированы по возрастанию. Используйте ”?” для случайной сортировке.

Например, для сортировки по возрастанию по полю updated:

    ordering = ['updated']
Нисходящая сортировка по полю updated:

    ordering = ['-updated']
Для нисходящей сортировки по updated и восходящей по name, используйте:

    ordering = ['-updated', 'name']

permissions
-----------
Дополнительные разрешения(permissions) будут добавлены в таблицу разрешений при создании модели. Разрешения на добавление, удаление и изменение автоматически создаются для каждой модели. Это список 2-х элементных кортежей в формате (код разрешения, название разрешения).

default_permissions
-------------------
По умолчанию ('add', 'change', 'delete'). Вы можете поменять этот список, например, указав пустой список, если ваше приложение не требует никаких прав доступа. Необходимо указать в модели перед тем, как она будет создана командой migrate.

proxy
-----
При proxy = True, модель унаследованная от другой модели будет создана как proxy-модель.

unique_together
----------------
Множество полей, комбинация значений которых должна быть уникальна:

    unique_together = (("id", "slug"),)

Кортеж кортежей полей, которые должны быть вместе уникальны. Используется в интерфейсе администратора для проверки данных и на уровне базы данных (то есть соответствующее определение UNIQUE будет добавлено в CREATE TABLE запрос).

Для удобства unique_together может быть одноуровневым списком, если определяется один набор уникальных полей:

    unique_together = ("id", "slug")

index_together
--------------
Множество полей, для которых создается один индекс:

        index_together = [
            ["pub_date", "deadline"],
        ]
Будет создан один индекс для группы полей (то есть будет выполнен необходимый CREATE INDEX.)

Для удобства index_together может быть одноуровневым списком, если определяется один набор полей:

    index_together = ["pub_date", "deadline"]
verbose_name
------------
Читабельное название модели, в единственном числе:

    verbose_name = "product"
Если не указано, Django создаст из названия модели: CamelCase станет camel case.

verbose_name_plural
-------------------
Название модели в множественном числе:

    verbose_name_plural = "products"
Если не указано, Django создаст по правилу verbose_name + "s".

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

Выполнение запросов
===================
После создания модели, Django автоматически создает API для работы с базой данных, который позволяет вам создавать, получать, изменять и удалять объекты.

Создание объектов
-----------------
Для представления данных таблицы в виде объектов Python, Django использует интуитивно понятную систему: класс модели представляет таблицу, а экземпляр модели - запись в этой таблице.

Чтобы создать объект, создайте экземпляр класса модели, указав необходимые поля в аргументах и вызовите метод save() чтобы сохранить его в базе данных.

Чтобы создать и сохранить объект используйте метод create().
Сохранение изменений в объектах
--------------------------------
Для сохранения изменений в объект, который уже существует в базе данных, используйте save().

Сохранение полей ForeignKey и ManyToManyField
---------------------------------------------
Обновление ForeignKey работает так же, как и сохранение обычных полей; просто назначьте полю объект необходимого типа. 

Обновление ManyToManyField работает немного по-другому; используйте метод add() поля, чтобы добавить связанный объект.

Получение объектов
------------------
Для получения объектов из базы данных, создается QuerySet через Manager модели.

QuerySet представляет выборку объектов из базы данных. Он может не содержать, или содержать один или несколько фильтров – критерии для ограничения выборки по определенным параметрам. В терминах SQL, QuerySet - это оператор SELECT, а фильтры - условия такие, как WHERE или LIMIT.

Вы получаете QuerySet, используя Manager. Каждая модель содержит как минимум один Manager, и он называется objects по умолчанию. Обратиться к нему можно непосредственно через класс модели:

Получение всех объектов
-----------------------
Самый простой способ получить объекты из таблицы - это получить их всех. Для этого используйте метод all() менеджера(Manager):

Метод all() возвращает QuerySet всех объектов в базе данных.

    def index(request, category_slug=None):
        category = None
        categories = Category.objects.all()
        
        products = Product.available.all()
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'shop/product/index.html', {'category': category,
                                                          'categories': categories,
                                                          'products': products})
Получение объектов через фильтры
--------------------------------
QuerySet, возвращенный Manager, описывает все объекты в таблице базы данных. Обычно вам нужно выбрать только подмножество всех объектов.

Для создания такого подмножества, вы можете изменить QuerySet, добавив условия фильтрации. Два самых простых метода изменить QuerySet - это:

filter(**kwargs)
----------------
Возвращает новый QuerySet, который содержит объекты удовлетворяющие параметрам фильтрации.

    def index(request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(status='available')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'shop/product/index.html', {'category': category,
                                                          'categories': categories,
                                                          'products': products})
exclude(**kwargs)
-----------------
Возвращает новый QuerySet содержащий объекты, которые не удовлетворяют параметрам фильтрации.

Цепочка фильтров
-----------------
Результат изменения QuerySet - это новый QuerySet и можно использовать цепочки фильтров. 

Отфильтрованный QuerySet – уникален
-----------------------------------
После каждого изменения QuerySet, вы получаете новый QuerySet, который никак не связан с предыдущим QuerySet. Каждый раз создается отдельный QuerySet, который может быть сохранен и использован.

QuerySets – ленивы
------------------
QuerySets – ленивы, создание QuerySet не выполняет запросов к базе данных. Вы можете добавлять фильтры хоть весь день и Django не выполнит ни один запрос, пока QuerySet не вычислен. 

Получение одного объекта с помощью get
--------------------------------------
filter() всегда возвращает QuerySet, даже если только один объект возвращен запросом - в этом случае, это будет QuerySet содержащий один объект.

Если вы знаете, что только один объект возвращается запросом, вы можете использовать метод get() менеджера(Manager), который возвращает непосредственно объект:

Учтите, что есть разница между использованием get() и filter() с [0]. Если результат пустой, get() вызовет исключение DoesNotExist. Это исключение является атрибутом модели, для которой выполняется запрос. 

Также Django отреагирует, если запрос get() вернет не один объект. В этом случае будет вызвано исключение MultipleObjectsReturned, которое также является атрибутом класса модели.

Ограничение выборки
-------------------
Используйте синтаксис срезов для списков Python для ограничения результата выборки QuerySet. Это эквивалент таких операторов SQL как LIMIT и OFFSET.

На самом деле, срез QuerySet возвращает новый QuerySet – запрос не выполняется. 

Фильтры полей
--------------
Фильтры полей – это “операторы” для составления условий SQL WHERE. Они задаются как именованные аргументы для метода filter(), exclude() и get() в QuerySet.

Фильтры полей выглядят как field__lookuptype=value. (Используется двойное подчеркивание). 

Python позволяет определить функции, которые принимают именованные аргументы с динамически вычисляемыми названиями и значениями.
Поля указанные при фильтрации должны быть полями модели. Есть одно исключение, для поля ForeignKey можно указать поле с суффиксом _id. В этом случае необходимо передать значение первичного ключа связанной модели. 

API базы данных поддерживает около двух дюжин фильтров; 
Вот пример самых используемых фильтров:

- exact
“Точное” совпадение. Например:

    >>> Product.objects.get(name__exact="Samsung phone")
Создаст такой SQL запрос:

    SELECT ... WHERE name = 'Samsung phone';
Если вы не указали фильтр – именованный аргумент не содержит двойное подчеркивание – будет использован фильтр exact.

- iexact
Регистронезависимое совпадение. Такой запрос:

    >>> Product.objects.get(name__iexact="Samsung phone")
Найдет Product с названием "Samsung phone", "samsung phone", и даже "SamsunG pHone".

- contains
Регистрозависимая проверка на вхождение. Например:

    Product.objects.get(name__contains='Samsung')
Будет конвертировано в такой SQL запрос:

    SELECT ... WHERE name LIKE '%Samsung%';

Существуют также регистронезависимые версии, icontains.

- startswith, endswith
Поиск по началу и окончанию соответственно. Существуют также регистронезависимые версии istartswith и iendswith.

Фильтры по связанным объектам
-----------------------------
Django предлагает удобный и понятный интерфейс для фильтрации по связанным объектам, самостоятельно заботясь о JOIN в SQL. Для фильтра по полю из связанных моделей, используйте имена связывающих полей разделенных двойным нижним подчеркиванием, пока вы не достигните нужного поля.

Этот пример получает все объекты Product с Category, name которого равен 'phone':

    >>> Product.objects.filter(category__name='phone')
Этот поиск может быть столь глубоким, как вам будет угодно.

Все работает и в другую сторону. Чтобы обратиться к “обратной” связи, просто используйте имя модели в нижнем регистре.

Этот пример получает все объекты Category, которые имеют хотя бы один связанный объект Product с name содержащим 'Samsung':

    >>> Category.objects.filter(product__name__contains='Samsung')
Если вы используйте фильтр через несколько связей и одна из промежуточных моделей не содержит подходящей связи, Django расценит это как пустое значение (все значения равны NULL). Исключение не будет вызвано. Например, в этом фильтре:

    Product.objects.filter(product__brend__name='Lennon')
(при связанной модели Brend), если нет объекта brend связанного с product, это будет расценено как отсутствие name, вместо вызова исключения т.к. brend отсутствует. В большинстве случаев это то, что вам нужно. Единственный случай, когда это может работать не однозначно - при использовании isnull. Например:

    Product.objects.filter(entry__brend__name__isnull=True)
вернет объекты Product у которого пустое поле name у brend и также объекты, у которых пустой brend в  entry. Если вы не хотите включать вторые объекты, используйте:

    Product.objects.filter(brend__name__isnull=False,
            product__brend__name__isnull=True)

Удаление объектов
-----------------
Метод удаления соответственно называется delete(). Этот метод сразу удаляет объект и ничего не возвращает. Например:

    e.delete()
Можно также удалить несколько объектов сразу. Каждый QuerySet имеет метод delete(), который удаляет все объекты из QuerySet.

Учтите, что при любой возможности будет использован непосредственно SQL запрос, то есть метод delete() объекта может и не использоваться при удалении. Если вы переопределяете метод delete() модели и хотите быть уверенным, что он будет вызван, вы должны “самостоятельно” удалить объект модели (например, использовать цикл по QuerySet и вызывать метод delete() для каждого объекта) не используя метод delete() QuerySet.

При удалении Django повторяет поведение SQL выражения ON DELETE CASCADE – другими словами, каждый объект, имеющий связь(ForeignKey) с удаляемым объектом, будет также удален. Например:

    b = Product.objects.get(pk=1)
    # This will delete the Product and all of its Category objects.
    b.delete()
Это поведение можно изменить, определив аргумент on_delete поля ForeignKey.

Метод delete() содержится только в QuerySet и не существует в Manager. Это сделано, чтобы вы случайно не выполнили Category.objects.delete(), и не удалили все записи. Если вы на самом деле хотите удалить все объекты, сначала явно получите QuerySet, содержащий все записи:

    Category.objects.all().delete()

Работа с формами
================
HTML формы
----------
Форма в HTML – это набор элементов в 

        <form>...</form>, 

которые позволяют пользователю вводить текст, выбирать опции, изменять объекты и конторолы страницы, и так далее, а потом отправлять эту информацию на сервер.

Некоторые элементы формы - текстовые поля ввода и чекбоксы - достаточно простые и встроены в HTML. Некоторые – довольно сложные, состоят из диалогов выбора даты, слайдеров и других контролов, который обычно используют JavaScript и CSS.

Кроме input элементов форма должна содержать еще две вещи:

- куда: URL, на который будут отправлены данные
- как: HTTP метод, который должна использовать форма для отправки данных

Форма также говорит браузеру, что данные должны оправляться на URL, указанный в атрибуте action тега form и для отправки необходимо использовать HTTP метод, указанный атрибуте method - post.

GET или POST
------------
GET и POST – единственные HTTP методы, которые используются для форм.

При GET данные собираются в строку и передаются в URL. URL содержит адрес, куда отправлять данные, и данные для отправки. 

Любой запрос, который может изменить состояние системы - например, который изменяет данные в базе данных - должен использовать POST. GET должен использоваться для запросов, которые не влияют на состояние системы.

GET удобен для таких вещей, как форма поиска, т.к. URL, который представляет GET запрос, можно легко сохранить в избранное или отправить по почте.

Формы в Django
---------------
В контексте Web приложения ‘form’ может означать HTML form, или класс Django Form, который создает HTML формы, или данне, которые передаются при отправке формы, или ко всему механизму вместе.

Класс Django Form
------------------
Как и модель в Django, которая описывает структуру объекта, его поведение и представление, Form описывает форму, как она работает и показывается пользователю.

Как поля модели представляют поля в базе данных, поля формы представляют HTML input элементы. 

Поля формы сами являются классами. Они управляют данными формы и выполняют их проверку при отправке формы. Например, DateField и FileField работают с разными данными и выполняют разные действия с ними.

Поле формы представлено в браузере HTML “виджетом” - компонент интерфейса. Каждый тип поля представлен по умолчанию определенным классом Widget, который можно переопределить при необходимости.

Создание, обработка и рендеринг форм
-------------------------------------
При рендеринге объекта в Django мы обычно:

- получаем его в представлении (например, загружаем из базы данных)
- передаем в контекст шаблона
- представляем в виде HTML в шаблоне, используя переменные контекста

Рендеринг форм происходит аналогичным образом с некоторыми отличиями.

В случае с моделями, вряд ли нам может понадобится пустая модель в шаблоне. Для форм же нормально показывать пустую форму для пользователя.

Экземпляр модели, который используется в представлении, обычно загружается из базы данных. При работе с формой мы обычно создаем экземпляр формы в представлении.

При создании формы мы может оставить её пустой, или добавить начальные данные

Создание форм в Django
----------------------
Для начала нам понадобится следующий класс формы:

from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

Этот код создает класс Form с одним полем (your_name). Мы добавили читабельное название поля, которое будет добавлено в тег label при рендеринге поля (на самом деле мы могли не добавлять label т.к. аналогичное название Django сгенерировал бы самостоятельно).

Максимальное количество символом в значении мы указали с помощью параметра max_length. Он используется для двух вещей. Будет добавлен атрибут maxlength="100" в HTML тег input (теперь браузер не позволит пользователю ввести больше символов, чем мы указали). Также Django выполнит проверку введенного значения, когда получит запрос с браузера с введенными данными.

Экземпляр Form содержит метод is_valid(), который выполняет проверку всех полей формы. Если все данные правильные, это метод:
- вернет True
- добавит данные формы в атрибут cleaned_data.

После рендеринга наша форма будет выглядеть следующим образом:

        <label for="your_name">Your name: </label>
        <input id="your_name" type="text" name="your_name" maxlength="100">

Обратите внимание, она не содержит тег form, или кнопку отправки. Вам необходимо самостоятельно их добавить в шаблоне.

Поля формы
----------
При создании класса Form наиболее важной деталью является определение полей формы. Каждое поле обладает собственной логикой проверки вводимых данных наряду с дополнительными возможностями.

required
--------
По умолчанию каждый класс Field предполагает значение обязательным. Таким образом, если вы передадите ему пустое значение, т.е. None или пустую строку (""), то метод clean() вызовет исключение ValidationError

Field.clean(value)
Каждый экземпляр класса Field имеет метод clean(), который принимает единственный аргумент и который вызывает исключение django.forms.ValidationError в случае ошибки или возвращает чистое значение

initial
-------
Аргумент initial позволяет определять начальное значение для поля, при его отображении на незаполненной форме.
Для определения динамических начальных данных, используйте параметр Form.initial.
Использование этого аргумента подходит для отображения пустой формы, в которой поля будут иметь указанные значения. 

Виджеты
--------
Каждое поле формы содержит соответствующий класс Widget, который отвечает за создание HTML кода, представляющего поле.

В большинстве случаев поле уже содержит подходящий виджет. Например, по умолчанию поле CharField представлено виджетом TextInput, который создает тег input type="text" в HTML. 

widget
------
Аргумент widget позволяет указать класс Widget, который следует использовать при отображении поля. 

HiddenInput
-----------
Скрытый ввод: input type='hidden' 

BooleanField
------------
Стандартный виджет: CheckboxInput
Пустое значение: False.
Возвращает: True или False языка Python.
Гарантирует, что значение равно True (т.е. чекбокс отмечен), если поле имеет атрибут required=True.
Ключи сообщений об ошибках: required.

TypedChoiceField
----------------
Стандартный виджет: Select
Пустое значение: Всё, что вы назовёте empty_value.
Возвращает: Значение типа, указанного аргументом coerce.
Проверяет, что полученное значение присутствует в списке вариантов и может быть преобразовано в нужный тип.
Ключи сообщений об ошибках: required, invalid_choice.

Принимает дополнительные аргументы:

- coerce
Функция, которая принимает один аргумент и возвращает преобразованное значение. Например, можно использовать стандартные int, float, bool и другие типы. Функция по умолчанию не выполняет преобразования. Преобразование значения происходит после валидации, поэтому можно вернуть значение, которое отсутствует в choices.

- empty_value
Значение, используемое для представления “пустоты”. Обычно это пустая строка. None является ещё одним вариантом. Следует отметить, что это значение не будет преобразовываться функцией, определённой аргументом coerce, так что выбирайте значение соответственно.

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

Представление
--------------
Данные формы отправляются обратно в Django и обрабатываются представлением, обычно тем же, которое и создает форму. Это позволяет повторно использовать часть кода.

Для обработки данных формой нам необходимо создать ее в представлении для URL, на который браузер отправляет данные формы:


        from django.shortcuts import render, get_object_or_404
        from .models import Product, Category
        from .forms import CartAddProductForm

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


Если в представление пришел GET запрос, будет создана пустая форма и добавлена в контекст шаблона для последующего рендеринга. Это мы и ожидаем получить первый раз открыв страницу с формой.

Шаблон
------
Наш cart.html шаблон может быть довольно простым:

        <form action="{% url "shop:cart_add" product.id %}" method="post">
            {{ cart_product_form }}
            {% csrf_token %}
            <input type="submit" value="Add to cart">
        </form>

Все поля формы и их атрибуты будут добавлены в HTML из {{ form }} при рендеринге шаблона.

Подделка межсайтового запроса (CSRF)
====================================

Промежуточный слой CSRF и шаблонный тег предоставляют легкую-в-использовании защиту против Межсайтовой подделки запроса. Этот тип атак случается, когда злонамеренный Web сайт содержит ссылку, кнопку формы или некоторый javascript, который предназначен для выполнения некоторых действий на вашем Web сайте, используя учетные данные авторизованного пользователя, который посещал злонамеренный сайт в своем браузере. Сюда также входит связанный тип атак, ‘login CSRF’, где атакуемый сайт обманывает браузер пользователя, авторизируясь на сайте с чужими учетными данными.

Первая защита против CSRF атак - это гарантирование того, что GET запросы (и другие ‘безопасные’ методы, определенные в 9.1.1 Safe Methods, HTTP 1.1, RFC 2616) свободны от побочных эффектов. Запросы через ‘небезопасные’ методы, такие как POST, PUT и DELETE могут быть защищены при помощи шагов, описанных ниже.

Для того чтобы включить CSRF защиту для ваших представлений, выполните следующие шаги:

Промежуточный слой CSRF активирован по умолчанию и находится в настройке MIDDLEWARE_CLASSES. Если вы переопределяете эту настройку, помните, что ``‘django.middleware.csrf.CsrfViewMiddleware’``должен следовать перед промежуточными слоями, которые предполагают, что запрос уже проверен на CSRF атаку.

        MIDDLEWARE_CLASSES = (
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'django.middleware.security.SecurityMiddleware',
        )


Если вы отключили защиту, что не рекомендуется, вы можете использовать декоратор csrf_protect() в части представлений, которые вы хотите защитить.

{% csrf_token %}
-----------------
В любом шаблоне, который использует POST форму, используйте тег csrf_token внутри элемента form если форма для внутреннего URL, т. е.:

        <form action="." method="post">{% csrf_token %}

Это не должно делаться для POST форм, которые ссылаются на внешние URL’ы, поскольку это может вызвать утечку CSRF токена, что приводит к уязвимости.

В соответствующих функциях представления, убедитесь, что 'django.template.context_processors.csrf' контекстный процессор используется. Обычно, это может быть сделано в один из двух способов:

Использовать RequestContext, который всегда использует 'django.template.context_processors.csrf' (не зависимо от параметра TEMPLATES ). Если вы используете общие представления или contrib приложения, вы уже застрахованы, так как эти приложения используют RequestContext повсюду.

Вручную импортировать и использовать процессор для генерации CSRF токена и добавить в шаблон контекста. т.е.:

        from django.shortcuts import render_to_response
        from django.template.context_processors import csrf

        def my_view(request):
            c = {}
            c.update(csrf(request))
            # ... view code here
            return render_to_response("a_template.html", c)

Формы и CSRF защита
-------------------
Django поставляется с защитой против Cross Site Request Forgeries. При отправке формы через POST с включенной защитой от CSRF вы должны использовать шаблонный тег csrf_token. 

Данные поля
-----------
Когда в форму добавлены данные, и она проверена методом is_valid() (и is_valid() вернул True), проверенные данные будут добавлены в словарь form.cleaned_data. Эти данные будет преобразованы в подходящий тип Python.

templates/shop/product/detail.html
----------------------------------

        <div class="product-detail">
            <img src="{% if product.image %}{{ product.image.url }}{% else %}{% static "img/no_image.png" %}{% endif %}">
            <h1>{{ product.name }}</h1>
            <h2><a href="{{ product.category.get_absolute_url }}">{{ product.category }}</a></h2>
            <p class="price">${{ product.price }}</p>

            <form action="{% url "shop:cart_add" product.id %}" method="post">
                {{ cart_product_form }}
                {% csrf_token %}
                <input type="submit" value="Add to cart">
            </form>
            
            {{ product.description|linebreaks }}
        </div>

shop/urls.py
------------
        
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
            url(r'^(?P<category_slug>[-\w]+)/$', views.index, name='product_index_by_category'),
            url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
        ]

templates/shop/product/cart.html
--------------------------------
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
                                    
                                    <input type="submit" value="Update">
                                    {% csrf_token %}
                                </form>
                            </td>
                            <td><a href="#">Remove</a></td>
                            <td class="num"></td>
                            <td class="num"></td>
                        </tr>
                        {% endwith %}
                    {% endfor %}
                    <tr class="total">
                        <td>Total</td>
                        <td colspan="4"></td>
                        <td class="num"></td>
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

