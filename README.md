# tdd-django unit_13

Своя CMS
========

настройки для Grappelli
=======================
http://django-grappelli.readthedocs.io/en/latest/quickstart.html

Installation
------------
    $ pip install django-grappelli


INSTALLED_APPS (before django.contrib.admin):
---------------------------------------------
        INSTALLED_APPS = (
            'grappelli',
            'django.contrib.admin',
        )

URL-patterns.
-------------
        urlpatterns = [
            url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
            url(r'^admin/', include(admin.site.urls)), # admin site
        ]

context processor (needed for the Dashboard and the Switch User feature):
--------------------------------------------------------------------------
        TEMPLATES = [
            {
                ...
                'OPTIONS': {
                    'context_processors': [
                        ...
                        'django.template.context_processors.request',
                        ...
                    ],
                },
            },
        ]


STATIC_ROOT
-----------
Значение по умолчанию изменено с '' (пустая строка) на None.

Абсолютный путь к каталогу, в который collectstatic соберет все статические файлы.

Если используется стандартное приложение staticfiles (по умолчанию), команда collectstatic соберет все статические файлы в указанном каталоге.

Это должен быть каталог(изначально пустой), куда будут скопированы все статические файлы для более простой настройки сервера; это не каталог, в котором вы создаете статические файлы при разработке. Вы должны создавать статические файлы в каталогах, которые будут найдены модулями поиска статических файлов. По умолчанию это подкаталоги 'static/' в приложениях и каталоги, указанные в STATICFILES_DIRS.

        STATIC_URL = '/static/'

        STATIC_ROOT = os.path.join(BASE_DIR, 'public')
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, "static"),
        )
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


Collect the media files:
------------------------
        $ python manage.py collectstatic

settings.py
-----------

        APP_TITLE = 'Janus CMS'

        GRAPPELLI_ADMIN_TITLE = APP_TITLE

настройки для FileBrowser
=========================
https://django-filebrowser.readthedocs.io/en/latest/quickstart.html

Installation
------------

    pip install django-filebrowser

INSTALLED_APPS (before django.contrib.admin):
---------------------------------------------
        INSTALLED_APPS = (
            'grappelli',
            'filebrowser',
            'django.contrib.admin',
        )

url-patterns (before any admin-urls):
-------------------------------------
        from filebrowser.sites import site

        urlpatterns = [
           url(r'^admin/filebrowser/', include(site.urls)),
           url(r'^grappelli/', include('grappelli.urls')),
           url(r'^admin/', include(admin.site.urls)),
        ]

Collect the static files:
-------------------------
    python manage.py collectstatic

settings.py
-----------

        FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT 
        FILEBROWSER_MEDIA_URL = MEDIA_URL 
        FILEBROWSER_STATIC_ROOT = STATIC_ROOT 
        FILEBROWSER_STATIC_URL = STATIC_URL 
        URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/' 
        PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/' 

настройки для tinyMCE
=====================
https://github.com/aljosa/django-tinymce

Install django-tinymce:

    $ pip install django-tinymce

INSTALLED_APPS settings.py:
---------------------------
        INSTALLED_APPS = (
            ...
            'tinymce',
        )

urls.py:
--------
        urlpatterns = [
            ...
            url(r'^tinymce/', include('tinymce.urls')),
        ]

Collect the static files:
-------------------------
    python manage.py collectstatic

In your code:
-------------
    from django.db import models
    from tinymce.models import HTMLField

    class MyModel(models.Model):
        ...
        content = HTMLField()

Интернационализация и локализация
=================================
https://docs.djangoproject.com/en/1.9/ref/settings/#globalization-i18n-l10n.

Целью интернационализации и локализации является обеспечение возможности отдельному веб приложению предоставлять свой контент на языке и в формате, понятном целевой аудитории.

Django обеспечивает две вещи:

- Он позволяет разработчикам и авторам шаблонов указывать какие именно части их приложений должны быть переведены или отформатированы под используемые языки и традиции.

- Он использует эти метки для локализации веб приложений под конкретного пользователя, учитывая его настройки.

Интернационализация
-------------------
Подготовка программного обеспечения для локализации. Обычно выполняется разработчиками.

Локализация
-----------
Создание переводов и локальных форматов. Обычно выполняется переводчиками.

Перевод и форматирование контролируются параметрами USE_I18N and USE_L10N соответственно. Тем не менее, оба функционала участвуют в интернационализации и локализации.

locale name
-----------
Имя локали, либо спецификация языка в виде ll или комбинация языка и спецификации страны в виде ll_CC. Примеры: it, de_AT, es, pt_BR. Языковая часть всегда указывается в нижнем регистре, а часть, определяющая страну, – в верхнем регистре. Разделителем является символ подчёркивания.

language code
-------------
Представляет имя языка. Используя этот формат, браузеры отправляют имена языков, контент на которых они предпочитают принять, в HTTP заголовке Accept-Language. Примеры: it, de-at, es, pt-br. Обе части (язык и страна) указываются в нижнем регистре, но HTTP заголовок Accept-Language регистронезависимый. Разделителем является символ тире.


    LANGUAGE_CODE = 'en'


ISO Language Code Table
-----------------------
http://www.lingoes.net/en/translator/langcode.htm

    uk  Ukrainian
    uk-UA   Ukrainian (Ukraine)

LANGUAGE_CODE setting:
----------------------

    LANGUAGES = (
    ('en', 'English'),
    ('uk', 'Ukrainian'),
    )


message file
------------
Файл сообщения является обычным текстовым файлом, представляющим единственный язык, который содержит все доступные строки перевода и правила их отображения для данного языка. Файлы сообщений имеют расширение .po.

translation string
-------------------
Строка, которая может быть переведена.

format file
-----------
Файл формата является модулем языка Python и определяет форматы данных для данной локали.

Django предоставляет утилиты для извлечения переводимых строк в файл сообщений. Этот файл является удобным средством, которое позволяет переводчикам делать свою работу. После того, как перевод строк этого файла завершён, файл должен быть скомпилирован. Этот процесс обеспечивает набор средств GNU gettext.

При наличии скомпилированного ресурса с переводом строк, Django обеспечивает автоматический перевод веб приложений для каждого доступного языка, в соответствии с языковыми настройками пользователя.

Механизм интернационализации Django включен по умолчанию, т.е. в определённых местах фреймворка всегда присутствует небольшая трата ресурсов на его работу. Если вы не используете интернационализацию, то вам следует потратить пару секунд на установку USE_I18N = False в файле конфигурации. Это позволит Django выполнять некоторую оптимизацию, не подгружая библиотеки интернационализации.

Есть также независимый, но связанный параметр USE_L10N, который управляет применением локального форматирования для данных.

Удостоверьтесь, что вы активировали механизм перевода для вашего проекта, для этого достаточно проверить наличие django.middleware.locale.LocaleMiddleware в параметре конфигурации MIDDLEWARE_CLASSES. 


        MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        # ...
        )

Как Django находит переводы
----------------------------
Во время своей работы Django создаёт в памяти унифицированный каталог с переводами. Для этого он использует следующий алгоритм, учитывая порядок нахождения путей для загрузки файлов сообщений (.mo) и приоритет множества перевода для одного слова:

Каталоги, указанные в LOCALE_PATHS, имеют повышенный приоритет, список представлен по убыванию приоритета.

        LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale/'),
        )

Затем происходит поиск каталога locale в каждом установленном приложении, указанном в INSTALLED_APPS. Тут тоже приоритет идёт по убыванию.

Наконец, используется базовый перевод Django из django/conf/locale.

Поиск переводов для JavaScript строк происходит аналогично, но с небольшими отличиями. 
Имя каталога, содержащего перевод, должно быть названо в соответствии соглашению по наименованию локалей. Т.е. en, uk и так далее.

        locale/
               en/
               uk/

Интернационализация в коде
==========================
Обычный перевод
---------------
Укажите переводимую строку с помощью функции ugettext(). Удобно импортировать её с помощью краткого псевдонима, _ (символ подчеркивания), чтобы сократить затраты на ввод.

Модуль gettext стандартной библиотеки языка Python определяет _() в качестве псевдонима для gettext() в глобальном пространстве имён.

Символ подчёркивания (_) используется в интерактивном интерпретаторе Python и в доктестах в качестве “результата предыдущей операции”. Определение глобальной функции _() приведёт к путанице. Явное импортирование ugettext() в виде _() решает эту проблему.

        # Internationalization
        # https://docs.djangoproject.com/en/1.9/topics/i18n/

        LANGUAGE_CODE = 'uk' # uk-UA   Ukrainian

        TIME_ZONE = 'UTC'

        USE_I18N = True

        USE_L10N = True

        USE_TZ = True

        from django.utils.translation import gettext_lazy as _

        # uk-UA   Ukrainian

        LANGUAGES = (
            ('en', _('English')),
            ('uk', _('Ukrainian')),
        )

./manage.py startapp pages

Для хранение древовидных структур в Django чаще всего используются внешние ключи к родителю, без каких либо дополнительных ухищрений. Все хорошо когда надо добавить новый элемент или удалить листовой элемент. Но все усложняется когда надо построить дерево для какого-то элемента или удалить элемент, у которого есть потомки, немаловажной остается проблема и сортировки.

Одним из вариантов решений является алгоритм MPTT(Modified Preorder Tree Traversal) или еще называемый Nested Sets, который облегчает процесс выборки, построение пути, подсчет потомков, но усложняет процесс добавления нового элемента в дерево или удаления существующего (приходится пересчитывать используемые маркеры для каждого элемента дерева).

В django для управления древовидными структурами существует два модуля django-mptt и django-treebeard.

Установка и настройка

Устанавливаем последнюю версию django-mptt

git clone git://github.com/brosner/django-mptt.git
cd django-mptt
python setup install 

django-mptt
-----------
https://github.com/django-mptt/django-mptt

    pip install django-mptt

serrings.py
-----------

    INSTALLED_APPS = [
        'grappelli',
        'filebrowser',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'mptt',
        'ckeditor',
        'ckeditor_uploader',
        'tinymce',
        'shop',
        'userprofiles',
        'bootstrap3',
        'reviews',
    ]


UUIDField
=========
    class UUIDField(**kwargs)
Стандартный виджет: TextInput

Пустое значение: '' (пустая строка).

Нормализует к: объекту UUID.
https://docs.python.org/3/library/uuid.html#uuid.UUID

Ключи сообщений об ошибках: required, invalid.

Это поле будет принимать любой строковый формат, понимаемый аргументом hex конструктора UUID.

AUTH_USER_MODEL
---------------
По умолчанию: ‘auth.User’

Модель пользователя.

Вы не можете изменить эту настройку в процессе разработки проекта (то есть после создания и миграции моделей, которые ссылаются на указанную модель). Предполагается, что эта настройка будет добавлена при создании проекта, и модель, на которую она указывает, будет доступна в первой миграции приложения.

pages/utils.py:

        # -*- coding: utf-8 -*-
        """A collection of functions for Page CMS"""

        from django.conf import settings as django_settings
        from django.utils import timezone

        from datetime import datetime


        def get_now():
            if django_settings.USE_TZ:
                return datetime.utcnow().replace(tzinfo=timezone.utc)
            else:
                return datetime.now()


pages/models.py:
-----------------
        # -*- coding:utf-8 -*-
        """Django page ``models``."""

        from django.db import models

        from django.utils.translation import ugettext_lazy as _
        from django.utils.encoding import python_2_unicode_compatible
        from django.conf import settings as django_settings
        from mptt.models import MPTTModel
        from .utils import get_now

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


Ленивый перевод
---------------
Используйте ленивые версии функций перевода из django.utils.translation (их легко опознать по суффиксу lazy в их именах) для отложенного перевода строк – перевод производится во время обращения к строке, а не когда вызывается функция.

Эти функции хранят ленивую ссылку на строку, не на её перевод. Сам перевод будет выполнен во время использования строки в строковом контексте, например, во время обработки шаблона.

Это полезно, когда функция перевода вызывается при загрузке модуля.

Такое может легко произойти во время определения моделей, форм или модельных форм, так как в Django их поля реализованы в виде атрибутов класса. По этой причине, надо использовать ленивый перевод в следующих случаях:

- Поля модели и связанные с ними значения атрибутов verbose_name и help_text

Например, для перевода подсказки для поля status name в модели:


        from django.utils.translation import ugettext_lazy as _

            status = models.IntegerField(_('status'), choices=STATUSES, default=DRAFT)


Вы можете перевести имена связей ForeignKey, ManyToManyField или OneToOneField с помощью их атрибута verbose_name:

            author = models.ForeignKey(django_settings.AUTH_USER_MODEL,
                    verbose_name=_('author'))

Значения для подписи модели
---------------------------
Рекомендуется всегда предоставлять явные значения для verbose_name и verbose_name_plural, а не надеяться на механизм их автоматического определения через имя класса:

    class Meta:
        """Make sure the default page ordering is correct."""
        ordering = ['tree_id', 'lft']
        get_latest_by = "publication_date"
        verbose_name = _('page')
        verbose_name_plural = _('pages')

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

Значения атрибута short_description у методов модели
----------------------------------------------------
Для методов модели вы можете с помощью атрибута short_description предоставить перевод для Django и интерфейса администратора:

    from . import settings

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

 

Локализация: как создать языковые файлы
========================================
После того, как текстовые ресурсы приложения были помечены для перевода, следует выполнить (или получить) сам перевод.

Файлы сообщений
----------------
Первым шагом будет создание файла сообщений для нового языка. Файл сообщений является простым текстовым файлом, предоставляющим один язык, который содержит все переводимые строки и правила их представления на этом языке. Файлы сообщений имеют расширение .po.

Django поставляется с утилитой, django-admin makemessages, которая автоматизирует создание и обновление этих файлов.

Утилиты Gettext
---------------
Команда makemessages использует команды из утилит набора GNU gettext: xgettext, msgfmt, msgmerge и msguniq.

Для создания или обновления файла сообщений запустите эту команду:

    django-admin makemessages -l uk

где uk является названием локали для создаваемого файла сообщений. 

Этот скрипт должен быть запущен из одного из двух мест:

- Корневой каталог вашего Django проекта (который содержит manage.py)
- Корневой каталог одного из приложений Django.

Скрипт просматривает дерево исходного кода вашего проекта или приложения и извлекает все строки, помеченные для перевода(смотрите Как Django находит переводы и убедитесь что LOCALE_PATHS настроен правильно). Затем скрипт создаёт (или обновляет) файл сообщений в каталоге locale/LANG/LC_MESSAGES. В случае примера с uk, файл будет создан в locale/uk/LC_MESSAGES/django.po.

При запуске makemessages из корневого каталога вашего проекта, извлечённые строки будут автоматически размещены в соответствующих файлах сообщений. Таким образом, строка, полученная из файла приложения, которое обладает каталогом locale, будет размещена в файле сообщений в этом каталоге. А строка, полученная из файла приложения, у которого нет каталога locale, будет размещена в файле сообщений в каталоге, который первым упомянут в LOCALE_PATHS или будет выведена ошибка если LOCALE_PATHS пуст.

По умолчанию, django-admin makemessages просматривает каждый файл с расширениями .html или .txt. Если вам надо изменить это поведение, используйте опцию --extension или -e для указания нужного расширения для просматриваемых файлов:

    django-admin makemessages -l uk -e txt

Разделяйте множество расширений с помощью запятой и/или используйте опцию многократно:

    django-admin makemessages -l uk -e html,txt -e xml

Если у вас не установлены утилиты gettext, тогда makemessages создаст пустые файлы. Если вы столкнулись с такой проблемой, тогда либо установите утилиты gettext, либо скопируйте файл сообщений для английского языка (locale/en/LC_MESSAGES/django.po), если он доступен, и используйте его как стартовую точку; это просто пустой файл переводов.

Формат .po файлов несложен. Каждый .po файл содержит небольшой заголовок, например, контактную информацию ответственного. Но основная часть файла является списком сообщений – простое сопоставление переводимых строк с переводами на конкретный язык.

.po файлы: Кодировка и использование BOM
----------------------------------------
Django поддерживает .po файлы только в кодировке UTF-8 и без меток BOM (Byte Order Mark). Если ваш редактор по умолчанию добавляет такие метки в начало файла, вам следует изменить это поведение.

gettext на Windows
==================

- Скачайте следующие архивы с серверов GNOME https://download.gnome.org/binaries/win32/dependencies/

    gettext-runtime-X.zip
    gettext-tools-X.zip

X является версией, мы требуем версию 0.15 или выше.

- Извлеките содержимое каталогов bin\ обоих архивов в такой же каталог на вашей системе (т.е. C:\Program Files\gettext-utils).

- Обновите системный PATH:

    Control Panel > System > Advanced > Environment Variables.

В списке System variables, выберите Path, затем Edit.

- Добавьте 
    ;C:\Program Files\gettext-utils\bin в конец поля Variable value.

Вы также можете использовать бинарники gettext, взятые где-то, если команда xgettext --version работает правильно. Не пытайтесь выполнять команды Django, использующие пакет gettext, если команда xgettext --version, введённая в консоли Windows, выбрасывает окно с текстом “xgettext.exe has generated errors and will be closed by Windows”.

Настройка команды makemessages
------------------------------
Если вам требуется передать дополнительные параметры в xgettext, вам следует создать свою команду makemessages и переопределить её атрибут xgettext_options:

    from django.core.management.commands import makemessages

    class Command(makemessages.Command):
        xgettext_options = makemessages.Command.xgettext_options + ['--keyword=mytrans']


Все репозитории с файлами сообщений имеют одинаковую структуру:
---------------------------------------------------------------
Во всех указанных путях в параметре конфигурации LOCALE_PATHS происходит поиск 

    <language>/LC_MESSAGES/django.(po|mo)

    $APPPATH/locale/<language>/LC_MESSAGES/django.(po|mo)
    $PYTHONPATH/django/conf/locale/<language>/LC_MESSAGES/django.(po|mo)


Для создания файлов сообщений надо использовать django-admin makemessages. 
--------------------------------------------------------------------------

    ./manage.py makemessages --all

    processing locale en
    processing locale uk

    en/
    LC_MESSAGES/
    django.po

    uk/
    LC_MESSAGES/
    django.po



uk/LC_MESSAGES/django.po:
--------------------------
        # SOME DESCRIPTIVE TITLE.
        # Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
        # This file is distributed under the same license as the PACKAGE package.
        # FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
        #
        #, fuzzy
        msgid ""
        msgstr ""
        "Project-Id-Version: PACKAGE VERSION\n"
        "Report-Msgid-Bugs-To: \n"
        "POT-Creation-Date: 2016-04-28 11:44+0000\n"
        "PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
        "Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
        "Language-Team: LANGUAGE <LL@li.org>\n"
        "Language: \n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n"
        "%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"

        #: mysite/settings.py:139
        msgid "Ukrainian"
        msgstr ""

        #: mysite/settings.py:140
        msgid "English"
        msgstr ""

        #: pages/models.py:22
        msgid "Published"
        msgstr ""

        #: pages/models.py:23
        msgid "Hidden"
        msgstr ""

        #: pages/models.py:24
        msgid "Draft"
        msgstr ""

        #: pages/models.py:31
        msgid "author"
        msgstr ""

        #: pages/models.py:34
        msgid "parent"
        msgstr ""

        #: pages/models.py:35
        msgid "creation date"
        msgstr ""

        #: pages/models.py:37
        msgid "publication date"
        msgstr ""

        #: pages/models.py:38
        msgid ""
        "When the page should go\n"
        "            live. Status must be \"Published\" for page to go live."
        msgstr ""

        #: pages/models.py:40
        msgid "publication end date"
        msgstr ""

        #: pages/models.py:41
        msgid ""
        "When to expire the page.\n"
        "            Leave empty to never expire."
        msgstr ""

        #: pages/models.py:44
        msgid "last modification date"
        msgstr ""

        #: pages/models.py:46
        msgid "status"
        msgstr ""

        #: pages/models.py:47
        msgid "template"
        msgstr ""

        #: pages/models.py:50
        msgid "delegate to"
        msgstr ""

        #: pages/models.py:53
        msgid "freeze date"
        msgstr ""

        #: pages/models.py:54
        msgid ""
        "Don't publish any content\n"
        "            after this date."
        msgstr ""

        #: pages/models.py:71
        msgid "page"
        msgstr ""

        #: pages/models.py:72
        msgid "pages"
        msgstr ""

        #: pages/models.py:98
        msgid ""
        "Get the calculated status of the page based on :attr: Page."
        "publication_date, :attr: Page.publication_end_date and :attr: Page.status"
        msgstr ""

перевод
-------
- msgid является переводимой строкой, которая определена в исходном коде. Не изменяйте её.

- msgstr является местом, где вы пишите свой перевод. Обычно оно пустое, именно вы отвечаете за его наполнение. Удостоверьтесь, что вы сохранили кавычки вокруг перевода.


    #: mysite/settings.py:139
    msgid "English"
    msgstr "Англійська"

    #: mysite/settings.py:140
    msgid "Ukrainian"
    msgstr "Українська"


Для удобства, каждое сообщение включает, в виде закомментированной строки, размещенной выше строки msgid, имя файла и номер строки из которой была получена переводимая строка.

Укажите свою кодировку
----------------------
Из-за особенностей внутренней работы утилит пакета gettext и нашего желания позволить использование не-ASCII символов в строках кода Django и ваших приложений, вы должны использовать UTF-8 в качестве кодировки ваших PO файлов (по умолчанию при их создании). Это означает, что все будут использовать одинаковую кодировку, что очень важно в момент, когда Django обрабатывает PO файлы.
Для повторного прохода по всему исходному коду и шаблонам в поисках новых переводимых строк и для обновления всех файлов с сообщениями для всех языков, выполните это:

    django-admin makemessages -a


Комментарии для переводчиков
-----------------------------
Если необходимо дать переводчикам подсказку по переводимой строке, вы можете добавить комментарий с префиксом Translators в строке предшествующей переводимой, например:

    def my_view(request):
        # Translators: This message appears on the home page only
        output = ugettext("Welcome to my site.")

Комментарий появится в результирующем .po файле, который связан с переводимой конструкцией расположенной далее, и должен быть отображён большинством средств перевода.

Для полноты изложения приведём соответствующий фрагмент .po файла:

    #. Translators: This message appears on the home page only
    # path/to/python/file.py:123
    msgid "Welcome to my site."
    msgstr ""

Пометка строк как no-op
------------------------
Используйте функцию django.utils.translation.ugettext_noop() для пометки строки как переводимой, но не переводя её. Такая строка будет переведена позже с помощью переменной.

Компиляция файлов с сообщениями
===============================
После того, как вы создали файл с сообщениями, а также после каждого его обновления, вам следует скомпилировать этот файл, чтобы позволить gettext его использовать. Сделайте это с помощью утилиты django-admin compilemessages.

Эта команда обрабатывает все имеющиеся .po файлы и создаёт на их основе .mo файлы, которые являются бинарными файлами, оптимизированными для использования gettext. Запускать django-admin compilemessages надо в том же каталоге, что и django-admin makemessages, вот так:

    django-admin compilemessages

Ваш перевод готов к использованию.

django-admin compilemessages
-----------------------------
Для компиляции файлов перевода надо использовать django-admin compilemessages, это приведёт к созданию бинарных .mo файлов, которые нужны для работы gettext.

django-admin compilemessages --settings=path.to.settings


    ./manage.py compilemessages
    processing file django.po in /home/janus/github/tdd-django/mysite/locale/en/LC_MESSAGES
    processing file django.po in /home/janus/github/tdd-django/mysite/locale/uk/LC_MESSAGES

    en/
    LC_MESSAGES/
    django.mo
    django.po

    uk/
    LC_MESSAGES/
    django.mo
    django.po


Измените urls.py
================
Для поддержки нескольких языков в URL нужно использовать i18n_patterns вместо patterns в urls.py

        from django.conf.urls.i18n import i18n_patterns

        urlpatterns += i18n_patterns(
            url(r'^admin/filebrowser/', include(site.urls)),
            url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
            url(r'^admin/', admin.site.urls),
        )


