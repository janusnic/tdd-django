# tdd-django unit_10

Аутентификация пользователей в Django
=====================================
Django поставляется с системой аутентификации пользователей. Она обеспечивает пользовательские аккаунты, группы, права и сессии на основе куки.

Система аутентификации Django отвечает за оба аспекта: аутентификацию и авторизацию. аутентификация проверяет пользователя, а авторизация определяет, что аутентифицированный пользователь может делать.

Система аутентификации состоит из:
----------------------------------
1. Пользователей

2. Прав: Бинарные (да/нет) флаги, определяющие наличие у пользователя права выполнять определённые действия.

3. Групп: Общий способ назначения меток и прав на множество пользователей.

4. Настраиваемой системы хеширования паролей

5. Инструментов для форм и представлений для аутентификации пользователей или для ограничения доступа к контенту

Поддержка аутентификации скомпонована в виде модуля в django.contrib.auth. По умолчанию, требуемые настройки уже включены в settings.py, создаваемый с помощью команды django-admin startproject, и представляют собой две записи в параметре конфигурации INSTALLED_APPS:

1. 'django.contrib.auth' содержит ядро системы аутентификации и её стандартные модели.

2. 'django.contrib.contenttypes' является фреймворком типов, который позволяет правам быть назначенными на создаваемые вами модели.

две записи в параметре конфигурации MIDDLEWARE_CLASSES:
-------------------------------------------------------
1. SessionMiddleware управляет сессиями во время запросов.

2. AuthenticationMiddleware ассоциирует пользователей с запросами с помощью сессий.

При наличии этих настроек, применение команды manage.py migrate создаёт в базе данных необходимые для системы аутентификации таблицы, создаёт права для любых моделей всех зарегистрированных приложений.

Использование системы аутентификации пользователя
=================================================

Создание пользователей
----------------------
        Самый простой способ создать пользователя – использовать метод create_user():

        from django.contrib.auth.models import User
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        # At this point, user is a User object that has already been saved
        # to the database. You can continue to change its attributes
        # if you want to change other fields.
        user.last_name = 'Lennon'
        user.save()

Создание суперпользователя
--------------------------
Суперпользователя можно создать с помощью команды createsuperuser:

    $ python manage.py createsuperuser --username=joe --email=joe@example.com

Команда попросит ввести пароль. Пользователь будет создан сразу же по завершению команды. Если не указывать --username или the --email, команда попросит ввести их.


UserProfile:
============

        ./manage.py startapp userprofiles

settings.py
------------

        # Application definition
        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'ckeditor',
            'ckeditor_uploader',
            'shop',
            'userprofiles',
        ]

userprofiles/models.py
--------------------------

        from django.db import models
        from django.utils.encoding import python_2_unicode_compatible
        from django.contrib.auth.models import User
        from django.db.models.signals import post_save
        
        @python_2_unicode_compatible
        class UserProfile(models.Model):
            # This line is required. Links UserProfile to a User model instance.
            user = models.OneToOneField(User)

            # The additional attributes we wish to include.

            location = models.CharField(max_length=140, blank=True)
            gender = models.CharField(max_length=140, blank=True)
            age = models.IntegerField(default=0, blank=True)
            company = models.CharField(max_length=50, blank=True)

            website = models.URLField(blank=True)
            profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

            # Override the __str__() method to return out something meaningful!
            def __str__(self):
                return self.user.username

        def create_profile(sender, instance, created, **kwargs):
            if created:
                profile, created = UserProfile.objects.get_or_create(user=instance)

        # Signal while saving user
        post_save.connect(create_profile, sender=User)



get_or_create(defaults=None, **kwargs)
--------------------------------------
Удобный метод для поиска объекта по заданным параметрам поиска kwargs (может быть пустым, если все поля содержат значения по умолчанию), и создания нового при необходимости.

Возвращает кортеж (object, created), где object полученный или созданный объект и created – булево значение, указывающее был ли создан объект.

Этот метод удобно использовать для скриптов импорта данных. Например:

        try:
            obj = Person.objects.get(first_name='John', last_name='Lennon')
        except Person.DoesNotExist:
            obj = Person(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
            obj.save()
Такой способ становится весьма громоздким при увеличении количества полей модели. Пример выше может быть переписан с использованием метода get_or_create():

        obj, created = Person.objects.get_or_create(first_name='John', last_name='Lennon',
                          defaults={'birthday': date(1940, 10, 9)})

Все именованные аргументы переданные в get_or_create() — кроме одного не обязательного defaults — будут использованы при вызове get(). Если объект найден, get_or_create() вернет этот объект и False. Если найдено несколько объектов - будет вызвано исключение MultipleObjectsReturned. Если объект не найден, get_or_create() создаст и сохранит новый объект, возвращая новый объект и True. Новый объект будет создан примерно за таким алгоритмом:

        params = {k: v for k, v in kwargs.items() if '__' not in k}
        params.update(defaults)
        obj = self.model(**params)
        obj.save()

Это означает, что будут выбраны именованные аргументы кроме 'defaults' и не содержащие двойное подчеркивание (которые указывают на не-точный поиск). Затем добавляются значения из defaults, перезаписывая ключи при необходимости, полученные данные используются как аргументы для конструктора класса модели. Как уже указывалось выше, это упрощенный алгоритм, но все важные детали указаны. 

Если модель содержит поле defaults и вы хотите использовать его в параметрах поиска в get_or_create(), просто используйте 'defaults__exact':

    Foo.objects.get_or_create(defaults__exact='bar', defaults={'defaults': 'baz'})

Метод get_or_create() использует аналогичное поведение с ошибками что и метод create(), если вы самостоятельно определяете значение первичного ключа. Если объект должен быть создан и значение первичного ключа уже существует в базе данных, будет вызвано исключение IntegrityError.

Этот метод атомарный при правильном использовании, правильной настройке и работе БД. Однако, если уникальность полей не контролируется на уровне БД(unique или unique_together), этот метод склонен к “гонке-состояний” и в БД могут попасть не уникальные данные(при нескольких процессах запросы могут одновременно отправиться на выполнения к БД, а там уже ничего не проверяется).

При использовании MySQL, убедитесь что используете READ COMMITTED вместо REPEATABLE READ (по умолчанию), иначе get_or_create может вызывать IntegrityError, но объект не будет возвращен последующим вызовом get().

Наконец, несколько слов об использовании get_or_create() в представлениях Django. Пожалуйста используйте его только для POST запросов, если только у вас нет основательных причин не делать этого. Запросы GET не должны влиять на данные; используйте запрос POST для изменения данных. 

Вы можете использовать get_or_create() с атрибутами ManyToManyField и обратными внешними связями. При это запросы будут ограничены контекстом связи. Это может вызвать некоторые проблемы при создании объектов.

Возьмем следующие модели:

        class Chapter(models.Model):
            title = models.CharField(max_length=255, unique=True)

        class Book(models.Model):
            title = models.CharField(max_length=256)
            chapters = models.ManyToManyField(Chapter)

Вы можете использовать get_or_create() для поля chapters модели Book, но будут учитывать только объекты связанные с конкретной книгой:

        >>> book = Book.objects.create(title="Ulysses")
        >>> book.chapters.get_or_create(title="Telemachus")
        (<Chapter: Telemachus>, True)
        >>> book.chapters.get_or_create(title="Telemachus")
        (<Chapter: Telemachus>, False)
        >>> Chapter.objects.create(title="Chapter 1")
        <Chapter: Chapter 1>
        >>> book.chapters.get_or_create(title="Chapter 1")
        # Raises IntegrityError

Это произошло, потому что мы пытались получить или создать “Chapter 1” для книги “Ulysses”, но ни один объект не был найден, т.к. он не связан с этой книгой, и мы получили ошибку при попытке его создать т.к. поле title должно быть уникальным.


Прослушивание сигналов
======================
Для того, чтобы принять сигнал, Вам необходимо с помощью метода Signal.connect() зарегистрировать функцию receiver, которая вызывается, когда сигнал послан:

        Signal.connect(receiver[, sender=None, weak=True, dispatch_uid=None])
Параметры:  
- receiver – Функция, которая будет привязана к этому сигналу. Смотрите Функции-получатели.
- sender – Указывает конкретного отправителя. Смотрите Сигналы, получаемые от определённых отправителей..
- weak – Django сохраняет обработчики сигналов используя слабые ссылки(weak references). Поэтому, если функция-обработчик является локальной функцией, сборщик мусора может удалить ее. Чтобы избежать этого, передайте weak=False в connect().
- dispatch_uid – Уникальный идентификатор получателя сигнала. На случай, если назначение обработчика может вызываться несколько раз. Смотрите Предотвращение дублирования сигналов.

Функции-получатели
------------------
Во-первых, мы должны определить функцию-получатель. Получатель должен быть Python функцией или методом:

        def my_callback(sender, **kwargs):
            print("Request finished!")
Заметьте, что функция принимает аргумент sender, а также аргументы (**kwargs) в формате словаря; все обработчики сигналов должны принимать подобные аргументы.

Все сигналы имеют возможность посылать именованные аргументы и могут изменить их набор в любой момент. Сигнал request_finished документирован как не посылающий аргументов, и у нас может появиться искушение записывать наш обработчик сигнала в виде my_callback(sender).

Регистрация функции-получателя
------------------------------
Есть два способа, которыми Вы можете подключить получатель к сигналу. Вы можете вручную вызвать connect:

        from django.core.signals import request_finished

        request_finished.connect(my_callback)
Кроме того, вы можете использовать декоратор receiver() при определении вашего получателя:

        receiver(signal)
Параметры:  signal – Сигнал или список обрабатываемых сигналов.
Вот как можно использовать декоратор:

        from django.core.signals import request_finished
        from django.dispatch import receiver

        @receiver(request_finished)
        def my_callback(sender, **kwargs):
            print("Request finished!")
Теперь наша функция my_callback будет вызываться каждый раз, когда запрос завершается.

Код обработчиков сигналов и подключения может находиться где угодно. Но мы рекомендуем избегать корневого модуля приложения и models, чтобы сократить побочный эффект при импорте приложения.

На практике, обработчики сигналов лежат в модуле signals приложения, к которому они относятся. Подключение к сигналам выполняется в методе ready() конфигурационного класса приложения. При использовании декоратора receiver() просто импортируйте модуль signals в ready().

Т.к. ready() не существует в предыдущих версиях Django, регистрацию обработчиков сигналов обычно выполняют в модуле models.

Метод ready() можно выполнить более одного раза во время тестировани, таким образом, вам может потребоваться защитить ваши сигналы от дублирования, особенно, если вы планируете отправлять их из тестов.
Сигналы, получаемые от определённых отправителей.
-------------------------------------------------
Некоторые сигналы могу быть посланы много раз, но Вам будет нужно получать только определённое подмножество этих сигналов. Например, рассмотрим django.db.models.signals.pre_save - сигнал, посылаемый перед сохранением модели. Бывает, что Вам не нужно знать о сохранении любой модели, Вас интересует только одна конкретная модель:

В этих случаях Вы можете получать только сигналы, посланные определёнными отправителями. В случае django.db.models.signals.pre_save отправитель будет сохраняемой моделью некоторого класса, так что вы можете указать, что вы хотите получать только сигналы, посылаемые этой моделью:

        from django.db.models.signals import pre_save
        from django.dispatch import receiver
        from myapp.models import MyModel


        @receiver(pre_save, sender=MyModel)
        def my_handler(sender, **kwargs):
            ...
Функция my_handler будет вызвана только при сохранении объекта класса MyModel.

Предотвращение дублирования сигналов
-------------------------------------
В некоторых случаях модуль, в котором Вы подключаете сигналы, может быть импортирован несколько раз. Это может привести к тому, что получатель сигнала будет зарегистрирован несколько раз, и таким образом, вызов сигнала произойдет несколько раз при наступлении одного и того же события.

Такое поведение может приводить к проблемам (например, если происходит отправка электронной почты всякий раз, когда посылается сигнал о сохранении модели), поэтому передавайте некоторый уникальный идентификатор в качестве значения аргумента dispatch_uid для идентификации в функции-получателе. Обычно, этот идентификатор является строкой, хотя подойдёт любой хешируемый объект. В итоге функция-получатель будет привязана к сигналу единожды для каждого уникального значения dispatch_uid.

        from django.core.signals import request_finished

        request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")
Создание и посылка сигналов.
---------------------------
Вы можете создавать свои собственные сигналы в ваших приложениях.

Создание сигналов
-----------------
        class Signal([providing_args=list])
Все сигналы являются экземплярами класса django.dispatch.Signal, где providing_args – список названий аргументов сигнала, которые будут доступны слушателям. Этот аргумент предназначен просто для документирования, никакой проверки, передаёт ли сигнал эти параметры, не выполняется.

Например:

        import django.dispatch

        pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])
Это объявление сигнала pizza_done, который предоставит получателям аргументы toppings и size.

Вы можете задать в этом списке аргументов любые значения передаваемых параметров.

Отправка сигналов
------------------
В Django существует два способа отправки сигналов.

        Signal.send(sender, **kwargs)
        Signal.send_robust(sender, **kwargs)
Для отправки сигнала необходимо вызвать Signal.send() или Signal.send_robust(). Вы обязательно должны указать аргумент ``sender``(обычно это класс), кроме того можно указать сколько угодно других именованных аргументов.

Например, вот как может выглядеть отправка сигнала pizza_done:

        class PizzaStore(object):
            ...

            def send_pizza(self, toppings, size):
                pizza_done.send(sender=self.__class__, toppings=toppings, size=size)
                ...
И send(), и send_robust() возвращают список кортежей пар [(receiver, response), ... ]. Каждый кортеж содержит вызываемую функцию и ее ответ.

send() отличается от send_robust() способом обработки исключений, генерируемых функцией-получателем. send() не ловит никаких исключений, сгенерированных в получателе, позволяя исключению проваливаться дальше. Таким образом, не все получатели могут получить сигнал при возникновении ошибки.

send_robust() перехватывает все ошибки, наследуемые от класса Exception языка Python, и гарантирует, что сигнал дойдёт до всех получателей. Если произойдёт ошибка в одном из них, экземпляр исключения будет помещён в кортежную пару, для получателя, который соответствует вызываемой ошибке.

Трассировочная информация доступна через атрибут __traceback__ ошибок, возвращаемых при вызове send_robust().

Отключение сигнала
------------------
        Signal.disconnect([receiver=None, sender=None, weak=True, dispatch_uid=None])
Чтобы отключить получатель от сигнала, вызовите Signal.disconnect(). Аргументы те же, что и у Signal.connect(). Метод возвращает True в случае, если получатель был отключен и False - если нет.

В аргументе receiver указывается получатель, который должен перестать получать сигнал. Аргумент может содержать None, если для идентификации получателя используется dispatch_uid.

Migrations
------------

        ./manage.py makemigrations userprofiles
        Migrations for 'userprofiles':
          0001_initial.py:
            - Create model UserProfile
        ./manage.py migrate
        Operations to perform:
          Apply all migrations: sessions, blog, admin, userprofiles, contenttypes, auth
        Running migrations:
          Rendering model states... DONE
          Applying userprofiles.0001_initial... OK

Объект InlineModelAdmin
=======================
Интерфейс администратора позволяет редактировать связанные объекты на одной странице с родительским объектом. Это называется “inlines”.

Вы можете редактировать userprofile на странице редактирования user.

Вы добавляете “inlines” к модели добавив их в ModelAdmin.inlines:
userprofiles/admin.py
-------------------------

        from django.contrib import admin
        from .models import UserProfile
        from django.contrib.auth.admin import UserAdmin
        from django.contrib.auth import get_user_model

        class UserProfileInline(admin.StackedInline):
            model = UserProfile
            can_delete = False

        class UserProfileAdmin(UserAdmin):
            inlines=(UserProfileInline, )

        admin.site.unregister(get_user_model())
        admin.site.register(get_user_model(), UserProfileAdmin)


Django предоставляет два подкласса InlineModelAdmin:
------------------------------------------------------------------
  1. TabularInline
  2. StackedInline
  Разница между ними только в используемом шаблоне.

Создание форм в Django Класс Form
=================================

        from django import forms
        from django.contrib.auth.models import User

        class RegistrationForm(forms.Form):
            username = forms.RegexField(label="Username", max_length=30,
                regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
            email = forms.EmailField(label='E-mail')
            password = forms.CharField(label='Password',
                widget=forms.PasswordInput(render_value=False))

Максимальное количество символом в значении мы указали с помощью параметра max_length. Он используется для двух вещей. Будет добавлен атрибут maxlength="30" в HTML тег input (теперь браузер не позволит пользователю ввести больше символов, чем мы указали). Также Django выполнит проверку введенного значения, когда получит запрос с браузера с введенными данными.

Экземпляр Form содержит метод is_valid(), который выполняет проверку всех полей формы. Если все данные правильные, это метод:
- вернет True
- добавит данные формы в атрибут cleaned_data.

После рендеринга наша форма будет выглядеть следующим образом:


        <p><label for="id_username">Username:</label> <input class="form-control" id="id_username" maxlength="30" name="username" placeholder="Enter Your User Name" type="text" /></p>
        <p><label for="id_email">E-mail:</label> <input class="form-control" id="id_email" name="email" placeholder="johndoe@company.com" type="email" /></p>
        <p><label for="id_password">Password:</label> <input class="form-control" id="id_password" name="password" placeholder="Easy to remember, hard to guess" type="password" /></p>

Обратите внимание, она не содержит тег form, или кнопку отправки. Вам необходимо самостоятельно их добавить в шаблоне.

Представление
--------------
Данные формы отправляются обратно в Django и обрабатываются представлением, обычно тем же, которое и создает форму. Это позволяет повторно использовать часть кода.

Для обработки данных формой нам необходимо создать ее в представлении для URL, на который браузер отправляет данные формы:

        # -*- coding: utf-8 -*-
        from django.contrib.auth import authenticate, login
        from django.shortcuts import redirect
        from django.views.generic import FormView, TemplateView

        from userprofiles.utils import get_form_class
        from django.core.urlresolvers import reverse
        from django.http import HttpResponseRedirect, HttpResponse

        class RegistrationView(FormView):
            form_class = get_form_class('userprofiles.forms.RegistrationForm')
            template_name = 'userprofiles/registration.html'

            def form_valid(self, form):
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # return redirect(up_settings.REGISTRATION_REDIRECT)
                url = reverse('users:userprofiles_registration_complete')
                return HttpResponseRedirect(url)

        registration = RegistrationView.as_view()


Если в представление пришел GET запрос, будет создана пустая форма и добавлена в контекст шаблона для последующего рендеринга. Это мы и ожидаем получить первый раз открыв страницу с формой.

Если форма отправлена через POST запрос, представление создаст форму с данными из запроса: form = RegistrationForm(request.POST) Это называется “привязать данные к форме” (теперь это связанная с данными форма).

Шаблон
----------
templates/userprofiles/registration.html
---------------------------------------------

        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Register with Blog {% endblock %}

        {% block content %}
        <div class="container">
            <div class="row">
            <h2>Register with Janus Blog</h2>
            <form action="." method="post" class="form-horisontal" role="form">
              <div class="form-group">
                {% csrf_token %}
                <fieldset>
                    {{ form.as_p }}
                </fieldset>
              </div>
              </div>
              <div class="row">
              <div class="form-group">
                <fieldset class="submit-row">
                    <p><button type="submit" class="btn btn-info">Create account</button></p>
                </fieldset>
              </div>
            </form>
            </div>
        </div>
        {% endblock %}


RegistrationForm
===========
forms.py
---------

        # -*- coding: utf-8 -*-
        from django import forms
        from django.contrib.auth.models import User

        class RegistrationForm(forms.Form):
            username = forms.RegexField(label="Username", max_length=30,
                regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
            email = forms.EmailField(label='E-mail')
            password = forms.CharField(label='Password',
                widget=forms.PasswordInput(render_value=False))

            def __init__(self, *args, **kwargs):
                super(RegistrationForm, self).__init__(*args, **kwargs)

            def save(self, *args, **kwargs):
                new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password'],
                        email=self.cleaned_data['email']
                    )

                if hasattr(self, 'save_profile'):
                    self.save_profile(new_user, *args, **kwargs)

                return new_user


Field.widget
--------------
Настройка классов виджета
--------------------------------
attrs
-----
Словарь, которые содержит HTML атрибуты, которые будут назначены сгенерированному виджету.

forms.py
---------

        # -*- coding: utf-8 -*-
        from django import forms
        from django.contrib.auth.models import User

        class RegistrationForm(forms.Form):
            username = forms.RegexField(label="Username", max_length=30,
                regex=r'^[\w.-]+$', error_messages={'invalid': 'This value may contain only letters, numbers and ./-/_ characters.'})
            email = forms.EmailField(label='E-mail')
            password = forms.CharField(label='Password',
                widget=forms.PasswordInput(render_value=False))

            def __init__(self, *args, **kwargs):
                super(RegistrationForm, self).__init__(*args, **kwargs)

                self.fields['username'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'Enter Your User Name'})

                self.fields['email'].widget.attrs.update({'class' : 'form-control', 'placeholder' : 'johndoe@company.com'})

                self.fields['password'].widget.attrs.update({'class' : 'form-control'})
                self.fields['password'].widget.attrs.update({'placeholder' : 'Easy to remember, hard to guess'})

            def save(self, *args, **kwargs):
                new_user = User.objects.create_user(
                        username=self.cleaned_data['username'],
                        password=self.cleaned_data['password'],
                        email=self.cleaned_data['email']
                    )

                if hasattr(self, 'save_profile'):
                    self.save_profile(new_user, *args, **kwargs)

                return new_user


Представления-классы для редактирования данных
==============================================
FormView
-----------

        class RegistrationView(FormView):
            form_class = get_form_class('userprofiles.forms.RegistrationForm')
            template_name = 'userprofiles/registration.html'

            def form_valid(self, form):
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # return redirect(up_settings.REGISTRATION_REDIRECT)
                url = reverse('users:userprofiles_registration_complete')
                return HttpResponseRedirect(url)

        registration = RegistrationView.as_view()


as_view()
-----------
Возвращает выполняемое(callable) представление, которое принимает запрос(request) и возвращает ответ(response):


        registration = RegistrationView.as_view()


userprofiles/urls.py
---------------------

        # -*- coding: utf-8 -*-
        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
           ]

urls.py
--------

        urlpatterns = [
            
            url(r'^$', views.home, name='main'),
            url(r'^shop/', include('shop.urls', namespace='shop')),
            url(r'^ckeditor/', include('ckeditor_uploader.urls')),
            url(r'^users/', include('userprofiles.urls', namespace="users")),
            url(r'^admin/', admin.site.urls),
        ]
        if settings.DEBUG:
            urlpatterns += static(settings.MEDIA_URL,
                                  document_root=settings.MEDIA_ROOT)


HttpResponseRedirect
-------------------------
Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'http://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
url
---
Этот атрибут, доступный только для чтения, содержит URL для редиректа (аналог заголовка Location).

        url = reverse('users:userprofiles_registration_complete')
        return HttpResponseRedirect(url)


userprofiles/views.py
------------------------

        class RegistrationCompleteView(TemplateView):
            template_name = 'userprofiles/registration_complete.html'

            def get_context_data(self, **kwargs):
                return {
                    'account_verification_active': False,
                    'expiration_days': 7,
                }
        registration_complete = RegistrationCompleteView.as_view()


userprofiles/registration_complete.html
--------------------------------------------

        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Register with Blog {% endblock %}

        {% block content %}
            <h1>Registration</h1>
            {% if account_verification_active %}
                <p>
                    Your registration was successful. We send you a e-mail including a link.<br />
                    Please click the link to activate your account. Thank you!<br />
                    <br />
                    The link is valid for {{ expiration_days }} days.
                </p>
            {% else %}
                <p>
                    Your registration was successful.
                </p>
            {% endif %}
        {% endblock %}


userprofiles/urls.py
---------------------

        # -*- coding: utf-8 -*-

        from django.conf.urls import url
        from . import views

        urlpatterns = [
            url(r'^register/$', views.RegistrationView.as_view(), name='userprofiles_registration'),
            url(r'^register/complete/$', views.RegistrationCompleteView.as_view(), name='userprofiles_registration_complete'),
           ]


utils.py
--------

        from django.core.exceptions import ImproperlyConfigured

        try:
            from importlib import import_module
        except ImportError:
            from django.utils.importlib import import_module

        def get_form_class(path):
            i = path.rfind('.')
            module, attr = path[:i], path[i + 1:]
            try:
                mod = import_module(module)
            # except ImportError, e: # python 2.7
            except ImportError as e: # python 3.4
                raise ImproperlyConfigured( 'Error loading module %s: "%s"' % (module, e))
            try:
                form = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a form named "%s"' % (module, attr))
            return form

base.html
---------
        {% include 'includes/header.html'%}
        {% include 'includes/mainmenu.html'%}
             <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        {% include 'includes/footer.html'%}
         
header.html
-----------

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
                <!--[if lt IE 8]>
                    <p class="browserupgrade">You are using an <strong>outdated</strong> browser. Please <a href="http://browsehappy.com/">upgrade your browser</a> to improve your experience.</p>
                <![endif]-->
            </head>
            <body>

footer.html
-----------
        {% load staticfiles %}
              <hr>

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


mainmenu.html
-------------
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
                  <ul class="nav  navbar-nav navbar-right">
                    {% if user.is_authenticated %}
                    <li><a href="{% url 'users:logout' %}">Logout</a></li>
                    <li><a href="{% url 'users:profile' slug=user.username %}">{{ user.username }}</a></li>
                    {% else %}
                    <li><a href="{% url 'users:userprofiles_registration' %}">Register</a></li>
                    <li><a href="{% url 'users:login' %}">Login</a></li>
                  {% endif %}
                 </ul>
                </div><!--/.navbar-collapse -->
              </div>
            </nav>