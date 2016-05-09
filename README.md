# tdd-django unit_15

Своя CMS
========

layouts.py
----------

# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Template(models.Model):
    """
    Stores template information.
    Template name is used for template selection in templates foled of your project
    """
    template = models.CharField(_('Template name'), max_length=200)
    submenu_max_characters = models.PositiveIntegerField(_('Max characters in submenu'), default=150)
    active = models.BooleanField(_('Active'), default=False, blank=True)

    def __syr__(self):
        return self.template

    def save(self, *args, **kwargs):
        if not self.active:
            if not Template.objects.exists():
                self.active = True

        else:
            others = Template.objects.filter(active=True).exclude(id=self.id)

            for other_active in others:
                other_active.active = False
                super(Template, other_active).save(*args, **kwargs)

            self.active = True

        super(Template, self).save(*args, **kwargs)

    class Meta:
        
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

pages/models.py
---------------
from .layouts.models import *

admin.py
--------
# -*- encoding: utf-8 -*-

from django.contrib import admin

from ..common.admin_actions import activate, deactivate
from .models import *

class LayoutsAdmin(admin.ModelAdmin):

    fields = ('template', 'submenu_max_characters', 'active')
    list_display = fields
    actions = [activate, deactivate]

admin.site.register(Template, LayoutsAdmin)

pages/admin.py
--------------
from pages.layouts.admin import *

Dashboard
---------

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.ModelList(
                _('General'),
                column=1,
                collapsible=True,
                models=(
                    
                    'pages.language.models.*',
                    'pages.layouts.models.*',
                    
                ),
            )
        )

site/models.py
--------------
# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Site(models.Model):
    """
    Model for site settings
    there is supposed to by only one Site
    (for now)
    """
    domain = models.CharField(_('Domain'), max_length=150)
    display_name = models.CharField(_('Website name'), max_length=200)
    tagline = models.CharField(
        _('Tagline'),
        help_text=_('Smaller text next to website name'),
        max_length=200,
        blank=True
    )
    footer = models.TextField(
        _('Footer'),
        help_text=_('Custom footer with HTML to be displayed on each page'),
        max_length=1000,
        blank=True
    )

    def __str__(self):
        return self.domain

    class Meta:
        
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')


class Script(models.Model):
    """
    Model for scripts that should
    be inserted on each page (like footer above)

    for example google analytics/facebook/google+ ..
    """
    name = models.CharField(
        _('Name'),
        help_text=_('Script identification'),
        max_length=50
    )
    code = models.TextField(
        _('Code'),
        help_text=_('Source code for script to be inserted, including &lt;script&gt;&lt;/script&gt; tags'),
        max_length=1000
    )

    class Meta:
        
        verbose_name = _('Script')
        verbose_name_plural = _('Scripts')

admin.py
--------

# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

class SiteAdmin(admin.ModelAdmin):
    list_display = ('domain', 'display_name', 'tagline')

class ScriptAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

admin.site.register(Site,SiteAdmin)
admin.site.register(Script,ScriptAdmin)

Dashboard
---------
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

                    'pages.layouts.models.*',
                    'pages.site.models.*',
                ),
            )
        )


menu/models.py
--------------

# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from ..language.models import Language

@python_2_unicode_compatible
class Menu(models.Model):
    """
    Stores data about menu.
    There may be reason to have multiple menu
    Links in the header for example
    """
    name = models.CharField(
        _('Menu name'),
        help_text=_('For identification only'),
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')

@python_2_unicode_compatible
class MenuItem(models.Model):
    """
    Stores menuitem information.
    It is recommended to write urls in SEO format,
    e.g.: this_is_my_site_describing_something.
    Is related to :model: `pages.Menu`.
    """
    lang = models.ForeignKey(Language, verbose_name=_('Language'))
    menu = models.ForeignKey(Menu, verbose_name=_('Menu'))
    menuitem_name = models.CharField(_('Menu item name'), max_length=200)
    url = models.CharField(
        _('Url'),
        help_text=_('It is recommended to write urls in SEO format, '
                    'e.g.: this_is_my_site_describing_something.'),
        max_length=200
    )
    position = models.IntegerField(_('Position'), blank=True)
    style = models.CharField(
        _('Style'),
        help_text=_('Custom style for this menu item'),
        max_length=200,
        blank=True
    )

    def __str__(self):
        return '%s - %s' % (self.menuitem_name, self.lang)

    def save(self, *args, **kwargs):
        """
        if MenuItem does not contain position,
        set it to last_item's_position + 1
        """
        if not self.position:

            last_position = self.get_last_position()
            self.position = last_position + 1

        super(MenuItem, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        makes sure that there is no spaces in positioning after delete
        """
        super(MenuItem, self).delete(*args, **kwargs)
        self.reorder_items()

    def reorder_items(self):
        """
        repositions items after deletion or exception
        """
        items = MenuItem.objects.filter(
            lang=self.lang,
            menu=self.menu
        ).order_by('position')

        for pos, item in enumerate(items):
            item.position = pos + 1
            item.save()

    def get_last_position(self):
        """
        returns last_item's_position or 0 (no items)
        """
        other_objects = MenuItem.objects.filter(
            lang=self.lang,
            menu=self.menu
        ).order_by('-position')

        if other_objects.count():
            last_position = other_objects[0].position

        else:
            last_position = 0

        return last_position

    def is_first(self):
        """
        returns True if self.position is 1, False otherwise
        """
        if self.position == 1:
            return True

        return False

    def is_last(self):
        """
        if self.position is last, return True, False otherwise

        @return bool
        """
        last_position = self.get_last_position()

        if self.position == last_position:
            return True

        return False

    def increase_position(self):
        """
        moves this item to self.position + 1
        """
        if self.is_last():
            pass

        else:
            self.swap_with(self.position + 1)

    def decrease_position(self):
        """
        moves this item to self.position - 1
        """
        if self.is_first():
            pass

        else:
            self.swap_with(self.position - 1)

    def swap_with(self, position):
        """
        handles item moving, makes sure there are no items with same position
        """
        try:
            object_to_swap_with = MenuItem.objects.get(
                lang=self.lang,
                menu=self.menu,
                position=position
            )

            object_to_swap_with.position = self.position
            object_to_swap_with.save()

            self.position = position
            self.save()

        except MenuItem.DoesNotExist:
            self.reorder_items()

    def is_current(self, page_url):
        """
        checks if this is currently active menuitem

        @return bool
        """
        if page_url == self.url or (
            self.page.index and self.page.active and page_url is None
        ):

            return True

        return False

    def get_url(self):
        """
        returns url for django-page or http link
        if 'http://' is in self.url or 'https://'
        """
        if 'http://' in self.url or 'https://' in self.url:
            return self.url

        else:
            return '/{}/{}'.format(self.lang.country_code, self.url)

    class Meta:

        verbose_name = _('Menu item')
        verbose_name_plural = _('Menu items')

pages/models.py
----------------
from .menu.models import *

./manage.py makemigrations page
./manage.py mograte

menu/admin.py
-------------

# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *

admin.site.register(Menu)
admin.site.register(MenuItem)

pages/admin.py
---------------

from pages.menu.admin import *


Dashboard
----------
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
                    'pages.menu.models.*',
                    'pages.layouts.models.*',
                    'pages.site.models.*',
                ),
            )
        )


Форматирование строк. Оператор %
================================

Иногда возникают ситуации, когда нужно сделать строку, подставив в неё некоторые данные, полученные в процессе выполнения программы (пользовательский ввод, данные из файлов и т. д.). Подстановку данных можно сделать с помощью форматирования строк. Форматирование можно сделать с помощью оператора %, и метода format.

Метод format является наиболее правильным, но часто можно встретить программный код с форматированием строк в форме оператора %.
Форматирование строк с помощью оператора %
------------------------------------------
Если для подстановки требуется только один аргумент, то значение - сам аргумент:

        >>> 'Hello, %s!' % 'Vasya'
        'Hello, Vasya!'

А если несколько, то значением будет являться кортеж со строками подстановки:

        >>> '%d %s, %d %s' % (6, 'bananas', 10, 'lemons')
        '6 bananas, 10 lemons'

Формат  
------
        '%d', '%i', '%u'    Десятичное число.
        '%o'    Число в восьмеричной системе счисления.
        '%x'    Число в шестнадцатеричной системе счисления (буквы в нижнем регистре).
        '%X'    Число в шестнадцатеричной системе счисления (буквы в верхнем регистре).
        '%e'    Число с плавающей точкой с экспонентой (экспонента в нижнем регистре).
        '%E'    Число с плавающей точкой с экспонентой (экспонента в верхнем регистре).
        '%f', '%F'  Число с плавающей точкой (обычный формат).
        '%g'    Число с плавающей точкой. с экспонентой (экспонента в нижнем регистре), если она меньше, чем -4 или точности, иначе обычный формат.
        '%G'    Число с плавающей точкой. с экспонентой (экспонента в верхнем регистре), если она меньше, чем -4 или точности, иначе обычный формат.
        '%c'    Символ (строка из одного символа или число - код символа).
        '%r'    Строка (литерал python).
        '%s'    Строка (как обычно воспринимается пользователем).
        '%%'    Знак '%'.

Спецификаторы преобразования:
-----------------------------
    %.
    Ключ (опционально), определяет, какой аргумент из значения будет подставляться.
    Флаги преобразования.
    Минимальная ширина поля. Если *, значение берётся из кортежа.
    Точность, начинается с '.', затем - желаемая точность.
    Модификатор длины (опционально).
    Тип (см. таблицу выше).


     print ('%(language)s has %(number)03d quote types.' % {"language": "Python", "number": 2})

Флаги преобразования:

        "#" Значение будет использовать альтернативную форму.
        "0" Свободное место будет заполнено нулями.
        "-" Свободное место будет заполнено пробелами справа.
        " " Свободное место будет заполнено пробелами справа.
        "+" Свободное место будет заполнено пробелами слева.


    def move(self, obj):
        """
        Returns html with links to move_up and move_down views.
        """
        button = u'<a href="%s"><img src="%simg/arrow-%s.png" /> %s</a>'
        prefix = ADMIN_MEDIA_PREFIX

        link = '%d/move_up/' % obj.pk
        html = button % (link, prefix, 'up', _('up')) + " | "
        link = '%d/move_down/' % obj.pk
        html += button % (link, prefix, 'down', _('down'))

        return html


django.utils.html
=================

escape(text)

    Возвращает заданный текст с амперсандом, кавычками и угловыми скобками, закодированные для использования в HTML. Ввод сначала пропускают через force_text(), а к выходному сигналу применяется mark_safe().

conditional_escape(text)

    Подобно escape(), за исключением того, что он не работает с заранее маскироваными строками.

format_html(format_string, *args, **kwargs)

    Похоже на str.format, за исключением того, что он подходит для создания фрагментов HTML. Все args и kwargs пропускают через conditional_escape() перед подачей на str.format.

     Для случая построения небольших фрагментов HTML, эта функция предпочтительнее интерполяции строк, где % или str.format используется непосредственно.

    Таким образом, вместо написания:

    mark_safe("%s <b>%s</b> %s" % (some_html,
                                    escape(some_text),
                                    escape(some_other_text),
                                    ))

    Используйте:

    format_html("{} <b>{}</b> {}",
                mark_safe(some_html), some_text, some_other_text)

    Преимущество в том, что вам не нужно применять escape() для каждого аргумента рискуя ошибиться и получить уязвимость XSS.

format_html_join(sep, format_string, args_generator)

    Оболочка format_html(), для группы аргументов, которые должны быть отформатированы с использованием той же строки формата, а затем объединяются при помощи sep. sep также проходит через conditional_escape().

    args_generator должен быть итератор, который возвращает последовательность аргументов, которые будут переданы в format_html().

    format_html_join('\n', "<li>{} {}</li>", ((u.first_name, u.last_name)
                                                for u in users))

strip_tags(value)

    Пытается удалить что-нибудь, что выглядит как HTML-тег из строки.

    Абсолютно никакой гарантии не предусмотрено о результирующей строке будучи HTML безопасным. Так что никогда не маркировать безопасному хранению результат strip_tag вызова без возможности избежать этого во-первых, например, с помощью побега ().

    Например:

    value = "<b>Joel</b> <button>is</button> a <span>slug</span>"
    strip_tags(value)

    Вернет "Joel is a slug".

html_safe()
    
    Метод __html __ () класса помогает без шаблонизатора обнаружить классы, чьи выводы не требуют HTML эскейпмнга.


from django.utils.html import format_html

    def move(self, obj):
        """
        Returns html with links to move_up and move_down views.
        """
        button = u'<a href="%s"><img src="%simg/arrow-%s.png" /> %s</a>'
        prefix = ADMIN_MEDIA_PREFIX

        link = '%d/move_up/' % obj.pk
        html = button % (link, prefix, 'up', _('up')) + " | "
        link = '%d/move_down/' % obj.pk
        html += button % (link, prefix, 'down', _('down'))

        return format_html(html)

Исключения Django
=================
Django вызывает несколько собственных исключений на ряду со стандартными исключениями Python.

Основные исключения Django
--------------------------
Основные исключения Django определены в django.core.exceptions.

ObjectDoesNotExist
------------------
exception ObjectDoesNotExist

    Основной класс DoesNotExist. try/except для ObjectDoesNotExist словит исключения DoesNotExist для всех моделей.

FieldDoesNotExist
-----------------
exception FieldDoesNotExist

    Исключение FieldDoesNotExist вызывается методом _meta.get_field() модели, если запрошенное поле не найдено в модели или в предках модели.
    
MultipleObjectsReturned
-----------------------
exception MultipleObjectsReturned

    Исключение MultipleObjectsReturned вызывается запросом при получении нескольких объектов в случае, когда ожидался один объект. Базовая версия этого исключения предоставляется модулем django.core.exceptions; каждый класс модели содержит версию подкласса, которая может использоваться для идентификации особого объектного типа, который возвратил коллекцию объектов.
    
SuspiciousOperation
-------------------
exception SuspiciousOperation

    Исключение SuspiciousOperation вызывается когда пользователь выполнил операцию, которая должна быть рассмотрена как подозрительная с точки зрения безопасности, например, при подмене куки сессии. Подклассы SuspiciousOperation:

        DisallowedHost
        DisallowedModelAdminLookup
        DisallowedModelAdminToField
        DisallowedRedirect
        InvalidSessionKey
        SuspiciousFileOperation
        SuspiciousMultipartForm
        SuspiciousSession

    Исключение SuspiciousOperation на уровне WSGI обработчика будет логгировано как ошибка и будет возвращен HttpResponseBadRequest. Подробности смотрите в разделе о логгировании.

PermissionDenied
----------------
exception PermissionDenied

    Исключение PermissionDenied вызывается если пользователь не имеет права на выполнение запрошенного действия.PermissionDenied

ViewDoesNotExist
----------------
exception ViewDoesNotExist

    Исключение ViewDoesNotExist вызывается модулем django.core.urlresolvers, если запрошенное представление на найдено.

MiddlewareNotUsed
-----------------
exception MiddlewareNotUsed

    Исключение MiddlewareNotUsed вызывается, если мидлвар не используется в конфигурации сервера.

ImproperlyConfigured
--------------------
exception ImproperlyConfigured

    Исключение ImproperlyConfigured вызывается, если Django неправильно сконфигурировано. Например, если значение в settings.py неправильное.

FieldError
-----------
exception FieldError

    Исключение FieldError вызывается, если существует проблема с полем модели. Такое может произойти по следующим причинам:

        Поле в модели конфликтует с полем абстрактного класса, которое имеет такое же имя.

        Бесконечный цикл, вызванный сортировкой.

        Аргумент не может быть получен из параметров фильтра.

        Поле не может быть определено из аргумента в параметрах запроса.

        Объединение не разрешено для указанного поля.

        Имя поля неверное.

        Запрос состоит из неверного порядка аргументов.

ValidationError
---------------
exception ValidationError

    Исключение ValidationError вызывается, если происходит ошибка проверки данных от формы или модели. 

        NON_FIELD_ERRORS

        NON_FIELD_ERRORS

ValidationError, которые не относятся ни к одному из полей формы или модели, классифицируются как NON_FIELD_ERRORS. Эта константа определяет ключ в словаре ошибок.

Ошибки определения URL
----------------------
Ошибки определения URL определены в django.core.urlresolvers.
Resolver404
-----------
exception Resolver404

    Исключение Resolver404 вызывается в django.core.urlresolvers.resolve(), если путь переданный в resolve() не соответствует ни одному представлению. Подкласс django.http.Http404.

NoReverseMatch
--------------
exception NoReverseMatch

    Исключение NoReverseMatch вызывается модулем django.core.urlresolvers, если не получилось найти соответствующий URL по переданным параметрам.

Исключения базы данных
-----------------------
Ошибки базы данных определены в django.db.

Django оборачивает стандартные исключения базы данных таким образом, что код Django гарантирует стандартную реализацию этих классов.

        exception Error

        exception InterfaceError

        exception DatabaseError

        exception DataError

        exception OperationalError

        exception IntegrityError

        exception InternalError

        exception ProgrammingError

        exception NotSupportedError

Обёртка Django для исключений базы данных ведёт себя аналогично обёртываемым исключениям. 

В соответствии с PEP 3134, атрибут __cause__ содержит изначальное исключение базы данных, предоставляя доступ к дополнительной информации. (Этот атрибут доступен для Python 2 и Python 3, хотя PEP 3134 создавался для Python 3.)

exception models.ProtectedError
-------------------------------
Выбрасывается для предотвращения удаления связанных объектов при использовании django.db.models.PROTECT. models.ProtectedError`является дочерним классом :exc:`IntegrityError.
Исключения Http
---------------
Ошибки HTTP определенны в django.http.
UnreadablePostError
-------------------
exception UnreadablePostError

    Исключение UnreadablePostError выбрасывается когда пользователь прерывает закачку файла.

Исключения транзакций
---------------------
Ошибки транзакции определены в django.db.transaction.
TransactionManagementError
--------------------------
exception TransactionManagementError

    Исключение TransactionManagementError вызывается для всех проблем с транзакциями в базе данных.

Исключения, используемые в тестах
---------------------------------
Ошибки HTTP определенны в django.test.
RedirectCycleError
------------------
exception client.RedirectCycleError
    
    Исключение RedirectCycleError вызывается, если тестовый клиент определил циклическое перенаправление или очень длинную цепочку перенаправлений.

Исключения Python
-----------------
Django вызывает встроенные исключения Python когда это требуется.

Интерфейс администратора Django
-------------------------------
Интерфейс администратора по умолчанию включен, если вы создавали проект командой startproject.

Объект ModelAdmin
-----------------
class ModelAdmin

    Класс ModelAdmin – это отображение модели в интерфейсе администратора. Его код добавляют обычно в файл admin.py вашего приложения.

ModelAdmin.has_change_permission(request, obj=None)
---------------------------------------------------
Должен возвращать True, если пользователю позволено изменять объект, иначе False. Если obj равен None, должен вернуть True или False, указывая может ли пользователь изменить какой-либо объект данного типа.

    def move_up(self, request, item_pk):
        if self.has_change_permission(request):
            item = get_object_or_404(MenuItem, pk=item_pk)
            item.increase_position()

        else:
            raise PermissionDenied

        
        return redirect('/admin/pages/menuitem')

    def move_down(self, request, item_pk):
        if self.has_change_permission(request):
            item = get_object_or_404(MenuItem, pk=item_pk)
            item.decrease_position()

        else:
            raise PermissionDenied
