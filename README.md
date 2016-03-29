# tdd-django unit_04

- Объектно-ориентированное программирование на Python
[Особенности ООП в Python](https://slides.com/janusnicon/class-inside/)

# основные идеи ООП:
1. наследование. Возможность выделять общие свойства и методы классов в один класс верхнего уровня (родительский). Классы, имеющие общего родителя, различаются между собой за счет включения в них различных дополнительных свойств и методов.

2.  Инкапсуляция. Свойства и методы класса делятся на доступные из вне (опубликованные) и недоступные (защищенные). Защищенные атрибуты нельзя изменить, находясь вне класса. Опубликованные же атрибуты также называют интерфейсом объекта, т. к. с их помощью с объектом можно взаимодействовать.

3.  Полиморфизм. Полиморфизм подразумевает замещение атрибутов, описанных ранее в других классах: имя атрибута остается прежним, а реализация уже другой. Полиморфизм позволяет специализировать (адаптировать) классы, оставляя при этом единый интерфейс взаимодействия.

# Особенности ООП в Python
1.  Любое данное — это объект. Число, строка, список, массив и др. — все является объектом. Бывают объекты встроенных классов, а бывают объекты пользовательских классов. Для единого механизма взаимодействия предусмотрены методы перегрузки операторов.

2.  Класс — это тоже объект с собственным пространством имен.  

3.  Инкапсуляции в Python не уделяется особого внимания. В других языках программирования обычно нельзя получить напрямую доступ к свойству, описанному в классе. Для его изменения может быть предусмотрен специальный метод. В Python же это легко сделать, просто обратившись к свойству класса из вне. 

SHOP
====

        ./manage.py startapp shop

Настройка базы данных
======================
mysite/settings.py. 
-------------------

        # Database
        # https://docs.djangoproject.com/en/1.9/ref/settings/#databases

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }


По умолчанию используется SQLite. SQLite включен в Python. 

Модели
=======

Модели отображают информацию о данных, с которыми вы работаете. Они содержат поля и поведение ваших данных. Обычно одна модель представляет одну таблицу в базе данных.

# Наследование

Каждая модель это класс унаследованный от django.db.models.Model.

        from django.db import models

Атрибут модели представляет поле в базе данных.

        class Category(models.Model):
            name = models.CharField('categories name', max_length=100)

            description = models.TextField(max_length=4096)

name,description - поля модели. Каждое поле определено как атрибут класса (представлено экземпляром класса Field), и каждый атрибут соответствует полю таблицы в базе данных.

CharField, TextField для текстовых полей  - указывает Django какие типы данных хранят эти поля.

Названия каждого экземпляра Field - это название поля, в “машинном”(machine-friendly) формате. Вы будете использовать эти названия в коде, а база данных будет использовать их как названия колонок.

Вы можете использовать первый необязательный аргумент конструктора класса Field, чтобы определить отображаемое, удобное для восприятия, название поля. Оно используется в некоторых компонентах Django, и полезно для документирования. Если это название не указано, Django будет использовать “машинное” название. 

В этом примере, мы указали отображаемое название только для поля name - 'categories name'. Для всех других полей будет использоваться “машинное” название.

        class Category(models.Model):
            name = models.CharField('categories name', max_length=100)

            description = models.TextField(max_length=4096, default='')


Некоторые классы, унаследованные от Field, имеют обязательные аргументы. Например, CharField требует, чтобы вы передали ему max_length. Это используется не только в схеме базы данных, но и при валидации.

Field может принимать различные необязательные аргументы; в нашем примере мы указали default значение для description равное ''.

Наследование моделей
====================
Наследование моделей в Django работает так же, как и наследование классов в Python, но базовый класс должен наследоваться от django.db.models.Model.

Единственное, что вам нужно определить, это должна ли родительская модель быть независимой моделью (с собственной таблицей в базе данных), или же родительская модель просто контейнер для хранения информации, доступной только через дочерние модели.

Существует три вида наследования моделей в Django.

Чаще всего вы будете использовать родительскую модель для хранения общих полей, чтобы не добавлять их в каждую дочернюю модель. Если вы не собираетесь использовать его как независимую модель – Абстрактные модели то, что вам нужно.

Если родительская модель независимая(возможно, из другого приложения) и должна храниться в отдельной таблице, Multi-table наследование то, что вам нужно.

Если же вы хотите переопределить поведение модели на уровне Python, не меняя структуры базы данных, вы можете использовать Proxy-модели.

# Перегрузка операторов, строковое представление

- __str__(self)
Определяет поведение функции str(), вызванной для экземпляра вашего класса.


        class Category(models.Model):
            name = models.CharField(max_length=200, db_index=True)

            def __str__(self):
                return self.name


- __repr__(self)
----------------
Определяет поведение функции repr(), вызыванной для экземпляра вашего класса. Главное отличие от str() в целевой аудитории. repr() больше предназначен для машинно-ориентированного вывода (более того, это часто должен быть валидный код на Питоне), а str() предназначен для чтения людьми.


        def __add__(self, other):
            if isinstance(other, self.__class__):
                return Command(self, other)

        def __repr__(self):
            return '{u.name} (cost={u.cost}, level={u.level})'.format(u=self)


- __unicode__(self)
-------------------
Определяет поведение функции unicode(), вызыванной для экземпляра вашего класса. unicode() похож на str(), но возвращает строку в юникоде. Будте осторожны: если клиент вызывает str() на экземпляре вашего класса, а вы определили только __unicode__(), то это не будет работать. Постарайтесь всегда определять __str__() для случая, когда кто-то не имеет такой роскоши как юникод.

        def __unicode__(self):
            return self.name

Активация моделей
=================
- Создать структуру базы данных (CREATE TABLE) для приложения.

- Создать Python API для доступа к данным объектов Category.

Но первым делом мы должны указать нашему проекту, что приложение shop установлено.

Приложения Django “подключаемые”: вы можете использовать приложение в нескольких проектах и вы можете распространять приложение, так как они не связаны с конкретным проектом Django.

Отредактируйте файл mysite/settings.py и измените настройку INSTALLED_APPS добавив строку 'shop':

mysite/settings.py
-------------------
```
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop',
)
```
Теперь Django знает, что необходимо использовать приложение shop. 

INSTALLED_APPS
--------------
По умолчанию: () (Пустой кортеж)

Кортеж строк, который указывают все приложения Django, используемые в проекте. Каждая строка должна быть полным Python путем к:

- классу настройки приложения, или
- пакету с приложением.

INSTALLED_APPS теперь поддерживает конфигурации приложений.

- Названия приложения и метки(labels) должны быть уникальны в INSTALLED_APPS
- Названия приложений — Python путь к пакету приложения — должны быть уникальны. Нельзя подключить одно приложение дважды, разве что продублировав код с другим названием.

Короткие названия приложения — по умолчанию последняя часть названия приложения — должны быть так же уникальны. Например, можно использовать вместе django.contrib.auth и myproject.auth. Однако, необходимо указать label.

Эти правила распространяются на все приложения в INSTALLED_APPS, как на классы настройки приложений, так и на пакеты приложений.
Если несколько приложений содержат разные версии одних и тех же ресурсов (шаблоны, статические файлы, команды, файлы перевода), будут использоваться ресурсы из приложения, которое указано выше в INSTALLED_APPS.


Поля
====
Самая важная часть модели – и единственная обязательная – это список полей таблицы базы данных которые она представляет. Поля определены атрибутами класса. Нельзя использовать имена конфликтующие с API моделей, такие как clean, save или delete.


        from django.db import models

        class Category(models.Model):
            name = models.CharField(max_length=100)
            description = models.TextField(max_length=4096)


Типы полей
===========
Каждое поле в модели должно быть экземпляром соответствующего Field класса. Django использует классы полей для определения такой информации:

- Типа колонки в базе данных (например: INTEGER, VARCHAR).

- Виджет используемый при создании поля формы (например: input type="text", select).

- Минимальные правила проверки данных, используемые в интерфейсе администратора и для автоматического создания формы.

Настройка полей
===============
Для каждого поля есть набор предопределенных аргументов. Например, CharField (и унаследованные от него) имеют обязательный аргумент max_length, который определяет размер поля VARCHAR для хранения данных этого поля.

Также есть список стандартных аргументов для всех полей. Все они не обязательны.

null
-----
Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.

blank
------
Если True, поле не обязательно и может быть пустым. По умолчанию - False.

Это не то же что и null. null относится к базе данных, blank - к проверке данных. Если поле содержит blank=True, форма позволит передать пустое значение. При blank=False - поле обязательно.

# help_text
Поля моделей в Django принимают атрибут help_text, который используется в Django формах/админке для вывода назначения полей  — это служит отличной возможностью для документации ваших моделей. Если в дальнейшем вы пригласите нового разработчика в проект, то help_text позволит сохранить бесчисленное количество часов на объяснения структуры моделей.

Подсказка, отображаемая в поле формы. 
при отображении в форме, HTML-символы не экранируются. Это позволяет использовать HTML в help_text если вам необходимо. Например:

        help_text="Please use the following format: <em>YYYY-MM-DD</em>."

Также вы можете использовать обычный текст и django.utils.html.escape(), чтобы экранировать HTML. Убедитесь, что вы экранируете все подсказки, которые могут определять непроверенные пользователи, чтобы избежать XSS атак.

# primary_key

При True поле будет первичным ключом.

Если primary_key=True не указан ни для одного поля, Django самостоятельно добавит поле типа IntegerField для хранения первичного ключа, поэтому вам не обязательно указывать primary_key=True для каждой модели. 

Поле первичного ключа доступно только для чтения. Если вы поменяете значение первичного ключа для существующего объекта, а затем сохраните его, будет создан новый объект рядом с существующим. 


        from django.db import models

        class Category(models.Model):
            name = models.CharField(max_length=100, primary_key=True)
            description = models.TextField(max_length=4096)

        >>> cat = Category.objects.create(name='Apple')
        >>> cat.name = 'Pear'
        >>> cat.save()
        >>> Category.objects.values_list('name', flat=True)
        ['Apple', 'Pear']


unique
-------
При True поле будет уникальным.

## Первичный ключ по умолчанию
По умолчанию Django для каждой модели добавляет такое поле:

        id = models.AutoField(primary_key=True)

Это автоинкрементный первичный ключ.

Для его переопределения просто укажите primary_key=True для одного из полей. При этом Django не добавит поле id.

Каждая модель должна иметь хотя бы одно поле с primary_key=True (явно указанное или созданное автоматически).

primary_key=True подразумевает null=False и unique=True. Модель может содержать только один первичный ключ.

# verbose_name
Field.verbose_name

## Читабельное имя поля
Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField, первым аргументом принимает необязательное читабельное название. Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.

        class Category(models.Model):
            name = models.CharField(max_length=100, verbose_name=_('name'))
            description = models.TextField(max_length=4096)

# default
Field.default
Значение по умолчанию для поля. Это может быть значение или вызываемый(callable) объект. Если это вызываемый объект, он будет вызван при создании нового объекта.

Значение по умолчанию не может быть изменяемым значением (экземпляр модели, список, множество и т.д.), т.к. все объекты модели будут ссылаться на этот объект и использовать его как значение по умолчанию. 

lambda нельзя использовать в качестве значения для default т.к. она не может быть сериализована для миграций.

Значение по умолчанию используется, если был создан экземпляр модели, а значение для поля не было указано. Если поле является первичным ключом, значение по умолчанию также использует и при указании None.


# unique
Field.unique
При True значение поля должно быть уникальным.

Этот параметр учитывается при сохранении в базу данных и при проверке данных в модели. Если вы попытаетесь сохранить повторное значение в поле с unique, будет вызвана ошибка django.db.IntegrityError методом save().

Этот параметр можно использовать для любого типа поля кроме ManyToManyField, OneToOneField и FileField.

при unique равном True, не нужно указывать db_index, т.к. unique создает индекс.

# Типы полей

## CharField
class CharField(max_length=None[, **options])
Строковое поле для хранения коротких или длинных строк.

Для большого количества текстовой информации используйте TextField.

Виджет по умолчанию для этого поля TextInput.

CharField принимает один дополнительный аргумент:

### CharField.max_length
Максимальная длинна(в символах) этого поля. max_length используется для проверки данных на уровне базы данных и форм Django.

Если вы создаете независимое приложение, которое должно работать на различных базах данных, помните что существуют некоторые ограничения использования max_length для некоторых типов баз данных. 
#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы.

## TextField
class TextField([**options])
Большое текстовое поле. Форма использует виджет Textarea.

Если указать атрибут max_length, это повлияет на поле, создаваемое виджетом Textarea. Но не учитывается на уровне модели или базы данных. Для этого используйте CharField.

#### Пользователям MySQL
Если вы используете это поле с MySQLdb 1.2.1p2 и utf8_bin “collation” (которое не является значением по умолчанию), могут быть некоторые проблемы. 

## AutoField
class AutoField(**options)
Автоинкрементное поле IntegerField. Используется для хранения ID. Скорее всего вам не придется использовать это поле, первичный ключ будет автоматически добавлен к модели.

Миграции
=========

        cd mysite
        python manage.py migrate

INSTALLED_APPS
--------------
        'shop'

Выполняя makemigrations, вы говорите Django, что внесли некоторые изменения в ваши модели и хотели бы сохранить их в миграции.

        ./manage.py makemigrations shop
        
            Migrations for 'shop':
              0001_initial.py:
                - Create model Category

Миграции используются Django для сохранения изменений ваших моделей (и структуры базы данных) - это просто файлы на диске. Вы можете изучить миграцию для создания ваших моделей, она находится в файле shop/migrations/0001_initial.py. 

        # -*- coding: utf-8 -*-
        # Generated by Django 1.9.4 on 2016-03-28 12:21
        from __future__ import unicode_literals

        from django.db import migrations, models


        class Migration(migrations.Migration):

            initial = True

            dependencies = [
            ]

            operations = [
                migrations.CreateModel(
                    name='Category',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=100, verbose_name='Categories Name')),
                        ('description', models.TextField(default='', max_length=4096)),
                    ],
                ),
            ]


Команда sqlmigrate получает название миграции и возвращает SQL:

        ./manage.py sqlmigrate shop 0001

Вы увидите приблизительно такое:


        BEGIN;

        --
        -- Create model Category
        --
        CREATE TABLE "shop_category" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, 
            "name" varchar(100) NOT NULL, 
            "description" text NOT NULL);

        COMMIT;


Полученные запросы зависят от базы данных, которую вы используете. 

Названия таблиц созданы автоматически из названия приложения(shop) и названия модели в нижнем регистре – category. (Вы можете переопределить это.)

Первичные ключи (ID) добавлены автоматически. (Вы можете переопределить и это.)

Django добавляет "_id" к названию внешнего ключа. (вы можете переопределить это.)

Учитываются особенности базы данных, которую вы используете. Специфические типы данных такие как auto_increment (MySQL), serial (PostgreSQL), или integer primary key (SQLite) будут использоваться автоматически. Тоже касается и экранирование названий, что позволяет использовать в названии кавычки – например, использование одинарных или двойных кавычек.

Команда sqlmigrate не применяет миграцию к базе данных - она просто выводит запросы на экран, чтобы вы могли увидеть какой SQL создает Django. Это полезно, если вы хотите проверить что выполнит Django, или чтобы предоставить вашему администратору базы данных SQL скрипт.

Если необходимо, можете выполнить python manage.py check. Эта команда ищет проблемы в вашем проекте не применяя миграции и не изменяя базу данных.

В Django есть команда, которая выполняет миграции и автоматически обновляет базу данных - она называется migrate. 

выполните команду migrate, чтобы создать таблицы для этих моделей в базе данных:

        $ python manage.py migrate

        Operations to perform:
          Apply all migrations: contenttypes, admin, sessions, auth, shop
        Running migrations:
          Rendering model states... DONE
          Applying shop.0001_initial... OK

Команда migrate выполняет все миграции, которые ещё не выполнялись, (Django следит за всеми миграциями, используя таблицу в базе данных django_migrations) и применяет изменения к базе данных, синхронизируя структуру базы данных со структурой ваших моделей.

Django Object-relational Mapper (ORM)
=====================================

После создания модели, Django автоматически создает API для работы с базой данных, который позволяет вам создавать, получать, изменять и удалять объекты. 

Выполнение запросов QuerySet
============================

        ./manage.py shell
        
        Python 3.4.3 (default, Oct 14 2015, 20:28:29) 
        [GCC 4.8.4] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        (InteractiveConsole)

Создание объектов
-----------------
Для представления данных таблицы в виде объектов Python, Django использует интуитивно понятную систему: класс модели представляет таблицу, а экземпляр модели - запись в этой таблице.

Чтобы создать объект, создайте экземпляр класса модели, указав необходимые поля в аргументах и вызовите метод save() чтобы сохранить его в базе данных.

        >>> from shop.models import Category
        >>> cat = Category.objects.create(name='Django', description='Descriptions Django category')
        >>> cat.save()

        >>> cat
        <Category: Category object>
        >>>

        >>> Category.objects.all()
        [<Category: Category object>]

## Как получить список всех атрибутов объекта

        dir(cat)
        ['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_base_manager', '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_ordering', '_check_swappable', '_check_unique_together', '_default_manager', '_deferred', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', 'check', 'clean', 'clean_fields', 'date_error_message', 'delete', 'description', 'from_db', 'full_clean', 'get_deferred_fields', 'id', 'name', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'unique_error_message', 'validate_unique']
        >>> 

        >>> Category.__dict__
        mappingproxy({'objects': <django.db.models.manager.ManagerDescriptor object at 0x7f746a392400>, '_meta': <Options for Category>, 'MultipleObjectsReturned': <class 'shop.models.MultipleObjectsReturned'>, '__doc__': 'Category(id, name, description)', '_base_manager': <django.db.models.manager.Manager object at 0x7f746a392438>, 'DoesNotExist': <class 'shop.models.DoesNotExist'>, '_default_manager': <django.db.models.manager.Manager object at 0x7f746a392438>, '__module__': 'shop.models'})
        

        >>> cat.__dict__
        {'description': 'Descriptions Django category', '_state': <django.db.models.base.ModelState object at 0x7f746a30a550>, 'id': 1, 'name': 'Django framework'}
        >>> 

        >>> cat.name
        'Django'

Сохранение изменений в объектах
-------------------------------
Для сохранения изменений в объект, который уже существует в базе данных, используйте save().

        >>> cat.name = 'Django framework'
        >>> cat.save()
        >>> cat.name
        'Django framework'

## __str__()
        
        >>> cat.__str__()
        'Category object'

shop/models.py
--------------

        from django.db import models

        class Category(models.Model):
            name = models.CharField('Categories Name', max_length=100)
            description = models.TextField(max_length=4096, default='')

            def __str__(self):
                return self.name

## __str__()

        >>> from shop.models import Category
        >>> cat = Category(name='Python', description='Python cat description')
        >>> cat.save()
        >>> cat.name
        'Python'
        >>> cat.__str__()
        'Python'
        >>> 

## cat.__repr__()

        >>> cat.__repr__()
        '<Category: Python>'

Получение объектов
------------------
Для получения объектов из базы данных, создается QuerySet через Manager модели.

QuerySet представляет выборку объектов из базы данных. Он может не содержать, или содержать один или несколько фильтров – критерии для ограничения выборки по определенным параметрам. В терминах SQL, QuerySet - это оператор SELECT, а фильтры - условия такие, как WHERE или LIMIT.

Вы получаете QuerySet, используя Manager. Каждая модель содержит как минимум один Manager, и он называется objects по умолчанию. Обратиться к нему можно непосредственно через класс модели

Получение всех объектов
-----------------------
Самый простой способ получить объекты из таблицы - это получить их всех. Для этого используйте метод all() менеджера(Manager):
## objects.all()

        a = Category.objects.all()
        >>> a
        [<Category: Django>, <Category: Python>]

Получение одного объекта с помощью get
--------------------------------------

Если вы знаете, что только один объект возвращается запросом, вы можете использовать метод get() менеджера(Manager), который возвращает непосредственно объект:

## objects.get(id=1)

        >>> a = Category.objects.get(id=1)
        >>> a
        <Category: Django>
        >>> a = Category.objects.get(id=2)
        >>> a
        <Category: Python>

## objects.order_by('-name')

        >>> a = Category.objects.order_by('-name')
        >>> a
        [<Category: Python>, <Category: Django>]

Удаление объектов
-----------------
Метод удаления соответственно называется delete(). Этот метод сразу удаляет объект и ничего не возвращает.

Можно также удалить несколько объектов сразу. Каждый QuerySet имеет метод delete(), который удаляет все объекты из QuerySet.

## delete()

        >>> a = Category.objects.get(id=2)
        >>> a.delete()
        (1, {'shop.Category': 1})
        >>> a
        <Category: Python>

Миграции позволяют изменять ваши модели в процессе развития проекта без необходимости пересоздавать таблицы в базе данных. Их задача изменять базу данных без потери данных. 

1. Внесите изменения в модели (в models.py).
2. Выполните python manage.py makemigrations чтобы создать миграцию для ваших изменений
3. Выполните python manage.py migrate чтобы применить изменения к базе данных.

Model Product
-------------

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
                return self.name


        ./manage.py makemigrations shop
        ./manage.py migrate

Две команды необходимы для того, чтобы хранить миграции в системе контроля версий. Они не только помогают вам, но и могут использоваться другими программистами вашего проекта.

ImageField
==========
        class ImageField([upload_to=None, height_field=None, width_field=None, max_length=100, **options])
Наследует все атрибуты и методы поля FileField, но также проверяет является ли загруженный файл изображением.

В дополнение к атрибутам поля FileField ImageField содержит также height и width.

Для определения этих аргументов ImageField принимает дополнительные аргументы:

ImageField.height_field
-----------------------
Имя поля, которому автоматически будет присвоено значение высоты изображения при каждом сохранении объекта.

ImageField.width_field
----------------------
Имя поля, которому автоматически будет присвоено значение ширины изображения при каждом сохранении объекта.

Требуется библиотека Pillow.
-----------------------------
По-умолчанию, экземпляр ImageField создается как колонка varchar в базе данных. Как и с другими полями вы можете изменить максимальную длину используя аргумент max_length.


PositiveIntegerField
---------------------

        class PositiveIntegerField([**options])
Как и поле IntegerField, но значение должно быть больше или равно нулю (0). Можно использовать значение от 0 до 2147483647. Значение 0 принимается для обратной совместимости.

## BigIntegerField
class BigIntegerField([**options])
64-битное целочисленное, аналогично IntegerField но позволяет хранить числа от -9223372036854775808 до 9223372036854775807. Форма будет использовать TextInput для отображения.

## BooleanField
        class BooleanField(**options)
Поле хранящее значение true/false.

Виджет по умолчанию для этого поля CheckboxInput.

Если вам нужен параметр null, используйте поле NullBooleanField.

по умолчанию для BooleanField None, если Field.default не указан.


## DateField
        class DateField([auto_now=False, auto_now_add=False, **options])
Дата, представленная в виде объекта datetime.date Python. Принимает несколько дополнительных параметров:

### DateField.auto_now
Значение поля будет автоматически установлено в текущую дату при каждом сохранении объекта. Полезно для хранения времени последнего изменения. текущее время будет использовано всегда; 

### DateField.auto_now_add
Значение поля будет автоматически установлено в текущую дату при создании(первом сохранении) объекта. Полезно для хранения времени создания. 

В форме поле будет представлено как :class:`~django.forms.TextInput с JavaScript календарем, и кнопкой “Сегодня”. Содержит дополнительную ошибку invalid_date.

Опции auto_now_add, auto_now и default взаимоисключающие. Использование их вместе вызовет ошибку.

При использовании auto_now или auto_now_add со значением True будут установлены параметры editable=False и blank=True.

Опции``auto_now`` и auto_now_add всегда используют дату в часовом поясе по умолчанию в момент создания или изменения объекта. Если такое поведение вам не подходит, вы можете указать свою функцию как значение по умолчанию, или переопределить метод save(), вместо использования auto_now или auto_now_add. Или использовать DateTimeField вместо DateField и выполнять преобразование в дату при выводе значения.

## DateTimeField
        class DateTimeField([auto_now=False, auto_now_add=False, **options])
Дата и время, представленные объектом datetime.datetime Python. Принимает аналогичные параметры что и DateField.

Виджет по умолчанию в форме для этого поля - TextInput. Интерфейс администратора использует два виджета TextInput и JavaScript.

## IntegerField
        class IntegerField([**options])
Число. Значение от -2147483648 до 2147483647 для всех поддерживаемых баз данных Django. Форма использует виджет TextInput.


## SmallIntegerField
        class SmallIntegerField([**options])
Как и поле IntegerField, но принимает значения в определенном диапазоне(зависит от типа базы данных). Для баз данных поддерживаемых Django можно использовать значения от -32768 до 32767.


## TimeField
        class TimeField([auto_now=False, auto_now_add=False, **options])
Время, представленное объектом datetime.time Python. Принимает те же аргументы, что и DateField.

Форма использует виджет TextInput. Интерфейс администратора также использует немного JavaScript.


Создание суперпользователя
===========================

        $ python manage.py createsuperuser

Запускаем сервер для разработки
-------------------------------

        $ python manage.py runserver

Откроем “/admin/” локального домена в браузере – http://127.0.0.1:8000/admin/. Вы должны увидеть страницу авторизации интерфейса администратора

Добавим приложение shop в интерфейс администратора
--------------------------------------------------
Нам нужно указать, что объекты модели Category и Product могли редактироваться в интерфейсе администратора. 

shop/admin.py
-------------

        from django.contrib import admin
        from .models import Category, Product

        admin.site.register(Category)
        admin.site.register(Product)


Поля формы формируются на основе описания модели Category и Product.

Для различных типов полей модели (DateTimeField, CharField) используются соответствующие HTML поля. Каждое поле знает как отобразить себя в интерфейсе администратора.

К полям DateTimeField добавлен JavaScript виджет. Для даты добавлена кнопка “Сегодня” и календарь, для времени добавлена кнопка “Сейчас” и список распространенных значений.

В нижней части страницы мы видим несколько кнопок:

Save – сохранить изменения и вернуться на страницу списка объектов.

Save and continue editing – сохранить изменения и снова загрузить страницу редактирования текущего объекта.

Save and add another – Сохранить изменения и перейти на страницу создания нового объекта.

Delete – Показывает страницу подтверждения удаления.

Мыкет проекта
==============
```
.
├── db.sqlite3
├── functional_tests
│   ├── __init__.py
│   └── tests.py
├── static
│   ├── favicon.ico
│   ├── css
│   │   ├── main.css
│   │   ├── bootstrap.css
│   │   ├── bootstrap-theme.css
│   │   └── bootstrap.css.map
│   ├── js
│   │   ├── main.js
│   │   ├── plugins.js
│   │   └── vendor
│   ├── img
│   │   └── star.png
│   └── fonts
│       ├── glyphicons-halflings-regular.eot
│       ├── glyphicons-halflings-regular.svg
│       ├── glyphicons-halflings-regular.ttf
│       └── glyphicons-halflings-regular.woff
├── templates
│   ├── base.html
│   ├── 404.html
│   ├── home
│   │   └── index.html
│   └── shop
│       └── product
│           └── index.html
├── shop
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── home
│   ├── admin.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── __pycache__
│   ├── tests.py
│   └── views.py
├── manage.py
└── mysite
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

mysite/settings.py
------------------

        STATIC_URL = '/static/'

        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
        )

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

shop/urls.py
------------
        """shop URL Configuration
        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            
        ]

shop/views.py
-------------
        from django.shortcuts import render

        def index(request):
            return render(request,'shop/product/index.html')


templates/home/index.html
-------------------------

        {% extends "base.html" %}
        {% load static %}

            {% block title %}My Cool Django Site{% endblock %}

        {% block content %}

                <!-- Main jumbotron for a primary marketing message or call to action -->
            <div class="jumbotron">
              <div class="container">
                <h1>Hello, world!</h1>
                <p>This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.</p>
                <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a></p>
              </div>
            </div>

            <div class="container">
              <!-- Example row of columns -->
              <div class="row">
                <div class="col-md-4">
                  <h2>Heading</h2>
                  <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
                  <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
                </div>
                <div class="col-md-4">
                  <h2>Heading</h2>
                  <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
                  <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
               </div>
                <div class="col-md-4">
                  <h2>Heading</h2>
                  <p>Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
                  <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
                </div>
              </div>

              <hr>
        {% endblock %}

templates/base.html
-------------------

        {% load staticfiles %}
        <!doctype html>
        <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7" lang=""> <![endif]-->
        <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8" lang=""> <![endif]-->
        <!--[if IE 8]>         <html class="no-js lt-ie9" lang=""> <![endif]-->
        <!--[if gt IE 8]><!--> <html class="no-js" lang=""> <!--<![endif]-->
            <head>
                <meta charset="utf-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
                <title>{% block title %}{% endblock %}</title>
                <meta name="description" content="">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="apple-touch-icon" href="apple-touch-icon.png">
                <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
                <style>
                    body {
                        padding-top: 50px;
                        padding-bottom: 20px;
                    }
                </style>
                <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
                <link rel="stylesheet" href="{% static 'css/main.css' %}">
                <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}"></script>
            </head>
            <body>
                <!--[if lt IE 8]>
                    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
                <![endif]-->
            <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
              <div class="container">
                <div class="navbar-header">
                  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                  </button>
                  <a class="navbar-brand" href="/">Project name</a>
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                  <ul class="nav navbar-nav">
                    <li class="active"><a href="/">Home <span class="sr-only">(current)</span></a></li>
                    <li><a href="/shop">Shop</a></li>
                  </ul>
                  <form class="navbar-form navbar-right" role="form">
                    <div class="form-group">
                      <input type="text" placeholder="Email" class="form-control">
                    </div>
                    <div class="form-group">
                      <input type="password" placeholder="Password" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-success">Sign in</button>
                  </form>
                </div><!--/.navbar-collapse -->
              </div>
            </nav>

             <div id="content">
                {% block content %}
                {% endblock %}
            </div>

              <footer>
                <p>&copy; Company 2016</p>
              </footer>
            </div> <!-- /container -->        
                <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
                <script>window.jQuery || document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>

                <script src="{% static 'js/vendor/bootstrap.min.js' %}">
                <script src="{% static 'js/plugins.js' %}">
                <script src="{% static 'js/main.js' %}">
                
                <!-- Google Analytics: change UA-XXXXX-X to be your site's ID. -->
                <script>
                    (function(b,o,i,l,e,r){b.GoogleAnalyticsObject=l;b[l]||(b[l]=
                    function(){(b[l].q=b[l].q||[]).push(arguments)});b[l].l=+new Date;
                    e=o.createElement(i);r=o.getElementsByTagName(i)[0];
                    e.src='//www.google-analytics.com/analytics.js';
                    r.parentNode.insertBefore(e,r)}(window,document,'script','ga'));
                    ga('create','UA-XXXXX-X','auto');ga('send','pageview');
                </script>
            </body>
        </html>


templates/shop/index.html
-------------------------
            {% extends "base.html" %}
            {% load static %}

            {% block title %}Products{% endblock %}

            {% block content %}
                <div class="container">
                  <!-- row of columns -->
                  <div class="row">
                    <div class="col-md-4 sidebar">
                        <h3>Categories</h3>
                        <ul>
                            <li>
                                <a href="{% url "shop:index" %}">All</a>
                            </li>
                        </ul>
                    </div>
                    <div id="main" class="col-md-8 product-list">
                        <h1>Products</h1>
                        {% for product in products %}
                            <div class="item">
                            </div>
                        {% endfor %}
                    </div>
                  </div>
                  <hr>
            {% endblock %}

shop/views.py
-------------

        from django.shortcuts import render
        from .models import Product

        def index(request):
            products = Product.objects.filter(available=True)
            
            return render(request, 'shop/product/index.html', {'products': products})

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
                        <li>
                            <a href="{% url "shop:index" %}">All</a>
                        </li>
                    </ul>
                </div>

                <div id="main" class="col-md-8 product-list">
                    <h1>Products</h1>
                    {% for product in products %}
                        <div class="item">
                            <h2>{{ product.name }}</h3>
                            <h4>${{ product.price }}</h4>
                            <p>{{ product.description }}</p>
                        </div>
                    {% endfor %}
                
                </div>
              </div>
             <hr>
        {% endblock %}

shop/views.py
-------------
from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/index.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id, available=True)
    return render(request,'shop/product/detail.html', {'product': product })

shop/urls.py
-------------
        """shop URL Configuration
        """
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'^(?P<id>\d+)/$', views.product_detail, name='product_detail'),
        ]

templates/shop/product/detail.html
----------------------------------
        {% extends "base.html" %}
        {% load static %}

        {% block title %}{{ product.name }}{% endblock %}

        {% block content %}
            <div class="product-detail">
                <h1>{{ product.name }}</h1>
                <p class="price">${{ product.price }}</p>
                {{ product.description|linebreaks }}
            </div>
        {% endblock %}

templates/shop/product/index.html
----------------------------------
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
                            <li>
                                <a href="{% url "shop:index" %}">All</a>
                            </li>
                        </ul>
                    </div>

                    <div id="main" class="col-md-8 product-list">
                        <h1>Products</h1>
                        {% for product in products %}
                            <div class="item">
                                <a href= '{% url "shop:product_detail" product.id %}' ><h2>{{ product.name }}</h2></a>
                                <h4>${{ product.price }}</h4>
                                <p>{{ product.description }}</p>
                            </div>
                        {% endfor %}
                    
                    </div>
                  </div>
                 <hr>
            {% endblock %}
        
        
