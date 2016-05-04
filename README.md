# tdd-django unit_14

Своя CMS
========

настройки для Grappelli
=======================
http://django-grappelli.readthedocs.io/en/latest/quickstart.html

# For better admin interface, add the dashboard:
    GRAPPELLI_INDEX_DASHBOARD = 'pages.dashboard.PagesDashboard'

# Add grappelli, filebrowser and django_pages to INSTALLED_APPS:
        INSTALLED_APPS = (
            'grappelli.dashboard',
            'grappelli',
            ...
            'filebrowser',
            'django_pages'
        )

Установка MEDIA_ROOT path
-------------------------
    The Default FILEBROWSER_DIRECTORY is "uploads" so you should check if '/media/uploads' exists

Можно поменять в settings.py FILEBROWSER_DIRECTORY

DIRECTORY (относительно MEDIA_ROOT)
-----------------------------------
Главная FileBrowser Directory. Оставте пустой для обзора всех файлов в MEDIA_ROOT:

    DIRECTORY = getattr(settings, "FILEBROWSER_DIRECTORY", 'uploads/')

FileBrowser Media, TinyMCE Media
---------------------------------
    URL_FILEBROWSER_MEDIA, PATH_FILEBROWSER_MEDIA

URL и Path к FileBrowser media-files:
-------------------------------------
    URL_FILEBROWSER_MEDIA = getattr(settings, "FILEBROWSER_URL_FILEBROWSER_MEDIA", settings.STATIC_URL + "filebrowser/")
    PATH_FILEBROWSER_MEDIA = getattr(settings, "FILEBROWSER_PATH_FILEBROWSER_MEDIA", os.path.join(settings.STATIC_ROOT, 'filebrowser/'))

URL_TINYMCE, PATH_TINYMCE
-------------------------
    URL_TINYMCE = getattr(settings, "FILEBROWSER_URL_TINYMCE", settings.ADMIN_MEDIA_PREFIX + "tinymce/jscripts/tiny_mce/")
    PATH_TINYMCE = getattr(settings, "FILEBROWSER_PATH_TINYMCE", settings.ADMIN_MEDIA_PREFIX + "tinymce/jscripts/tiny_mce/")

Dashboard
=========

        # -*- encoding: utf-8 -*-

        from django.utils.translation import ugettext_lazy as _

        from grappelli.dashboard import modules, Dashboard
        from grappelli.dashboard.utils import get_admin_site_name


        class PagesDashboard(Dashboard):
            """
            Custom index dashboard for Django-pages
            """

            def init_with_context(self, context):
                site_name = get_admin_site_name(context)


                self.children.append(
                    modules.ModelList(
                        _('Pages'),
                        column=1,
                        collapsible=True,
                        models=('pages.models.*', )
                    )
                )

                self.children.append(
                    modules.AppList(
                        _('Administration'),
                        column=1,
                        collapsible=False,
                        models=('django.contrib.*', )
                    )
                )

                self.children.append(modules.LinkList(
                    _('File Management'),
                    column=3,
                    children=[
                        {
                            'title': _('File Browser'),
                            'url': '/admin/filebrowser/browse/',
                            'external': False,
                        },
                    ]
                ))

                self.children.append(modules.RecentActions(
                    _('Recent Actions'),
                    limit=5,
                    collapsible=False,
                    column=3,
                ))

Модель
------

        # -*- coding:utf-8 -*-
        """Django page ``models``."""

        from django.db import models

        from django.utils.translation import ugettext_lazy as _
        from django.utils.encoding import python_2_unicode_compatible
        from django.conf import settings as django_settings
        from mptt.models import MPTTModel
        from .utils import get_now
        from . import settings
        import uuid

        @python_2_unicode_compatible
        class Page(MPTTModel):
            # some class constants to refer to, e.g. Page.DRAFT
            DRAFT = 0
            PUBLISHED = 1
            EXPIRED = 2
            HIDDEN = 3
            STATUSES = (
                (PUBLISHED, _('Published')),
                (HIDDEN, _('Hidden')),
                (DRAFT, _('Draft')),
            )

            # used to identify pages across different databases
            uuid = models.UUIDField(default=uuid.uuid4, editable=False)

            author = models.ForeignKey(django_settings.AUTH_USER_MODEL,
                    verbose_name=_('author'))

            parent = models.ForeignKey('self', null=True, blank=True,
                    related_name='children', verbose_name=_('parent'))
            creation_date = models.DateTimeField(_('creation date'), editable=False,
                    default=get_now)
            publication_date = models.DateTimeField(_('publication date'),
                    null=True, blank=True, help_text=_('''When the page should go
                    live. Status must be "Published" for page to go live.'''))
            publication_end_date = models.DateTimeField(_('publication end date'),
                    null=True, blank=True, help_text=_('''When to expire the page.
                    Leave empty to never expire.'''))

            last_modification_date = models.DateTimeField(_('last modification date'))

            status = models.IntegerField(_('status'), choices=STATUSES, default=DRAFT)
            template = models.CharField(_('template'), max_length=100, null=True,
                    blank=True)

            delegate_to = models.CharField(_('delegate to'), max_length=100, null=True,
                    blank=True)

            freeze_date = models.DateTimeField(_('freeze date'),
                    null=True, blank=True, help_text=_('''Don't publish any content
                    after this date.'''))

            redirect_to_url = models.CharField(max_length=200, null=True, blank=True)

            redirect_to = models.ForeignKey('self', null=True, blank=True,
                related_name='redirected_pages')

            class Meta:
                """Make sure the default page ordering is correct."""
                ordering = ['tree_id', 'lft']
                get_latest_by = "publication_date"
                verbose_name = _('page')
                verbose_name_plural = _('pages')

            def __init__(self, *args, **kwargs):
                """Instanciate the page object."""
                # per instance cache
                self._languages = None
                self._content_dict = None
                self._is_first_root = None
                self._complete_slug = None
                super(Page, self).__init__(*args, **kwargs)

            def _get_calculated_status(self):
                """Get the calculated status of the page based on
                :attr:`Page.publication_date`,
                :attr:`Page.publication_end_date`,
                and :attr:`Page.status`."""
                if settings.PAGE_SHOW_START_DATE and self.publication_date:
                    if self.publication_date > get_now():
                        return self.DRAFT

                if settings.PAGE_SHOW_END_DATE and self.publication_end_date:
                    if self.publication_end_date < get_now():
                        return self.EXPIRED

                return self.status
            _get_calculated_status.short_description = _('Get the calculated status of the page based on :attr: Page.publication_date, :attr: Page.publication_end_date and :attr: Page.status')
            calculated_status = property(_get_calculated_status)

            def _visible(self):
                """Return True if the page is visible on the frontend."""
                return self.calculated_status in (self.PUBLISHED, self.HIDDEN)
            visible = property(_visible)

class Content
-------------
        @python_2_unicode_compatible
        class Content(models.Model):
            """
            A block of content, tied to a :class:`Page <pages.models.Page>`,
            for a particular language`.
            """
            page = models.ForeignKey(Page, verbose_name=_('Page'))
            type = models.CharField(_('type'), max_length=100, blank=False,
                db_index=True)
            body = models.TextField(_('Post content'))
            creation_date = models.DateTimeField(_('creation date'), editable=False,
                default=get_now)
            comments = models.BooleanField(_('Enable comments'), blank=True)

            def __str__(self):
                return u"{0} :: {1}".format(self.page.slug(), self.body[0:15])

            class Meta:
                get_latest_by = 'creation_date'
                verbose_name = _('Content')
                verbose_name_plural = _('Contents')


admin.py
--------

        from django.contrib import admin

        from .models import Page, Content
            
        admin.site.register(Page)
        admin.site.register(Content)


tinymce.widgets
---------------

        from django.contrib import admin
        from django import forms
        from .models import Page, Content
        from tinymce.widgets import TinyMCE
            
        admin.site.register(Page)

        class ContentAdminForm(forms.ModelForm):
            body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

            class Meta:
                model = Content
                fields = '__all__'

        class ContentAdmin(admin.ModelAdmin):
            form = ContentAdminForm

        admin.site.register(Content,ContentAdmin)

settings.py
-----------

        TINYMCE_DEFAULT_CONFIG = {
            'theme': "advanced",
        }


Система кэширования Django
==========================
Главная хитрость современных веб сайтов в том, что они динамичные. Каждый раз, когда пользователь запрашивает страницу, веб сервер производит множество действий, от запросов к базе данных до обработки шаблонов, чтобы создать страницу, которую увидит посетитель вашего сайта. Это требует больше затрат, с точки зрения использования ресурсов, чем статичная выдача файла с файловой системы.

Для большинства веб приложений такие лишние вычисления не особо заметны. Эти приложения не являются сайтами washingtonpost.com или slashdot.org. Это сайты небольшого или среднего размера с небольшим трафиком. Но для более крупных сайтов становится очень важна экономия ресурсов.

Кэширование означает сохранение результатов дорогостоящего вычисления, чтобы избежать его повторного вычисления в следующий раз. Ниже представлен псевдокод объясняющий как работает кэширование для динамически созданной веб страницы:

        given a URL, try finding that page in the cache
        if the page is in the cache:
            return the cached page
        else:
            generate the page
            save the generated page in the cache (for next time)
            return the generated page


Django поставляется с надёжной системой кэширования, которая позволяет вам сохранять динамические страницы так, что не потребуется их создавать для каждого запроса. Для удобства, Django даёт возможность тонкого управления уровнем кэширования: вы можете кэшировать результат работы представления, вы можете кэшировать только те куски, которые трудно вычислять или вы можете кэшировать весь ваш сайт.

Django также может работать с «даунстрим» кэшами, такими как Squid и кэшами браузеров. Это такие типы кэшей, которые вы не можете контролировать напрямую, но можете определять их поведение подсказками (через HTTP заголовки) о том, какую часть вашего сайта следует кэшировать и как.

Настройка кэша
--------------
Система кэширования требует небольшой настройки. А именно, надо указать где должны располагаться закэшированные данные – в базе данных, на файловой системе или прямо в памяти. Это важное решение, которое повлияет на производительность вашего кэша. Да, типы кэшей различаются по скорости работы.

Настройки кэша определяются параметром конфигурации CACHES. 

Memcached
---------
Самый быстрый и эффективный тип кэша, доступный Django, Memcached является кэшем, который полностью располагается в оперативной памяти, он был разработан для LiveJournal.com и позднее переведён в опенсорс компанией Danga Interactive. Он используется такими сайтами как Facebook и Wikipedia для снижения нагрузки на базу данных и значительного увеличения производительности сайта.

Memcached работает как демон и захватывает определённый объём оперативной памяти. Его задачей является представление быстрого интерфейса для добавления, получения и удаления определённых данных в кэше. Все данные хранятся прямо в оперативной памяти, таким образом нет никакой дополнительной нагрузки на базу данных или файловую систему.

После установкам самого Memcached, следует установить его пакет для Python. Существует несколько таких пакетов; два наиболее используемых — python-memcached и pylibmc.

Для использования Memcached с Django:
-------------------------------------
Установите BACKEND в django.core.cache.backends.memcached.MemcachedCache или django.core.cache.backends.memcached.PyLibMCCache (зависит от выбранного пакета).

Определите для LOCATION значение ip:port (где ip — это IP адрес, на котором работает демон Memcached, port — его порт) или unix:path (где path является путём к файлу-сокету Memcached).

В этом примере Memcached запущен на localhost (127.0.0.1) порт 11211, используя python-memcached:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': '127.0.0.1:11211',
            }
        }
В этом примере Memcached доступен через локальный файл-сокет /tmp/memcached.sock, используя python-memcached:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': 'unix:/tmp/memcached.sock',
            }
        }
При использовании pylibmc, не включайте префикс unix:/:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
                'LOCATION': '/tmp/memcached.sock',
            }
        }
Одной из замечательных особенностей Memcached является возможность распределять кэш по нескольким серверам. Это означает, что вы можете запустить демоны Memcached на нескольких машинах и программа будет рассматривать эту группу машин как единый кэш, без необходимости копирования всех значений кэша на каждую машину. Для того, чтобы воспользоваться этой особенностью, укажите адреса всех машин в LOCATION, в виде списка или строки, разделённой запятыми.

В данном примере, кэш распределён по экземплярам Memcached, работающим на IP адресах 172.19.26.240 и 172.19.26.242, на порту 11211 оба:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': [
                    '172.19.26.240:11211',
                    '172.19.26.242:11211',
                ]
            }
        }
В следующем примере, кэш распределён по экземплярам Memcached, работающим на IP адресах 172.19.26.240 (порт 11211), 172.19.26.242 (порт 11212) и на 172.19.26.244 (порт 11213):

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': [
                    '172.19.26.240:11211',
                    '172.19.26.242:11212',
                    '172.19.26.244:11213',
                ]
            }
        }
этот тип кэша имеет один недостаток: Кэш располагается в оперативной памяти и уничтожается при сбое сервера. Очевидно, что оперативная память не предназначена для постоянного хранения информации, поэтому не следует на неё рассчитывать в этом смысле. Несомненно, ни один из модулей кэширования не должен использоваться как постоянное хранилище — они предназначены для кэширования, не для хранения — мы особенно это отмечаем для данного типа кэша.


cache.py
--------
        # -*- coding: utf-8 -*-

        from django.core.cache import caches
        from django.core.cache.backends.base import InvalidCacheBackendError

        try:
            cache = caches['pages']
        except InvalidCacheBackendError:
            cache = caches['default']

Кэширование в базу данных
-------------------------
Кэширование в базу данных отлично работает в случае, если у вас есть быстрый сервер баз данных с поддержкой индексирования.

Для использования таблицы базы данных в качестве бэкэнда кэша:

Установите BACKEND в django.core.cache.backends.db.DatabaseCache

Установите LOCATION в tablename, имя таблицы базы данных. Это имя может быть любым, пока оно не противоречит правилам именования таблиц в вашей базе данных и не занято другой таблицей.

В данном примере, именем таблицы для кэша будет my_cache_table:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'my_cache_table',
            }
        }
Создание таблицы для кэша
-------------------------
Для того, чтобы использовать таблицу базы данных в качестве кэша, сначала надо её создать с помощью следующей команды:

python manage.py createcachetable
В результате в базе данных будет создана таблица, структура которой соответствует ожиданиям системы кэширования. Имя для таблицы будет взято из параметра LOCATION.

При использовании нескольких БД кэшей, команда createcachetable создаст по одной таблице для каждого кэша.

Если вы используете множество баз данных, то команда createcachetable обратится к методу allow_migrate() роутера вашей базы данных.

Аналогично команде migrate, команда createcachetable не внесёт изменения в существующую таблицу. Она создаёт только отсутствующие таблицы.

Чтобы вывести SQL, который был бы выполнен, без его выполнения, используйте опцию --dry-run.

Множество баз данных
---------------------
Если у вас несколько баз данных и вы планируете использовать кэширование, потребуется прописать инструкции роутинга для таблицы кэширования. В целях роутинга таблица кэширования представлена моделью CacheEntry в приложении django_cache. Эта модель не отобразится в модельном кэше, но содержимое модели может быть использовано для роутинга.

Например, представленный ниже роутер будет перенаправлять все операции чтения из кэша на cache_replica, а всё операции записи на cache_primary. Таблица кэширования будет синхронизироваться только с cache_primary:

        class CacheRouter(object):
            """A router to control all database cache operations"""

            def db_for_read(self, model, **hints):
                "All cache read operations go to the replica"
                if model._meta.app_label == 'django_cache':
                    return 'cache_replica'
                return None

            def db_for_write(self, model, **hints):
                "All cache write operations go to primary"
                if model._meta.app_label == 'django_cache':
                    return 'cache_primary'
                return None

            def allow_migrate(self, db, app_label, model_name=None, **hints):
                "Only install the cache model on primary"
                if app_label == 'django_cache':
                    return db == 'cache_primary'
                return None
Если вы не настроите роутинг для кэширования, то модуль кэширования будет использовать базу default.

Естественно, если вы не используете базу данных для кэша, вам не надо беспокоиться об инструкциях роутинга.

Кэширование на файловую систему
-------------------------------
Файловый бэкэнд сериализует и сохраняет каждое закэшированное значение в отдельном файле. Для использования этого бэкэнда, установите BACKEND в "django.core.cache.backends.filebased.FileBasedCache", а для LOCATION укажите подходящий каталог. Например, для хранения закэшированных данных в /var/tmp/django_cache, используйте такую настройку:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/django_cache',
            }
        }
Если вы используете Windows, то подставьте букву диска в начало пути, вот так:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': 'c:/foo/bar',
            }
        }
Путь до каталога должен быть абсолютным, т.е. он должен начинаться от корня файловой системы. Завершающий слэш не имеет значения.

Следует удостовериться, что указанный каталог существует и доступен для чтения и записи для пользователя, от которого работает ваш веб сервер. Продолжая предыдущий пример, если ваш веб сервер запущен от пользователя apache, проверьте, что каталог /var/tmp/django_cache существует и доступен для чтения и записи пользователю apache.

Кэширование в оперативной памяти
--------------------------------
Это стандартный кэш, который применяется, если другой не определён в вашем файле конфигурации. Если вам требуется высокая скорость работы кэша, но у вас нет возможности развернуть Memcached, рассмотрите вариант использования кэша в оперативной памяти. Этот кэш по-процессный и потокобезопасный. Для его использования надо параметру конфигурации BACKEND присвоить значение "django.core.cache.backends.locmem.LocMemCache". Например:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'unique-snowflake',
            }
        }
Параметр конфигурации LOCATION используется для идентификации отдельных хранилищ в памяти. Если у вас только один такой кэш, то вы можете пропустить этот параметр. Однако, в случае нескольких кэшей, вам потребуется назначить имя хотя бы для одного из них, для их различия.

Следует отметить, что каждый процесс будет работать со своим собственным экземпляром кэша, что означает невозможность разделения одного кэша между процессами. Это означает, что кэш данного типа неэкономно использует оперативную память и, возможно, не будет хорошим выбором для боевого окружения. Он хорош на время разработки.

Псевдокэширование (для разработки)
----------------------------------
Django поставляется с «псевдо» кэшем, который не выполняет собственно кэширование. Он просто реализует интерфейс кэша, не делая больше ничего.

Он полезен в случае, когда у вас есть боевой сайт , который плотно использует кэширование в различных местах, а также окружение разработки или тестирование, где кэшировать ничего не надо. Для активации псевдо кэширования, установите BACKEND:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
Использование собственного модуля кэширования
---------------------------------------------
Несмотря на то, что Django предоставляет ряд модулей кэширования, вам может потребоваться использовать свой кэширующий модуль. Для подключения внешнего кэширующего модуля используйте путь до него в качестве значения BACKEND параметра конфигурации CACHES, вот так:

        CACHES = {
            'default': {
                'BACKEND': 'path.to.backend',
            }
        }
При создании своего кэширующего модуля вы можете использовать стандартные модули в качестве примера. Их код располагается в каталоге django/core/cache/backends/ исходного кода Django.

Следует отметить, если нет важной причины для использования собственного кэширующего модуля, вы должны использовать кэширующие модули, поставляемые с Django. Они протестированы и просты в использовании.

Параметры кэша
--------------
После определения типа кэша и имени для каждого из них, для каждого модуля можно указать дополнительные аргументы для управления поведением кэша. Эти аргументы представляются в виде дополнительных ключей в параметре конфигурации CACHES. Приведём список допустимых аргументов:

TIMEOUT: время устаревания кэша по умолчанию, в секундах. По умолчанию 300 секунд (5 минут). Вы можете установить TIMEOUT в None, тогда кэш никогда не устареет. Если указать 0, все ключи будут сразу устаревать (таким образом можно заставить “не кэшировать”).

OPTIONS: Любая опция, которая должна быть передана модулю. Список допустимых опций варьируется от модуля к модулю и передается непосредственно в библиотеку для кэширования.

Модули кэширования, которые реализуют собственную стратегию очистки (т.е., модули locmem, filesystem и database) учитывают следующие опции:

MAX_ENTRIES: максимальное количество элементов в кэше перед началом удаления старых значений. Обычно, 300 элементов.

CULL_FREQUENCY: Часть элементов, которые надо удалить при достижении MAX_ENTRIES. Обычное соотношение — 1/CULL_FREQUENCY, таким образом, надо установить CULL_FREQUENCY в 2, чтобы удалять половину значений кэша при достижении MAX_ENTRIES. Аргумент должен быть целым числом и по умолчанию равен 3.

Значение 0 для CULL_FREQUENCY означает, что весь кэш должен быть сброшен при достижении MAX_ENTRIES. Это делает очистку значительно быстрее для определенных бэкендов(в частности database) ценой увеличения промахов кэша.

KEY_PREFIX: Строка, которая автоматически включается (предваряет, по умолчанию) во все ключи кэша, используемые сервером Django.

VERSION: Номер версии про умолчанию для ключей кэша, созданных сервером Django.

KEY_FUNCTION Строка, содержащая путь до функции, которая определяет правила объединения префикса, версии и ключа в итоговый ключ кэша.

В этом примере, модуль кэширования на файловую систему настроен на таймаут в 60 секунд и ёмкость в 1000 элементов:

        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/django_cache',
                'TIMEOUT': 60,
                'OPTIONS': {
                    'MAX_ENTRIES': 1000
                }
            }
        }
Неправильные аргументы игнорируются без ошибок, ка к и неправильные значения поддерживаемых аргументов.

language/models.py
------------------
        # -*- encoding: utf-8 -*-

        from django.db import models
        from django.core.files.storage import FileSystemStorage
        from django.utils.translation import ugettext_lazy as _
        from django.utils.encoding import python_2_unicode_compatible
        from django.http import Http404
        from pages.common.errors import ConfigurationError
        from pages.settings import FLAG_UPLOAD_DIR

        IMAGES_DIR = FileSystemStorage(FLAG_UPLOAD_DIR)

        @python_2_unicode_compatible
        class Language(models.Model):
            """
            Stores single language with optional flag image.
            Country Code will be part of URL in lowercase.
            """
            language = models.CharField(_('Language'), max_length=150, unique=True)
            country_code = models.CharField(
                _('Country code'),
                help_text=_('(US, UK, CZ, SK, ...)'),
                max_length=3,
                unique=True
            )
            flag = models.ImageField(
                _('Flag'),
                help_text=_('Flag image to display on page.'),
                storage=IMAGES_DIR,
                upload_to='languages',
                blank=True
            )
            default = models.BooleanField(
                _('Default'),
                help_text=_('Display as default language?'),
                blank=True
            )
            active = models.BooleanField(_('Active'), blank=True, default=True)

            def __str__(self):
                return self.language

            def save(self, *args, **kwargs):
                """
                override save method to check wheter it is first language.
                and if so, check default to True.
                if not, check if some other language has default set to True.
                if not, do not allow to set it to False.
                """
                if not self.default:
                    if not Language.objects.exists():
                        self.default = True

                else:
                    others = Language.objects.filter(default=True).exclude(id=self.id)

                    for other_default in others:
                        other_default.default = False
                        # call super.save on this, so we don't check all this again
                        super(Language, other_default).save(*args, **kwargs)

                    self.default = True

                self.country_code = self.country_code.lower()
                super(Language, self).save(*args, **kwargs)

            def delete(self, *args, **kwargs):
                """
                override delete method to check if any other language has default set.
                if not, set language with lowest ID as default.
                """
                super(Language, self).delete(*args, **kwargs)

                if not Language.objects.filter(default=True):
                    new_default = Language.objects.all().order_by('id')

                    if new_default:
                        new_default = new_default[0]
                        new_default.default = True
                        new_default.save()

            class Meta:
                
                verbose_name = _('Language')
                verbose_name_plural = _('Languages')



common/errors.py
----------------
        # -*- encoding: utf-8 -*-

        """
        Custom errors definition
        """

        from django.core.exceptions import ImproperlyConfigured


        class ConfigurationError(ImproperlyConfigured):

            def __init__(self, *args, **kwargs):
                super(ConfigurationError, self).__init__(*args, **kwargs)

common.admin_actions.py
-----------------------
        from django.utils.translation import ugettext_lazy as _

        def activate(modeladmin, request, queryset):
            queryset.update(status=PUBLISHED)

        activate.short_description = _('Activate selected items.')

        def deactivate(modeladmin, request, queryset):
            queryset.update(status=DRAFT)

        deactivate.short_description = _('Deactivate selected items.')

pages/admin.py
--------------
        from .common.admin_actions import activate, deactivate
            
        class PageAdmin(admin.ModelAdmin):
            fieldsets = (
                (None, {
                    'fields': (
                        'title',
                        'slug',
                        'author',
                        'parent',
                        'publication_date',
                        'publication_end_date',
                        'last_modification_date',
                        'status',
                        'template',
                        'delegate_to',
                        'freeze_date',
                        'redirect_to_url',
                        'redirect_to',
                    )
                }),
            )
            
            actions = [activate, deactivate]


pages/settings.py
-----------------
        # -*- coding: utf-8 -*-
        """Convenience module that provides default settings for the ``pages``
        application when the project ``settings`` module does not contain
        the appropriate settings."""
        from django.conf import settings

        # Show the publication start date field in the admin.  Allows for future dating
        # Changing the ``PAGE_SHOW_START_DATE``  from ``True`` to ``False``
        # after adding data could cause some weirdness.  If you must do this, you
        # should update your database to correct any future dated pages.
        PAGE_SHOW_START_DATE = getattr(settings, 'PAGE_SHOW_START_DATE', False)

        # Show the publication end date field in the admin, allows for page expiration
        # Changing ``PAGE_SHOW_END_DATE`` from ``True`` to ``False`` after adding
        # data could cause some weirdness.  If you must do this, you should update
        # your database and null any pages with ``publication_end_date`` set.
        PAGE_SHOW_END_DATE = getattr(settings, 'PAGE_SHOW_END_DATE', False)

        ADMIN_MEDIA_PREFIX = getattr(settings, 'ADMIN_MEDIA_PREFIX', '/static/admin/')

        # where to upload flag images /media/FLAG_UPLOAD_DIR
        FLAG_UPLOAD_DIR = getattr(settings, 'FLAG_UPLOAD_DIR', settings.MEDIA_ROOT)


mediadata/models.py
-------------------
        # -*- encoding: utf-8 -*-

        from django.db import models
        from django.utils.translation import ugettext_lazy as _
        from django.utils.encoding import python_2_unicode_compatible
        from pages.language.models import Language

        @python_2_unicode_compatible
        class MetaSet(models.Model):
            """
            Stores MetaData configurations
            """

            language = models.ForeignKey(Language, verbose_name=_('Language'))
            name = models.CharField(
                _('Name'),
                help_text=_('Name of meta set (for identification).'),
                max_length=200
            )

            def __str__(self):
                return self.name

            class Meta:
                
                verbose_name = _('Meta set')
                verbose_name_plural = _('Meta sets')

        @python_2_unicode_compatible
        class MetaData(models.Model):
            """
            Stores MetaData item
            """

            meta_set = models.ForeignKey(MetaSet, verbose_name=_('Meta set'))
            name = models.CharField(
                _('Name'),
                help_text=_('Name of meta tag &lt;meta name="THIS NAME" ... &gt;'),
                max_length=200
            )
            content = models.TextField(
                _('Content'),
                help_text=_('Content of meta tag &lt;meta ... content="THIS CONTENT" &gt;'),
                max_length=2000
            )

            def __str__(self):
                return self.name

            class Meta:
                
                verbose_name = _('Meta data')
                verbose_name_plural = _('Meta data')


pages/admin.py
--------------

        from django.contrib import admin
        from django import forms
        from .models import Page, Content
        from tinymce.widgets import TinyMCE
        from pages.language.models import Language
        from pages.metadata.models import MetaSet, MetaData
        from django.utils.translation import ugettext_lazy as _
        from .common.admin_actions import activate, deactivate

            
        class PageAdmin(admin.ModelAdmin):
            fieldsets = (
                (None, {
                    'fields': (
                        'title',
                        'slug',
                        'author',
                        'parent',
                        'publication_date',
                        'publication_end_date',
                        'last_modification_date',
                        'status',
                        'template',
                        'delegate_to',
                        'freeze_date',
                        'redirect_to_url',
                        'redirect_to',
                    )
                }),
            )

            actions = [activate, deactivate]
            

        admin.site.register(Page, PageAdmin)

        class ContentAdminForm(forms.ModelForm):
            body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

            class Meta:
                model = Content
                fields = '__all__'

        class ContentAdmin(admin.ModelAdmin):
            
            form = ContentAdminForm

        admin.site.register(Content,ContentAdmin)



        class LanguageAdminForm(forms.ModelForm):
            country_code = forms.RegexField(
                r'^[A-z]{2,3}$',
                label=_('Country code'),
                help_text=_('(US, UK, CZ, SK, ...)'),
                error_messages={
                    'invalid': _('2-3 letter combination required (US, UK, CZ, ...)')
                }
            )

            class Meta:
                fields = '__all__'
                model = Language


        class LanguageAdmin(admin.ModelAdmin):

            form = LanguageAdminForm
            fields = (('language', 'country_code'), 'flag', 'default', 'active')
            list_display = ('language', 'country_code', 'default', 'active')
            list_filter = ('active',)
            actions = [activate, deactivate]

        admin.site.register(Language, LanguageAdmin)



        class MetaDataInline(admin.TabularInline):

            model = MetaData


        class MetaSetAdmin(admin.ModelAdmin):

            fields = (('language', 'name'),)
            list_display = ('name', 'language')
            inlines = (MetaDataInline, )
            list_filter = ('language', )
            search_fields = ['metadata__name', 'metadata__content']


        class MetaDataAdmin(admin.ModelAdmin):

            list_display = ('name', 'content', 'meta_set')
            list_filter = ('meta_set__name', 'name')
            search_fields = ['content']

        admin.site.register(MetaSet, MetaSetAdmin)
        admin.site.register(MetaData, MetaDataAdmin)

PagesDashboard
---------------

        # -*- encoding: utf-8 -*-

        from django.utils.translation import ugettext_lazy as _

        from grappelli.dashboard import modules, Dashboard
        from grappelli.dashboard.utils import get_admin_site_name


        class PagesDashboard(Dashboard):
            """
            Custom index dashboard for Django-pages
            """

            def init_with_context(self, context):
                site_name = get_admin_site_name(context)

                self.children.append(
                    modules.ModelList(
                        _('General'),
                        column=1,
                        collapsible=True,
                        models=(
                            
                            'pages.language.models.*',
                            
                        ),
                    )
                )

                self.children.append(
                    modules.ModelList(
                        _('Pages'),
                        column=1,
                        collapsible=True,
                        models=('pages.models.*', )
                    )
                )

                self.children.append(
                    modules.ModelList(
                        _('SEO'),
                        column=2,
                        collapsible=True,
                        models=('pages.metadata.models.*', )
                    )
                )


                self.children.append(
                    modules.AppList(
                        _('Administration'),
                        column=1,
                        collapsible=False,
                        models=('django.contrib.*', )
                    )
                )

                self.children.append(modules.LinkList(
                    _('File Management'),
                    column=3,
                    children=[
                        {
                            'title': _('File Browser'),
                            'url': '/admin/filebrowser/browse/',
                            'external': False,
                        },
                    ]
                ))

                self.children.append(modules.RecentActions(
                    _('Recent Actions'),
                    limit=5,
                    collapsible=False,
                    column=3,
                ))


pages/models.py
---------------

            # -*- coding:utf-8 -*-
            """Django page ``models``."""

            from django.db import models
            from pages.cache import cache
            from django.utils.translation import ugettext_lazy as _
            from django.utils.encoding import python_2_unicode_compatible
            from django.conf import settings as django_settings
            from mptt.models import MPTTModel

            from .utils import get_now
            from . import settings
            import uuid
            from .language.models import *
            from .metadata.models import *

            @python_2_unicode_compatible
            class Page(MPTTModel):
                # some class constants to refer to, e.g. Page.DRAFT
                DRAFT = 0
                PUBLISHED = 1
                EXPIRED = 2
                HIDDEN = 3
                STATUSES = (
                    (PUBLISHED, _('Published')),
                    (HIDDEN, _('Hidden')),
                    (DRAFT, _('Draft')),
                )

                # used to identify pages across different databases
                uuid = models.UUIDField(default=uuid.uuid4, editable=False)

                title = models.CharField(_('Page title'), max_length=500)
                slug = models.SlugField(max_length=200, db_index=True, unique=True)

                metadata_set = models.ForeignKey(MetaSet, verbose_name=('Meta set'), null=True, blank=True)

                author = models.ForeignKey(django_settings.AUTH_USER_MODEL,
                        verbose_name=_('author'))

                parent = models.ForeignKey('self', null=True, blank=True,
                        related_name='children', verbose_name=_('parent'))
                creation_date = models.DateTimeField(_('creation date'), editable=False,
                        default=get_now)
                publication_date = models.DateTimeField(_('publication date'),
                        null=True, blank=True, help_text=_('''When the page should go
                        live. Status must be "Published" for page to go live.'''))
                publication_end_date = models.DateTimeField(_('publication end date'),
                        null=True, blank=True, help_text=_('''When to expire the page.
                        Leave empty to never expire.'''))

                last_modification_date = models.DateTimeField(_('last modification date'))

                status = models.IntegerField(_('status'), choices=STATUSES, default=DRAFT)
                template = models.CharField(_('template'), max_length=100, null=True,
                        blank=True)

                delegate_to = models.CharField(_('delegate to'), max_length=100, null=True,
                        blank=True)

                freeze_date = models.DateTimeField(_('freeze date'),
                        null=True, blank=True, help_text=_('''Don't publish any content
                        after this date.'''))


                redirect_to_url = models.CharField(max_length=200, null=True, blank=True)

                redirect_to = models.ForeignKey('self', null=True, blank=True,
                    related_name='redirected_pages')


                class Meta:
                    """Make sure the default page ordering is correct."""
                    ordering = ['tree_id', 'lft']
                    get_latest_by = "publication_date"
                    verbose_name = _('page')
                    verbose_name_plural = _('pages')
                    

                def __init__(self, *args, **kwargs):
                    """Instanciate the page object."""
                    # per instance cache
                    self._languages = None
                    self._content_dict = None
                    self._is_first_root = None
                    self._complete_slug = None
                    super(Page, self).__init__(*args, **kwargs)

                def _get_calculated_status(self):
                    """Get the calculated status of the page based on
                    :attr:`Page.publication_date`,
                    :attr:`Page.publication_end_date`,
                    and :attr:`Page.status`."""
                    if settings.PAGE_SHOW_START_DATE and self.publication_date:
                        if self.publication_date > get_now():
                            return self.DRAFT

                    if settings.PAGE_SHOW_END_DATE and self.publication_end_date:
                        if self.publication_end_date < get_now():
                            return self.EXPIRED

                    return self.status
                _get_calculated_status.short_description = _('Get the calculated status of the page based on :attr: Page.publication_date, :attr: Page.publication_end_date and :attr: Page.status')
                calculated_status = property(_get_calculated_status)

                def save(self, *args, **kwargs):
                    """Override the default ``save`` method."""
                    if not self.status:
                        self.status = self.DRAFT
                    # Published pages should always have a publication date
                    if self.publication_date is None and self.status == self.PUBLISHED:
                        self.publication_date = get_now()
                    # Drafts should not, unless they have been set to the future
                    if self.status == self.DRAFT:
                        if settings.PAGE_SHOW_START_DATE:
                            if (self.publication_date and
                                    self.publication_date <= get_now()):
                                self.publication_date = None
                        else:
                            self.publication_date = None
                    self.last_modification_date = get_now()
                    super(Page, self).save(*args, **kwargs)

                def _visible(self):
                    """Return True if the page is visible on the frontend."""
                    return self.calculated_status in (self.PUBLISHED, self.HIDDEN)
                visible = property(_visible)

                def __str__(self):
                    """Representation of the page, saved or not."""
                    if self.id:
                        # without ID a slug cannot be retrieved
                        return self.title
                    return "Page without id"