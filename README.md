# tdd-django unit_08

EmailField
-----------
    class EmailField([max_length=75, **options])
Поле CharField для хранения правильного email-адреса.

Значение max_length в 75 символов не достаточно для хранения всех возможных значений в соответствии RFC3696/5321. Для хранения всех возможных вариантов необходимо значение max_length в 254. Значение в 75 символов сложилось исторически и не изменяется для обратной совместимости.

DecimalField
-------------
        class DecimalField(max_digits=None, decimal_places=None[, **options])
Десятичное число с фиксированной точностью, представленное объектом Decimal Python. Принимает два обязательных параметра:

- DecimalField.max_digits
Максимальное количество цифр в числе - это число должно быть больше или равно decimal_places.

- DecimalField.decimal_places
Количество знаков после запятой.

Например, для хранения числа до 999 с двумя знаками после запятой, используйте:

- models.DecimalField(..., max_digits=5, decimal_places=2)
Для хранения числа до миллиарда и 10 знаков после запятой:

- models.DecimalField(..., max_digits=19, decimal_places=10)
Виджет по умолчанию для этого поля TextInput.


PositiveIntegerField
---------------------
        class PositiveIntegerField([**options])
Как и поле IntegerField, но значение должно быть больше или равно нулю (0). Можно использовать значение от 0 до 2147483647. Значение 0 принимается для обратной совместимости.

Orders
======
shop/models.py
---------------

        @python_2_unicode_compatible
        class Order(models.Model):
            first_name = models.CharField(max_length=50)
            last_name = models.CharField(max_length=50)
            email = models.EmailField()
            address = models.CharField(max_length=250)
            postal_code = models.CharField(max_length=20)
            city = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True)
            paid = models.BooleanField(default=False)

            class Meta:
                ordering = ('-created',)

            def __str__(self):
                return 'Order {}'.format(self.id)

            def get_total_cost(self):
                return sum(item.get_cost() for item in self.items.all())

        @python_2_unicode_compatible
        class OrderItem(models.Model):
            order = models.ForeignKey(Order, related_name='items')
            product = models.ForeignKey(Product, related_name='order_items')
            price = models.DecimalField(max_digits=10, decimal_places=2)
            quantity = models.PositiveIntegerField(default=1)

            def __str__(self):
                return '{}'.format(self.id)

            def get_cost(self):
                return self.price * self.quantity


ModelAdmin.raw_id_fields
-------------------------
По умолчанию Django использует select для полей ForeignKey. Если связанных объектов очень много, создание select может быть очень затратным процессом.

raw_id_fields содержит список полей, которые будут использовать поле Input для ForeignKey или ManyToManyField:

        class ArticleAdmin(admin.ModelAdmin):
            raw_id_fields = ("newspaper",)
Виджет поля для raw_id_fields будет содержать значение первичного ключа для ForeignKey или список ключей для ManyToManyField. Возле поля есть кнопка поиска и выбора связанных объектов


Объект InlineModelAdmin
-----------------------
- class InlineModelAdmin
- class TabularInline
- class StackedInline

Интерфейс администратора позволяет редактировать связанные объекты на одной странице с родительским объектом. Это называется “inlines”. Например, у нас есть две модели:

    from django.db import models

    class Author(models.Model):
       name = models.CharField(max_length=100)

    class Book(models.Model):
       author = models.ForeignKey(Author)
       title = models.CharField(max_length=100)

Вы можете редактировать книги автора на странице редактирования автора. Вы добавляете “inlines” к модели добавив их в ModelAdmin.inlines:

        from django.contrib import admin

        class BookInline(admin.TabularInline):
            model = Book

        class AuthorAdmin(admin.ModelAdmin):
            inlines = [
                BookInline,
            ]
Django предоставляет два подкласса InlineModelAdmin:
----------------------------------------------------
- TabularInline
- StackedInline
Разница между ними только в используемом шаблоне.

Параметры InlineModelAdmin
---------------------------
InlineModelAdmin содержит некоторые возможности ModelAdmin и собственные. Общие методы и атрибуты определены в классе BaseModelAdmin:

form
fieldsets
fields
formfield_overrides
exclude
filter_horizontal
filter_vertical
ordering
prepopulated_fields
get_queryset()
radio_fields
readonly_fields
raw_id_fields
formfield_for_choice_field()
formfield_for_foreignkey()
formfield_for_manytomany()
has_add_permission()
has_change_permission()
has_delete_permission()

Параметры класса InlineModelAdmin:
----------------------------------
- InlineModelAdmin.model
Модель используемая в “inline”. Обязательный параметр.

- InlineModelAdmin.fk_name
Название внешнего ключа модели. В большинстве случаев он определяется автоматически, но вы должны указать fk_name, если модель содержит несколько внешних ключей к родительской модели.

- InlineModelAdmin.formset
По умолчанию – BaseInlineFormSet. Использование собственного класса предоставляет большие возможности для переопределения поведения по умолчанию. Смотрите раздел о наборах модельных форм.

- InlineModelAdmin.form
Значение form по умолчанию – ModelForm. Это значение передается в inlineformset_factory() при создании набора форм.

При добавлении собственной валидации в форму InlineModelAdmin, учитывайте состояние родительской модели. Если родительская форма не пройдет валидацию, она может содержать не консистентные данные.

- InlineModelAdmin.extra
Указывает количество пустых форм для добавления объектов в наборе форм. Подробности смотрите в разделе о наборе форм.

Если JavaScript включен в браузере, ссылка “Add another” позволит добавить новую пустую форму в дополнение к формам указанным параметром extra.

Ссылка не появится если количество отображаемых форм превышает значение в параметре max_num, или если у пользователя отключен JavaScript.

InlineModelAdmin.get_extra() позволяет указать количество дополнительных форм.

- InlineModelAdmin.max_num
Указывает максимальное количество форм. Этот параметр не определяет количество связанных объектов. Подробности смотрите в разделе Ограничение количества редактируемых объектов.

InlineModelAdmin.get_max_num() позволяет указать максимальное количество дополнительных форм.

- InlineModelAdmin.min_num
Указывает минимальное количество отображаемых форм.

InlineModelAdmin.get_min_num() позволяет указать минимальное количество отображаемых форм.

- InlineModelAdmin.raw_id_fields
По умолчанию Django использует select для полей ForeignKey. Если связанных объектов очень много, создание select может быть очень затратным процессом.

- raw_id_fields – список полей которые должны использовать Input виджет для полей ForeignKey или ManyToManyField:

        class BookInline(admin.TabularInline):
            model = Book
            raw_id_fields = ("pages",)
        InlineModelAdmin.template
Шаблон для отображения.
-----------------------
- InlineModelAdmin.verbose_name
Позволяет переопределить значение verbose_name класса Meta модели.

- InlineModelAdmin.verbose_name_plural
Позволяет переопределить значение verbose_name_plural класса Meta модели.

- InlineModelAdmin.can_delete
Определяет можно ли удалять связанные объекты. По умолчанию равно True.

- InlineModelAdmin.get_formset(request, obj=None, **kwargs)
Возвращает BaseInlineFormSet, который будет использоваться на странице создания/редактирования.

- InlineModelAdmin.get_extra(request, obj=None, **kwargs)
Возвращает количество форм. По умолчанию возвращает значение атрибута InlineModelAdmin.extra.

Вы можете переопределить метод и добавить логику для определения количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj):

        class BinaryTreeAdmin(admin.TabularInline):
            model = BinaryTree

            def get_extra(self, request, obj=None, **kwargs):
                extra = 2
                if obj:
                    return extra - obj.binarytree_set.count()
                return extra

- InlineModelAdmin.get_max_num(request, obj=None, **kwargs)
Возвращает максимальное количество дополнительных форм. По умолчанию возвращает значение атрибута InlineModelAdmin.max_num.

Вы можете переопределить метод и добавить логику для определения максимального количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj):

        class BinaryTreeAdmin(admin.TabularInline):
            model = BinaryTree

            def get_max_num(self, request, obj=None, **kwargs):
                max_num = 10
                if obj.parent:
                    return max_num - 5
                return max_num
- InlineModelAdmin.get_min_num(request, obj=None, **kwargs)
Возвращает минимальное количество дополнительных форм. По умолчанию возвращает значение атрибута InlineModelAdmin.min_num.

Вы можете переопределить метод и добавить логику для определения минимального количества форм. Например, учитывать данные объекта модели(передается как именованный аргумент obj).


shop/admin.py
--------------

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    
admin.site.register(Order, OrderAdmin)


shop/views.py
--------------

        from django.shortcuts import render
        from .models import OrderItem
        from .forms import OrderCreateForm
        from .tasks import order_created
        from .cart import Cart

        def order_create(request):
            cart = Cart(request)
            if request.method == 'POST':
                form = OrderCreateForm(request.POST)
                if form.is_valid():
                    order = form.save()
                    for item in cart:
                        OrderItem.objects.create(order=order,
                                                 product=item['product'],
                                                 price=item['price'],
                                                 quantity=item['quantity'])
                    # clear the cart
                    cart.clear()
                    # launch task
                    order_created(order.id)
                    return render(request, 'shop/orders/created.html', {'order': order})
            else:
                form = OrderCreateForm()
            return render(request, 'shop/orders/create.html', {'cart': cart,
                                                        'form': form})

shop/forms.py
---------------
```
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']

```
shop/tasks.py
---------------
```
from django.core.mail import send_mail
from .models import Order

def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent

```

shop/orders/create.html
-----------------------

        {% extends "shop/base.html" %}

        {% block title %}  Checkout {% endblock %}

        {% block content %}
            <h1>Checkout</h1>
            <div class="order-info">
                <h3>Your order</h3>
                <ul>
                    {% for item in cart %}
                        <li>{{ item.quantity }}x {{ item.product.name }} <span>${{ item.total_price }}</span></li>
                    {% endfor %}
                </ul>
                <p>Total: ${{ cart.get_total_price }}</p>
            </div>
            <form action="." method="post" class="order-form">
                {{ form.as_p }}
                <p><input type="submit" value="Place order"></p>
                {% csrf_token %}
            </form>
        {% endblock %}


shop/orders/created.html
------------------------

        {% extends "shop/base.html" %}

        {% block title %}
            Thank you
        {% endblock %}

        {% block content %}
            <h1>Thank you</h1>
            <p>Your order has been successfully completed. Your order number is <strong>{{ order.id }}</strong>.</p>
        {% endblock %}


shop/urls.py
-------------

        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^create/$', views.order_create, name='order_create'),
        ]


shop/product/detail.html
------------------------

            {% extends "shop/base.html" %}
            {% load static %}

            {% block title %}
                Your shopping cart
            {% endblock %}

            {% block content %}
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
                    <a href="{% url "shop:product_list" %}" class="button light">Continue shopping</a>
                    <a href="{% url "shop:order_create" %}" class="button">Checkout</a>
                </p>
            {% endblock %}

Отправка электронных писем
===========================
Код находится в модуле django.core.mail.

Пример
```
from django.core.mail import send_mail

send_mail('Subject here', 'Here is the message.', 'from@example.com',
    ['to@example.com'], fail_silently=False)
```
Письмо отправлено через SMTP хост и порт, которые указаны в настройках EMAIL_HOST и EMAIL_PORT. Настройки EMAIL_HOST_USER и EMAIL_HOST_PASSWORD, если указаны, используются для авторизации на SMTP сервере, а настройки EMAIL_USE_TLS и EMAIL_USE_SSL указывают использовать ли безопасное соединение.

При отправке письма через django.core.mail будет использоваться кодировка из DEFAULT_CHARSET.
send_mail()
```
send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
```
Самый простой способ отправить письмо – использовать django.core.mail.send_mail().

Параметры subject, message, from_email и recipient_list являются обязательными.
-------------------------------------------------------------------------------
1. subject: строка.
2. message: строка.
3. from_email: строка.
4. recipient_list: список строк, каждая является email. Каждый получатель из recipient_list будет видеть остальных получателей в поле “To:” письма.
5. fail_silently: булево. При False send_mail вызовет smtplib.SMTPException. 
6. auth_user: необязательное имя пользователя, которое используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_USER.
7. auth_password: необязательный пароль, который используется при авторизации на SMTP сервере. Если не указано, Django будет использовать значение EMAIL_HOST_PASSWORD.
8. connection: необязательный бэкенд, который будет использоваться для отправки письма. Если не указан, будет использоваться бэкенд по умолчанию. 
9. html_message: если html_message указано, письмо будет с multipart/alternative, и будет содержать message с типом text/plain, и html_message с типом text/html.

Возвращает количество успешно отправленных писем (которое будет 0 или 1, т.к. функция отправляет только одно письмо).

Пример
------
Отправляет одно письмо john@example.com и jane@example.com, они оба указаны в “To:”:
```
send_mail('Subject', 'Message.', 'from@example.com',
    ['john@example.com', 'jane@example.com'])
```

Бэкенды для отправки электронной почты
---------------------------------------
Непосредственная отправка электронного письма происходит в бэкенде.

Django предоставляет несколько бэкендов. Эти бэкенды, кроме SMTP (который используется по умолчанию), полезны только при разработке или тестировании. Вы можете создать собственный бэкенд.

SMTP бэкенд
===========

Это бэкенд по умолчанию. Почта отправляется через SMTP сервер. Адрес сервера и параметры авторизации указаны в настройках EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_TIMEOUT, EMAIL_SSL_CERTFILE и EMAIL_SSL_KEYFILE.

SMTP бэкенд используется в Django по умолчанию. Если вы хотите указать его явно, добавьте в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
Dummy бэкенд
------------
Этот бэкенд ничего не делает с почтой. Чтобы указать этот бэкенд, добавьте следующее в настройки:
```
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
```
Этот бэкенд не следует использовать на боевом сервере, он создавался для разработки.

Настройка почты при разработке
==============================

Самый простой способ настроить почту для разработки – использовать бэкенд console. Этот бэкенд перенаправляет всю почту в stdout, позволяя увидеть содержимое писем.

Также можно использовать file. Этот бэкенд сохраняет содержимое каждого SMTP-соединения в файл.

Еще один способ – использовать локальный SMTP-сервер, который принимает письма и выводит их в консоль, но никуда их не оправляет. Python позволяет создать такой сервер одной командой:
```
python -m smtpd -n -c DebuggingServer localhost:1025
```
Эта команда запускает простой SMTP-сервер, который слушает 1025 порт на localhost. Этот сервер выводит заголовки и содержимое полученных писем в консоль. Вам необходимо указать в настройках EMAIL_HOST и EMAIL_PORT. Подробности об этом SMTP-сервер смотрите в документации Python к модулю smtpd.

settings.py
-----------
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = 'janusnic@gmail.com'
EMAIL_PORT = 1025

```
Пароли приложений Gmail
=======================
https://support.google.com/accounts/
Если вы пользуетесь двухэтапной аутентификацией, то специальные пароли понадобятся вам для входа в некоторые приложения (например, Outlook или почтовый клиент на iPhone/Mac). Вам не нужно запоминать эти пароли – наша система сгенерирует их автоматически. Подробнее...

Откройте настройки аккаунта Google на своем устройстве и введите шестнадцатизначный пароль, указанный выше.
Этот пароль открывает приложению или устройству доступ к вашему аккаунту Google (как и обычный пароль). Его не нужно запоминать. Также просим вас не записывать его и никому не показывать.


Create an Application specific password
---------------------------------------
- Visit your Google Account security page.
- In the 2-Step Verification box, click Settings(if there is no settings link, you may want to create a new one. you can skip step 3 & 4).
- Click the tab for App-specific passwords.
- Click Manage your application specific passwords.
- Under the Application-specific passwords section, enter a descriptive name for the application you want to authorize, such as "Django gmail" then click Generate application-specific password button.
- note down the password. for example: smbumqjiurmqrywn 

Then add the appropriate values to settings.py:
------------------------------------------------
```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-username@gmail.com'
EMAIL_HOST_PASSWORD = 'Application spectific password(for eg: smbumqjiurmqrywn)'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
You can use the shell to test it:
```
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'This is a test', 'your@email.com', ['toemail@email.com'],
     fail_silently=False)
```