# tdd-django unit_19

Class Based Views - Django
==========================

Gallery
=======
    
    manage.py startapp gallery

models.py
---------

        from django.db import models
        from django.core.urlresolvers import reverse

        from .fields import ThumbnailImageField

        class Item(models.Model):
            name = models.CharField(max_length=250)
            description = models.TextField()

            class Meta:
                ordering = ['name']

            def __str__(self):
                return self.name

            def get_absolute_url(self):
                return reverse('gallery:item_object', args=[str(self.id)])

        class Photo(models.Model):
            item = models.ForeignKey(Item)
            title = models.CharField(max_length=100)
            image = ThumbnailImageField(upload_to='photos')
            caption = models.CharField(max_length=250, blank=True)

            class Meta:
                ordering = ['title']

            def __str__(self):
                return self.title

            def get_absolute_url(self):
                return reverse('gallery:photo_object', args=[str(self.id)])

fields.py
---------

        from django.db.models.fields.files import ImageField, ImageFieldFile
        from PIL import Image
        import os

        def _add_thumb(s):
            """
            Changes the string which contains file name
            by inserting '.thumb' before file extension (which changes to .jpg)
            """
            parts = s.split('.')
            parts.insert(-1, 'thumb')
            if parts[-1].lower() not in ['jpeg', 'jpg']:
                parts[-1] = 'jpg'
            return '.'.join(parts)

        class ThumbnailImageFieldFile(ImageFieldFile):
            def _get_thumb_path(self):
                return _add_thumb(self.path)
            thumb_path = property(_get_thumb_path)

            def _get_thumb_url(self):
                return _add_thumb(self.url)
            thumb_url = property(_get_thumb_url)

            def save(self, name, content, save=True):
                super(ThumbnailImageFieldFile, self).save(name, content, save)
                img = Image.open(self.path)
                img.thumbnail(
                    (self.field.thumb_width, self.field.thumb_height),
                    Image.ANTIALIAS
                )
                img.save(self.thumb_path, 'JPEG')

            def delete(self, save=True):
                if os.path.exists(self.thumb_path):
                    os.remove(self.thumb_path)
                super(ThumbnailImageFieldFile, self).delete(save)

        class ThumbnailImageField(ImageField):
            """
            This field has the same behaviour as ImageField, 
            but additionally saves thumbnail of a picture
            """
            attr_class = ThumbnailImageFieldFile

            def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
                self.thumb_width = thumb_width
                self.thumb_height = thumb_height
                super(ThumbnailImageField, self).__init__(*args, **kwargs)

settings.py
-----------

        PROJECT_APPS = (

            'gallery',
        )


        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


Migrations
-------------

    manage.py migrate


admin.py
---------
        from django.contrib import admin
        from .models import Item, Photo

        class PhotoInline(admin.StackedInline):
            model = Photo

        class ItemAdmin(admin.ModelAdmin):
            inlines = [PhotoInline]

        admin.site.register(Item, ItemAdmin)
        admin.site.register(Photo)

dashboard.py
------------

        self.children.append(
            modules.ModelList(
                _('Gallery'),
                column=2,
                collapsible=True,
                models=('gallery.models.*', )
            )
        )


Общие представления и отображение объектов
===========================================

Django предлагает полезный и удобный набор встроенных общих представлений-классов, который позволяют отображать список объектов или конкретный объект.


TemplateView
============
Самый простой класс. Существует, чтобы просто отрендерить шаблон. 

Иногда нужно сделать для проекта статическую страницу, что-то вроде "Об авторе" или "О компании". Там просто нужно вывести определенную информацию, которая в дальнейшем редко будет меняться или совсем не будет. Создавать отдельное приложение не имеет смысла и забивать в базу всю информацию - тоже. 

Пишем в urls.py:

        from django.conf.urls import patterns, url
        from django.views.generic import TemplateView
        urlpatterns = paterns('',
            ...
            url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
            ...
        )

просто пишем шаблон about.html и вставляем туда любую статическую информацию


template_name 
-------------
В нем хранится имя шаблона, который нужно отрендерить. Для класса TemplateView этот параметр обязательный, другие классы имеют механизм автоматического формирования имени шаблона.

Для примера, можно создать дочерний класс и определить шаблон в нем:

        # views.py
        from django.views.generic import TemplateView

        class AboutView(TemplateView):
        template_name = 'about.html'

        # urls.py
        from app.views import AboutView
        ...
        url(r'^about/', AboutView.as_view(), name='about'),


И более сложный вариант дочернего класса. Представление при вызове as_view() принимает в себя параметры запроса в свойство request, и мы этим можем воспользоваться.


        # views.py
        from django.views.generic import TemplateView

        class AboutView(TemplateView):
        get_template_names(self): # именно names, не name
        if self.request.META['OS'] == 'Windows_NT':
        return 'about_win.html'
        else:
        return 'about.html'


views.py
--------
        from django.views.generic import TemplateView
        from .models import Item, Photo

        class IndexPageView(TemplateView):

            template_name = "gallery/index.html"

            def get_context_data(self, **kwargs):
                context = super(IndexPageView, self).get_context_data(**kwargs)
                context['item_list'] = Item.objects.all()[:3]
                return context
urls.py
-------

        from django.conf.urls import patterns, include, url
        from items.views import IndexPageView

        urlpatterns = patterns('',
            url(r'^$', IndexPageView.as_view(), name="index"),
        )

index.html:
------------
        {% extends "base.html" %}

        {% block title %}Home{% endblock %}
        {% block content %}
        <h2>Welcome to the Gallery!</h2>
        <p>Here you find pictures of various items.</p>
        <h3>Showcase</h3>
        <table>
            <tr>
                {% for item in item_list|slice:":3" %}
                    <td>
                        <a href="{{ item.get_absolute_url }}"><b>{{ item.name }}</b><br />
                        {% if item.photo_set.count %}
                            <img src="{{ item.photo_set.all.0.image.thumb_url }}" />
                        {% else %}
                            <span>No photos (yet)</span>
                        {% endif %}
                        </a>
                    </td>
                {% endfor %}
            </tr>
        </table>
        <p><a href="{% url 'item_list' %}">View the full list &raquo;</a></p>
        {% endblock %}

ListView
========

существует для отображения списка той или иной модели

В минимальном варианте достаточно указать класс в параметре model, по которому строить список, и создать шаблон. Если не указывать имя шаблона, то оно будет формироваться по следующему алгоритму: <имя_приложения>/<имя_модели>_list.html. В нашем случае это будет galery/item_list.html.
Сформированный список по умолчанию попадает в шаблон как параметр object_list.


CBV позволяет нам использовать особенности объектно-ориентированного программирования при разработке наших отображений. Теперь мы можем реализовывать базовые классы, несущие определенную функциональность и использовать их как примеси (mixins) для наших отображений.

    from django.views.generic import ListView


получение списка объектов или индивидуального объекта
------------------------------------------------------

определить представление:
-------------------------

### views.py

        from django.views.generic import ListView

        class ItemsListView(ListView):

            template_name = "gallery/items_listing.html"
            model = Item


привяжем представление к url:
------------------------------
### urls.py

        from django.conf.urls import patterns, include, url
        from .views import ItemsListView

        urlpatterns = patterns('',
            url(r'^$', ItemsListView.as_view(), name="item_list"),
         
        )

Мы можем явно указать в представлении, какой шаблон мы хотим использовать. Для этого мы должны добавить в представление атрибут template_name, с указанием имени шаблона. Если явно не указывать этот атрибут, Django “вычислит” его из названия объекта. В данном случае, таким “вычисленным” шаблоном будет "photo/album_list.html" – часть “photo” берется из имени приложения, определяющего модель, а часть “album” - это просто название модели в нижнем регистре.

Таким образом, если в настройках TEMPLATE_LOADERS “включен” класс загрузчика django.template.loaders.app_directories.Loader, то путь к шаблону будет следующим : /path/to/project/templates/gallery/items_listing.html

При обработке шаблона (рэндеринге), будет использоваться контекст, содержащий переменную album_list. Это переменная хранит список всех объектов (album). 

шаблон gallery/items_listing.html:
----------------------------------

            {% extends "base.html" %}

            {% block title %}Item List{% endblock %}

            {% block content %}
            <p><a href="{% url 'gallery:item_list' %}">&laquo; Back to main page</a></p>

            <h2>Items</h2>
            {% if object_list %}
            <table>
                <tr>
                    <th>Name</th>
                    <th>Sample Thumb</th>
                    <th>Description</th>
                </tr>
                {% for item in object_list %}
                <tr>
                    <td><i>{{ item.name }}</i></td>
                    <td>
                        {% if item.photo_set.count %}
                        <a href="{{ item.get_absolute_url }}">
                            <img src="{{ item.photo_set.all.0.image.thumb_url }}" />
                        </a>
                        {% else %}
                        (No photos currently uploaded)
                        {% endif %}
                    </td>
                    <td>{{ item.description }}</td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <p>There are currently no items to display.</p>
            {% endif %}
            {% endblock %}

Это действительно все, что нужно сделать. Все крутые “фичи” общих представлений-классов можно получить лишь устанавливая значения определенных атрибутов в представлении. 

Создание “дружелюбного” контента для шаблона
--------------------------------------------
Если вы оперируете запросом(queryset) или объектом, Django способно добавить в контекст переменную с именем модели в нижнем регистре. Эта переменная предоставляется в дополнение к стандартному значению object_list, и содержит то же самое значение, н-р, album_list.

Если этот вариант вас не устраивает, то имя переменной контекста можно задать вручную. Для этой цели служит атрибут context_object_name, который определяет имя переменной в контексте:

# views.py

        class ItemsListView(ListView):

            model = Item
            context_object_name = 'my_favourite_albums'


Добавление дополнительного контента
------------------------------------
Часто возникает потребность передать в контекст некоторые дополнительные данные, помимо тех, что автоматически предоставляются представлением. Представление-класс DetailView предоставляет нам только переменную контекста, содержащую данные об album, но как нам передать дополнительную информацию в шаблон?

Вы можете создать подкласс от DetailView и переопределить в нем метод get_context_data. Реализация метода по умолчанию просто добавляет объект, который будет доступен в шаблоне. Но переопределив метод, вы можете добавить любые дополнительные данные(расширить контекст):

        class ItemsListView(ListView):

            template_name = "gallery/items_listing.html"
            model = Item
            paginate_by = settings.PHOTOS_PER_PAGE

            
            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['page_title'] = _('Albums')
                return context


В общем случае, метод get_context_data объединяет(сливает вместе) данные контекста всех родительских классов с данными текущего класса. Чтобы сохранить такое поведение в пользовательских классах, в которых вы собираетесь изменять контекст, вы должны в начале вызвать метод get_context_data родительского класса. Если нет двух классов, которые пытаются определить одинаковый ключ, - вы получите желаемый результат. Однако, если есть некий класс, который пытается переопределить ключ, установленный родительскими классами(после вызова super), то любой потомок этого класса также должен явно установить такой ключ(после вызова super), если необходимо гарантировать полное переопределение данных родителей. Если у вас возникли проблемы, просмотрите mro(method resolution order) вашего представления.

Отображение подмножеств объектов
---------------------------------
Аргумент model, определяющий модель базы данных, с которой работает данное представление, доступен во всех общих представлениях-классах, которые предназначены для отображения единичного объекта или списка объектов. Тем не менее, аргумент model это не единственный способ, указать представлению с какими данными оно должно работать. Вы также можете указать необходимый список объектов используя аргумент queryset:


        class ItemObject(ListView):

            context_object_name = 'item'
            queryset = Item.objects.all()

Запись model = Item это всего лишь сокращенный вариант записи queryset = Item.objects.all(). Однако, используя queryset вы можете в полной мере использовать механизмы выборки данных, фильтрации , предоставив вашему представлению более конкретный список объектов, с которым оно должно работать. 

Вот простой пример: нам необходимо упорядочить список по дате публикации:


    class List(ListView):
        queryset = Item.objects.order_by('-publication_date')
        context_object_name = 'album_list'

Если мы хотим получить список определенного year='2015', мы можем использовать аналогичную технику:


        class List(ListView):
            model = Item
            paginate_by = settings.PHOTOS_PER_PAGE
            queryset = Item.objects.filter(item__year='2015')
            template_name = 'galery/album_list.html'

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['page_title'] = _('Albums')
                return context


Обратите внимание, что вместе с созданием отфильтрованной выборки объектов с использованием queryset, мы также используем другое(пользовательское) имя шаблона. Если мы этого не сделаем, представление будет использовать тот же шаблон, что и для отображения “родного” списка объектов, что нас не устраивает.


DetailView Просмотр информации об отдельном объекте
====================================================

DetailView - отвечает за просмотр отдельного объекта.
Чтобы получить единичный объект, нам необходимо его идентифицировать по какому-нибудь параметру. Обычно для этого используется так называемый уникальный первичный ключ (pk, id). Django также позволяет идентифицировать объект по полю slug, которое может быть любым уникальным словом. Разумеется для SEO иногда удобнее использовать именно slug, в случае если объектами выступают статьи или список пользователей. Однако в других случаях использовать для идентификации slug нет смысла (например просмотр комментария или личного сообщения). В таких случаях используется первичный ключ.

views.py
--------
        from django.views.generic import TemplateView, ListView, DetailView
        from .models import Item, Photo

        class IndexPageView(TemplateView):

            template_name = "gallery/index.html"

            def get_context_data(self, **kwargs):
                context = super(IndexPageView, self).get_context_data(**kwargs)
                context['item_list'] = Item.objects.all()[:3]
                return context

        class ItemsListView(ListView):

            template_name = "gallery/items_listing.html"

            model = Item

        class ItemObjectView(DetailView):

            template_name = "gallery/items_detail.html"

            model = Item

        class PhotoObjectView(DetailView):

            template_name = "gallery/photo_detail.html"

            model = Photo


наш объект будет доступен с помощью метода get_object. Этот метод поочередно пытается найти в маршруте переменные pk и slug, в данном случае переменная с именем pk будет обладать большим приоритетом. С помощью метода get_slug_field мы можем переопределить имя поля slug нашей модели. По умолчанию данный метод возвращает значение атрибута slug_field. Наш объект хранится в атрибуте object.

В случаях, когда необходимо отобразить огромное число объектов, крайне нежелательно выводить их все одновременно. В этом случае требуется механизм для постраничного вывода данных (пагинация). Класс DetailView наследует примесь MultipleObjectMixin, которая реализует требуемый нам функционал. Для определения количества объектов на страницу используется метод get_paginate_by, который по умолчанию возвращает значение атрибута paginate_by. С помощью атрибута мы можем без особых хлопот указать количество выводимых на 1 страницу объектов.

Иногда возникает необходимость реализовать постраничный вывод своим способом, для этого мы можем передать наш класс пагинации атрибуту paginator_class. По умолчанию этот атрибут содержит ссылку на стандартный класс Paginator, который реализован в модуле django.core.paginator.

Атрибут allow_empty определяет как обработать ситуацию, когда нет ни одного объекта в списке. Если мы установим значение данного атрибута в True (по умолчанию), то будет возвращаться пустой список объектов. В случае значения False будет возвращаться ошибка 404. Значение данного атрибута возвращает метод get_allow_empty. Его же можно использовать, если требуется некоторая дополнительная проверка или изменение логики.


Атрибут object_list хранит список наших объектов. Необходимо помнить о том, что мы должны не забыть передать текущую страницу нашему отображению для корректной работы. Наиболее простой способ — использование именованных групп в нашем файле urls.py

После того, как мы выбрали способ идентификации объекта, мы должны сообщить Django о своем выборе, передав переменную с соответствующим именем с помощью маршрута файла urls.py.

urls.py
-------

        from django.conf.urls import patterns, include, url
        from .views import ItemsListView, ItemObjectView, PhotoObjectView

        urlpatterns = patterns('',
            url(r'^$', ItemsListView.as_view(), name="item_list"),
            url(r'^(?P<pk>\d+)/$', ItemObjectView.as_view(), name="item_object"),
            url(r'^photo/(?P<pk>\d+)/$', PhotoObjectView.as_view(), name="photo_object")
        )


В шаблоне наш список объектов будет доступен по имени, которое задано с помощью атрибута context_object_name - item.name (или возвращается методом get_context_object_name). Объекты с текущей страницы находятся в переменной с именем object_list. Значение переменной is_paginated (булево значение) определяет разбит ли наш список объектов на страницы.


items_detail.html
-----------------

        {% extends "base.html" %}

        {% block title %}{{ object.name }}{% endblock %}

        {% block content %}

        <p><a href="{% url 'gallery:item_list' %}">&laquo; Back to full listing</a></p>
        <h2>{{ object.name }}</h2>
        <p>{{ object.description }}</p>

        <h3>Photos</h3>
        <table>
            <tr>
                <th>Title</th>
                <th>Thumbnail</th>
                <th>Caption</th>
            </tr>
            {% for photo in object.photo_set.all %}
            <tr>
                <td><i>{{ photo.title }}</i></td>
                <td>
                    <a href="{{ photo.get_absolute_url }}">
                        <img src="{{ photo.image.thumb_url }}" />
                    </a>
                </td>
                <td>{{ photo.caption }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endblock %}


photo_detail.html
-----------------

        {% extends "base.html" %}

        {% block title %}{{ object.item.name }} - {{ object.title }}{% endblock %}

        {% block content %}

        <a href="{{ object.item.get_absolute_url }}">&laquo; Back to {{ object.item.name }} detail page</a>
        <h2>{{ object.item.name }} - {{ object.title }}</h2>
        <img src="{{ object.image.url }}" />
        {% if object.caption %}
        <p>{{ object.caption }}</p>
        {% endif %}
        {% endblock %}

urls.py
-------

        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            url(r'', include('social.apps.django_app.urls', namespace='social')),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            
            url(r'^gallery/', include('gallery.urls', namespace='gallery')),

            url(r'^reviews/', include('reviews.urls', namespace='reviews')),
            url(r'^pages/(?P<url>.*)$', pages_views.main_view),
            url(r'^tinymce/', include('tinymce.urls')),
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            url(r'^users/', include('userprofiles.urls', namespace="users")),
        ]
