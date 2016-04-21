# tdd-django unit_11

Использование системы аутентификации пользователя
=================================================
Django предоставляет возможности аутентификации и авторизации пользователей, обычно этот механизм называют системой аутентификации, т.к. эти функции связаны.

Объект пользователя
===================
Объекты User - основа системы аутентификации. Они представляют пользователей сайта и используются для проверки прав доступа, регистрации пользователей, ассоциации данных с пользователями. Для представления пользователей в системе аутентификации используется только один класс, таким образом 'суперпользователи' или 'персонал' - это такие же объекты пользователей, просто с определёнными атрибутами.

Основные атрибуты пользователя:
==============================
- username
- password
- email
- first_name
- last_name
- groups
- user_permissions
- is_staff
- is_active
- is_superuser
- last_login
- date_joined

Смена пароля
-------------
Django не хранит пароль в открытом виде, хранится только хеш. Поэтому не советуем менять пароль напрямую. Именно по этой причине пользователь создается через специальную функцию.

Пароль можно сменить несколькими способами:

Команда manage.py changepassword *username* позволяет сменить пароль пользователя через консоль. Команда требует ввести пароль дважды. Если введённые значения совпадают, то пароль будет изменен. Если не указать имя пользователя, команда попробует найти пользователя с именем текущего системного пользователя.

Вы можете изменить пароль программно, используя метод set_password():

        >>> from django.contrib.auth.models import User
        >>> u = User.objects.get(username='john')
        >>> u.set_password('new password')
        >>> u.save()

Если вы используете интерфейс администратора Django, вы можете изменить пароль, используя админку.

Django также предоставляет представления и формы, которые можно использовать при создании страниц для смены пароля пользователем.

При смене пароля будут завершены все сессии пользователя, если вы используете SessionAuthenticationMiddleware.

Аутентификация пользователей
============================
    authenticate(**credentials)
Для аутентификации пользователя по имени и паролю используйте authenticate(). Параметры авторизации передаются как именованные аргументы, по умолчанию это username и password, если пароль и имя пользователя верны, будет возвращен объект User. Если пароль не правильный, authenticate() возвращает None. Например:

        from django.contrib.auth import authenticate
        user = authenticate(username='john', password='secret')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

Это низкоуровневый API для аутентификации; например, он используется в RemoteUserMiddleware. Если вы не пишете свою систему авторизации, скорее всего вам не понадобится его использовать. Если вам нужно будет ограничить доступ только авторизованным пользователям, используйте декоратор login_required().
Права доступа и авторизация
----------------------------
Django предоставляет простую систему проверки прав. Она позволяет добавлять права пользователю или группе пользователей.

Эта система используется админкой Django, но вы можете использовать её и в своем коде.

Админка использует проверку прав следующим образом:
---------------------------------------------------
- При доступе к странице добавления объекта проверяется наличие права “add” для объектов этого типа.

- При доступе к страницам просмотра списка объектов и изменения объекта проверяется наличие права “change” для объектов этого типа.

- При удалении объекта проверяется наличие права “delete” для объектов этого типа.

Права доступа можно добавлять не только типу объекта, но и конкретному объекту. Переопределив методы has_add_permission(), has_change_permission() и has_delete_permission() класса ModelAdmin, можно проверять права для конкретного объекта.

Модель User содержит связи многое ко многим с таблицами groups и user_permissions. Объект модели User работает со связанными моделями, как и другие модели Django:

        myuser.groups = [group_list]
        myuser.groups.add(group, group, ...)
        myuser.groups.remove(group, group, ...)
        myuser.groups.clear()
        myuser.user_permissions = [permission_list]
        myuser.user_permissions.add(permission, permission, ...)
        myuser.user_permissions.remove(permission, permission, ...)
        myuser.user_permissions.clear()
Права доступа по умолчанию
---------------------------
Если добавить приложение django.contrib.auth в параметр конфигурации INSTALLED_APPS, оно добавит права доступа по умолчанию – “add”, “change” и “delete” – для каждой модели из установленных приложений.

Эти права доступа создаются при выполнении команды manage.py migrate. При первом выполнении migrate, после добавления django.contrib.auth в INSTALLED_APPS, права доступа по умолчанию создаются для всех старых и новых моделей. Впоследствии команда назначает стандартные права на новые модели при каждом запуске manage.py migrate (функция, которая создаёт права, подключена к сигналу post_migrate).

Предположим у вас есть приложение с app_label foo и модель Bar. Чтобы проверить права доступа, используйте:

        add: user.has_perm('foo.add_bar')
        change: user.has_perm('foo.change_bar')
        delete: user.has_perm('foo.delete_bar')
Модель Permission редко используется напрямую.

Группы
=======
Модель django.contrib.auth.models.Group предоставляет возможность группировать пользователей, добавляя им набор прав доступа. Пользователь может принадлежать нескольким группам.

Пользователь, добавленный в группу, автоматически получает все права доступа этой группы. Например, если группа Site editors содержит права доступа can_edit_home_page, любой пользователь в этой группе получить это право доступа.

Также группы позволяют группировать пользователей, добавляя метки или дополнительные возможности. Например, вы можете создать группу 'Special users', и написать код, который предоставляет доступ к дополнительному функционалу сайта, или отправлять сообщения только пользователям этой группы.

Программное создание прав доступа
---------------------------------
Кроме добавления своих прав доступа через класс Meta модели, вы также можете создать их напрямую. Например, создадим право доступа can_publish для модели BlogPost в приложении myapp:

        from myapp.models import BlogPost
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(BlogPost)
        permission = Permission.objects.create(codename='can_publish',
                                               name='Can Publish Posts',
                                               content_type=content_type)
Теперь его можно добавить объекту User через атрибут user_permissions или к объекту Group через атрибут permissions.

Кеширование прав доступа
------------------------
ModelBackend кэширует права доступа объекта User после первого запроса на их получение. Такой подход удобен для цикла запрос-ответ, т.к. права доступа редко проверяются сразу же после их изменения (например, в админке). Если вы изменяете и проверяете права доступа в одном запросе или в тестах, проще всего заново загрузить объект User из базы данных. Например:

        from django.contrib.auth.models import Permission, User
        from django.shortcuts import get_object_or_404

        def user_gains_perms(request, user_id):
            user = get_object_or_404(User, pk=user_id)
            # any permission check will cache the current set of permissions
            user.has_perm('myapp.change_bar')

            permission = Permission.objects.get(codename='change_bar')
            user.user_permissions.add(permission)

            # Checking the cached permission set
            user.has_perm('myapp.change_bar')  # False

            # Request new instance of User
            user = get_object_or_404(User, pk=user_id)

            # Permission cache is repopulated from the database
            user.has_perm('myapp.change_bar')  # True

Аутентификация в запросах
-------------------------
Django использует сессию и промежуточный слой для работы системы аутентификации в объекте запроса.

Этот механизм предоставляет атрибут request.user для каждого запроса, который возвращает текущего пользователя. Если текущий пользователь не авторизован, атрибут содержит экземпляр AnonymousUser, иначе экземпляр User.

Различить их можно с помощью метода is_authenticated():

        if request.user.is_authenticated():
            # Do something for authenticated users.
            ...
        else:
            # Do something for anonymous users.
            ...
Как авторизовать пользователя
-----------------------------
Если вы ходите привязать к сессии авторизованного пользователя, используйте функцию login().

        login(request, user)

Чтобы авторизовать пользователя в представлении, используйте функцию login(). Она принимает объект HttpRequest и объект User. Функция login() сохраняет идентификатор пользователя в сессии, используя Django приложение для работы с сессиями.

Следует отметить, что любые данные установленные в анонимной сессии будут сохранены в сессии пользователя после его авторизации.

пример показывает как использовать обе функции authenticate() и login():

        from django.contrib.auth import authenticate, login

        def my_view(request):
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to a success page.
                else:
                    # Return a 'disabled account' error message
                    ...
            else:
                # Return an 'invalid login' error message.
                ...
Сначала вызывайте authenticate()
---------------------------------
Когда вы самостоятельно авторизуете пользователя, вы должны успешно выполнить его аутентификацию с помощью функции authenticate() перед вызовом функции login(). Функция authenticate() устанавливает атрибут у класса User, указывающий бэкенд относительно которого был успешно аутентифицирован данный пользователь (обратитесь к документации на бэкенды для подробностей), эта информация понадобится позже для процесса авторизации. При попытке авторизации объекта пользователя, который был получен из базы напрямую, будет выброшена ошибка.
Как отменить авторизацию пользователя
-------------------------------------
        logout(request)
Для отмены авторизации пользователя, который был авторизован с помощью функции django.contrib.auth.login(), следует использовать функцию django.contrib.auth.logout() в коде вашего представления. Функция принимает объект HttpRequest и не возвращает никаких значений. Например:

        from django.contrib.auth import logout

        def logout_view(request):
            logout(request)
            # Redirect to a success page.

функция logout() не выбрасывает никаких ошибок, если пользователь не был ранее авторизован.

При вызове функции logout() в рамках текущего запроса будут очищены все данные сессии. Все существующие данные будут стёрты. Это происходит для того, чтобы предотвратить возможность доступа к этим данным для другого пользователя, который будет использовать тот же браузер для своей авторизации. Если потребуется поместить некие данные в сессию, которые должны быть доступны пользователя сразу после отмены его авторизации, выполняйте это после вызова функции django.contrib.auth.logout().

Ограничение доступа для неавторизованных пользователей
------------------------------------------------------

Самым простым способом ограничить доступ к страницам является использование метода request.user.is_authenticated() и, при необходимости, перенаправление на страницу авторизации:

        from django.conf import settings
        from django.shortcuts import redirect

        def my_view(request):
            if not request.user.is_authenticated():
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            # ...

или отображение сообщения об ошибке:

        from django.shortcuts import render

        def my_view(request):
            if not request.user.is_authenticated():
                return render(request, 'myapp/login_error.html')
            # ...
Декоратор login_required
------------------------
        login_required(redirect_field_name='next', login_url=None)
Для краткости кода вы можете использовать декоратор login_required():

        from django.contrib.auth.decorators import login_required

        @login_required
        def my_view(request):
            ...
Функция login_required() делает следующее:
------------------------------------------
Если пользователь не авторизован, то перенаправляет его на URL, указанный в параметре конфигурации settings.LOGIN_URL, передавая текущий абсолютный путь в запросе. Например: /accounts/login/?next=/polls/3/.

Если пользователь авторизован, то выполняет код представления. В коде представления не требуется выполнять проверку авторизован ли пользователь или нет.

По умолчанию, в параметре "next" строки запроса хранится путь, по которому должен быть перенаправлен пользователь в результате успешной аутентификации. Если вам потребуется использовать другое имя для этого параметра, то воспользуйтесь необязательным аргументом redirect_field_name декоратора login_required():

        from django.contrib.auth.decorators import login_required

        @login_required(redirect_field_name='my_redirect_field')
        def my_view(request):
            ...

если вы воспользуетесь аргументом redirect_field_name, то вам скорее всего потребуется внести изменения в ваш шаблон авторизации, так как переменная контекста шаблона, которая содержит путь перенаправления, будет использовать значение аргумента redirect_field_name в качестве своего ключа, а не стандартное значение "next".

Декоратор login_required() также принимает необязательный аргумент login_url. Например:

        from django.contrib.auth.decorators import login_required

        @login_required(login_url='/accounts/login/')
        def my_view(request):
            ...
если вы не укажите аргумент login_url, то вам потребуется проверить параметр конфигурации settings.LOGIN_URL и ваше представление для авторизации соответственно настроены. Например, пользуясь стандартным поведением, добавьте следующие строки к вашей схеме URL:

        from django.contrib.auth import views as auth_views

        url(r'^accounts/login/$', auth_views.login),
Параметр конфигурации settings.LOGIN_URL также принимает имена представлений и именованные шаблоны URL. Это позволяет вам свободно переносить ваше представление для авторизации пользователя внутри схемы URL без необходимости изменения настроек.

Декоратор login_required() не проверяет свойство is_active объекта пользователя.

Если вы создаёте собственные представления для интерфейса администратора (или вам нужна та же аутентификация, что используются встроенными представлениями), то вам может пригодиться декоратор django.contrib.admin.views.decorators.staff_member_required() в качестве полезной альтернативы login_required().
Примесь LoginRequired
---------------------
При использовании CBV представлений, вы можете получить поведение аналогичное login_required, используя примесь LoginRequiredMixin. Эта примесь должна быть указана в самом начале списка наследования.

class LoginRequiredMixin
------------------------
Если представление использует эту примесь, все запросы от неаутентифицированных пользователей будут перенаправлены на страницу аутентификации или будет показана ошибка HTTP 403 Forbidden, это зависит от параметра raise_exception.

Вы можете установить любой из параметров AccessMixin для управления обработкой неаутентифицированных пользователей:

        from django.contrib.auth.mixins import LoginRequiredMixin

        class MyView(LoginRequiredMixin, View):
            login_url = '/login/'
            redirect_field_name = 'redirect_to'

Подобно декоратору login_required(), эта примесь не проверяет свойство is_active объекта пользователя.
Ограничение доступа для авторизованных пользователей с помощью дополнительной проверки
--------------------------------------------------------------------------------------

Самым простым способом будет выполнение вашей проверки над request.user прямо в представлении. Например, эта проверка в представлении проверяет, что пользователь имеет адрес электронной почты на требуемом домене и, если это не так, перенаправляет его на страницу авторизации:

        from django.shortcuts import redirect

        def my_view(request):
            if not request.user.email.endswith('@example.com'):
                return redirect('/login/?next=%s' % request.path)
            # ...
        user_passes_test(func, login_url=None, redirect_field_name='next')

Для удобства вы можете использовать декоратор user_passes_test, который выполняет перенаправление в случае, если проверяющая функция возвращает False:

        from django.contrib.auth.decorators import user_passes_test

        def email_check(user):
            return user.email.endswith('@example.com')

        @user_passes_test(email_check)
        def my_view(request):
            ...
Декоратор user_passes_test() принимает обязательный аргумент: функцию, которая принимает объект User и возвращает True, если пользователю разрешён доступ к просмотру страницы. Следует отметить, что декоратор user_passes_test() не выполняет автоматически проверку, что User прошёл авторизацию.

Декоратор user_passes_test() принимает для необязательных аргумента:

login_url
---------
Позволяет определеть URL на который будут перенаправляться пользователя, которые нее смогут пройти проверку. Это может быть страница авторизации или по умолчанию это будет значение параметра конфигурации settings.LOGIN_URL, если вы не указали никакого значения.

redirect_field_name
-------------------
Аналогично декоратору login_required(). Присвоение значения None удаляет соответствующее поле из URL, что может вам потребоваться при перенаправлении пользователей, которые не прошли проверку, на страницу отличную от страницы авторизации.

Например:

        @user_passes_test(email_check, login_url='/login/')
        def my_view(request):
            ...

class UserPassesTestMixin

При использовании CBV представлений, вы можете для этой цели применять UserPassesTestMixin.

test_func()
-----------
Вы можете переопределить метод test_func() класса для того, чтобы указать тест, который будет выполнен. Далее, вы можете указать любой параметр AccessMixin для настройки обработки неаутентифицированных пользователей:

        from django.contrib.auth.mixins import UserPassesTestMixin

        class MyView(UserPassesTestMixin, View):

            def test_func(self):
                return self.request.user.email.endswith('@example.com')
get_test_func()
---------------
Вы также можете переопределить метод get_test_func(), чтобы заставить примесь использовать по-другому именованную функцию для выполнения проверки (вместо test_func()).

Цепочка из UserPassesTestMixin
------------------------------
Из-за особенностей реализации UserPassesTestMixin, вы не можете выстроить цепочку наследования. Следующий пример не работает:

        class TestMixin1(UserPassesTestMixin):
            def test_func(self):
                return self.request.user.email.endswith('@example.com')

        class TestMixin2(UserPassesTestMixin):
            def test_func(self):
                return self.request.user.username.startswith('django')

        class MyView(TestMixin1, TestMixin2, View):
            ...
Если TestMixin1 вызовет super() и примет результат в работу, то TestMixin1 не будет больше работать в одиночку.
Декоратор permission_required
-----------------------------
        permission_required(perm, login_url=None, raise_exception=False)
Довольно частой задачей является проверка наличия определённого права у пользователя. Для решения этой задачи Django предоставляет удобный декоратор permission_required():

        from django.contrib.auth.decorators import permission_required

        @permission_required('polls.can_vote')
        def my_view(request):
            ...

Декоратор также может принимать перечисление прав, в этом случае пользователь должен обладать всеми правами для того, чтобы получить доступ к представлению.

декоратор permission_required() также принимает необязательный аргумент login_url:

        from django.contrib.auth.decorators import permission_required

        @permission_required('polls.can_vote', login_url='/loginpage/')
        def my_view(request):
            ...
Аналогично декоратору login_required() , по умолчанию значение для аргумента login_url соответствует значению параметра конфигурации settings.LOGIN_URL.

Если определён аргумент raise_exception, то декоратор будет выбрасывать исключение PermissionDenied с описанием 403 (HTTP Forbidden) представление вместо перенаправления на страницу авторизации.

Если вам надо использовать raise_exception, но также предоставить пользователям шанс сначала аутентифицироваться, вы можете использовать декоратор login_required():

        from django.contrib.auth.decorators import login_required, permission_required

        @permission_required('polls.can_vote', raise_exception=True)
        @login_required
        def my_view(request):
            ...

Примесь PermissionRequiredMixin
--------------------------------
Для того, чтобы выполнить проверки для CBV представлений, вы можете использовать PermissionRequiredMixin:

        class PermissionRequiredMixin

Эта примесь, подобно декоратору permisison_required, проверяет, есть ли у пользователя, который пытается получить доступ к представлению, все необходимые права. Вы можете указать право (или перечисление прав) с помощью параметра permission_required:

        from django.contrib.auth.mixins import PermissionRequiredMixin

        class MyView(PermissionRequiredMixin, View):
            permission_required = 'polls.can_vote'
            # Or multiple of permissions:
            permission_required = ('polls.can_open', 'polls.can_edit')
Вы можете установить любые параметры AccessMixin для изменения обработки неаутентифированных пользователей.

Вы также можете переопределить эти методы:

get_permission_required()
-------------------------
Возвращает перечисления имён прав, используемых примесью. По умолчанию, это содержимое атрибута permission_required, при необходимости преобразованное в кортеж.

has_permission()
----------------
Возвращает булево значение, есть ли у текущего пользователя право выполнить декорированное представление. По умолчанию, возвращается результат вызова метода has_perms() со списком прав, полученных от метода get_permission_required().

Перенаправление неаутентифицированных запросов в CBV представлениях
-------------------------------------------------------------------
Дл упрощения обработки правил доступа в CBV представлениях, примесь AccessMixin может быть использовано для перенаправления пользователя на страницу аутентификации или выбросить ошибку HTTP 403 Forbidden.

class AccessMixin
-----------------
login_url
---------
Стандартное значение для get_login_url(). По умолчанию, None, в этом случае метод get_login_url() возвратит settings.LOGIN_URL.

permission_denied_message
-------------------------
Стандартное значение для get_permission_denied_message(). По умолчанию, пустая строка.

redirect_field_name
--------------------
Стандартное значение для get_redirect_field_name(). По умолчанию, "next".

raise_exception
---------------
Если этот атрибут установлен в True, то вместо перенаправления будет выброшено исключение PermissionDenied. По умолчанию, False.

get_login_url()
---------------
Возвращает URL, на который будут перенаправляться пользователи не прошедшие тест. Возвращает значение атрибута login_url, если оно определено, или settings.LOGIN_URL.

get_permission_denied_message()
-------------------------------
При raise_exception равном True, этот метод может быть использован для управления сообщением об ошибке, которое будет передано в обработчик для отображения пользователю. По умолчанию, возврашает значение атрибута permission_denied_message.

get_redirect_field_name()
-------------------------
Возвращает имя параметра запроса, содержащий URL, на который должен быть перенаправлен пользователь в случае успешной авторизации. Если вы установите его в None, то параметр запроса не будет добавлен. По умолчанию, возвращает значение атрибута redirect_field_name.

handle_no_permission()
----------------------
В зависимости от значения raise_exception, метод либо выбрасывает исключение PermissionDenied или перенаправляет пользователя на login_url, необязательно используя redirect_field_name, если оно установлено.

Сброс сессии при изменении пароля
---------------------------------
Данная защитная мера применяется только в случае, если активировано SessionAuthenticationMiddleware в параметре конфигурации MIDDLEWARE_CLASSES. Оно активировано, если файл settings.py был сгенерирован с помощью команды startproject на Django ≥ 1.7.

Проверка сессии станет обязательной в Django 1.10 вне зависимости от того, активировано ли SessionAuthenticationMiddleware. Если вы работаете над проектом до Django 1.7 или он был сгенерирован с помощью шаблона, который не включает SessionAuthenticationMiddleware, рассмотрите вариант активации этой возможности прежде чем продолжить чтение соглашений по обновлению.
Если ваша AUTH_USER_MODEL унаследована от класса AbstractBaseUser или реализует свой собственный метод get_session_auth_hash(), то аутентифицированные сессии будут содержать хэш, возвращённый этим методом. В случае AbstractBaseUser, это будет HMAC от поля с паролем. Если активирован SessionAuthenticationMiddleware, Django проверяет, что хеш, отправленный с каждым запросом, совпадает с хешом, вычисленным на стороне сервера. Это позволяет пользователю отключиться от всех его сессий с помощью изменения их пароля.

Стандартные представления для изменения пароля, поставляемые с Django, функция django.contrib.auth.views.password_change() и представление user_change_password в пакете django.contrib.auth, обновляют в сессии хэш пароля так, чтобы соответствующий пользователь не терял авторизацию. Если вы реализуете собственное представление для изменения пароля и желаете сохранить такое поведение, используйте эту функцию:

update_session_auth_hash(request, user)
---------------------------------------
Данная функция принимает текущий запрос и обновлённый объект пользователя из которого будет извлечён новый хэш сессии и соответственно обновляет хэш сессии. Пример использования:

        from django.contrib.auth import update_session_auth_hash

        def password_change(request):
            if request.method == 'POST':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
            else:
                ...
Если вы обновляете существующий сайт и требуется активировать SessionAuthenticationMiddleware без необходимости повторной авторизации всех ваших пользователей, вам сначала следует обновиться до Django 1.7 и подождать некоторое время, чтобы сессии были пересозданы естественным образом по мере авторизации пользователей, сессии будут содержать хэш, описанный ранее. Для всех пользователи, которые не были авторизованы и для которых были обновлены сессии с помощью проверочного хэша, будет сброшена текущая сессия и им потребуется выполнить повторную авторизацию.

Так как метод get_session_auth_hash() использует параметр конфигурации SECRET_KEY, то обновление этого параметра приведёт к отмене всех существующих сессий на сайте.
Представления аутентификации
----------------------------
Django предоставляет несколько представлений, с помощью которых вы можете осуществлять управление авторизацией пользователей и их паролями. Представления используют ряд соответствующих форм, но вы можете передавать и свои формы.

Django не предоставляет стандартного шаблона для представлений аутентификации. Вы должны создать свой собственный шаблон для представлений, которые планируете использовать. 

Использование представлений
---------------------------
Существует несколько разных методов для реализации данных представлений в вашем проекте. Самым простым способом будет подключение схемы URL из django.contrib.auth.urls в вашу схему, например:

        urlpatterns = [
            url('^', include('django.contrib.auth.urls'))
        ]
добавить следующие шаблоны URL:

        ^login/$ [name='login']
        ^logout/$ [name='logout']
        ^password_change/$ [name='password_change']
        ^password_change/done/$ [name='password_change_done']
        ^password_reset/$ [name='password_reset']
        ^password_reset/done/$ [name='password_reset_done']
        ^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
        ^reset/done/$ [name='password_reset_complete']
Представления добавляют имя для URL для упрощения ссылок на них. 

Если вам требуется больше контроля над вашими URL, вы можете указывать специальное представление в вашей схеме URL:

        from django.contrib.auth import views as auth_views

        urlpatterns = [
            url('^change-password/', auth_views.password_change)
        ]
Представления принимают необязательные аргументы, которые вы можете использовать для изменения их поведения. Например, если требуется изменить имя шаблона, который будет использоваться представлением, вы можете указать аргумент template_name. Для этого надо указать именованные аргументы в схеме URL и они будут переданы в представление. Например:

        urlpatterns = [
            url(
                '^change-password/',
                auth_views.password_change,
                {'template_name': 'change-password.html'}
            )
        ]
Все представления возвращают экземпляр TemplateResponse, который позволяет легко изменять содержимое отклика перед его рендеринг7ом. Для этого следует обернуть представление внутри вашего собственного представления:

        from django.contrib.auth import views

        def change_password(request):
            template_response = views.password_change(request)
            # Do something with `template_response`
            return template_response

Все представления для аутентификации
------------------------------------

        login(request, template_name=`registration/login.html`, redirect_field_name=, authentication_form, current_app, extra_context)


Необязательные аргументы:

- template_name: Путь до шаблона, который будет использовать представление при авторизации пользователя. По умолчанию, registration/login.html.

- redirect_field_name: Имя GET поля, содержащего URL на который будет произведёно перенаправление после успешной авторизации. По умолчанию, next.

- authentication_form: Вызываемый объект (обычно, просто класс формы), использующийся для аутентификации. По умолчанию, AuthenticationForm.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

Вот, что делает представление django.contrib.auth.views.login:

- При вызове через GET, оно отображает форму для аутентификации, которая отправляет введённые данные через POST на тот же URL. 

- При вызове через POST с аутентификационными данными пользователя, оно пытается авторизовать пользователя. При успешной авторизации, представление перенаправляет на URL, указанный в next. Если параметр next не был предоставлен, происходит перенаправление на URL, содержащийся в параметре конфигурации settings.LOGIN_REDIRECT_URL (по умолчанию, /accounts/profile/). При невозможности авторизации, представление снова показывает форму.

Вашей обязанностью является предоставление HTML кода для шаблона, который по умолчанию называется registration/login.html. Данный шаблон принимает через контекст четыре переменных:

- form: Объект Form, который представляет AuthenticationForm.

- next: URL, на который будет осуществлено перенаправление после успешной авторизации. Можно также передавать строку запроса.

- site: Текущий Site, соответствующий параметру конфигурации SITE_ID. Если вы не активировали соответствующее приложение, переменной будет присвоен экземпляр RequestSite, который получает имя сайта и домен из текущего HttpRequest.

- site_name: Псевдоним для site.name. Если вы не активировали соответствующее приложение, переменной будет присвоено значение request.META['SERVER_NAME']. Для подробностей о работе с сайтами обратитесь к Фреймворк для сайтов.

Если потребуется отказаться от вызова шаблона registration/login.html, вы можете передать в представление параметр template_name через дополнительные аргументы URL с вашей схеме. Например, эта строка URL будет использовать шаблон myapp/login.html:

        url(r'^accounts/login/$', auth_views.login, {'template_name': 'myapp/login.html'}),
Вы также можете указать имя для GET поля, которое будет содержать URL для перенаправления после успешной авторизации пользователя, передав его в аргументе redirect_field_name в представление. По умолчанию, next.

Здесь показан пример содержимого шаблона registration/login.html, который вы можете использовать в качестве отправной точки. Он предполагает, что у вас есть шаблон base.html, который определяет блок content:

        {% extends "base.html" %}

        {% block content %}

        {% if form.errors %}
        <p>Your username and password didn't match. Please try again.</p>
        {% endif %}

        {% if next %}
            {% if user.is_authenticated %}
            <p>Your account doesn't have access to this page. To proceed,
            please login with an account that has access.</p>
            {% else %}
            <p>Please login to see this page.</p>
            {% endif %}
        {% endif %}

        <form method="post" action="{% url 'django.contrib.auth.views.login' %}">
        {% csrf_token %}
        <table>
        <tr>
            <td>{{ form.username.label_tag }}</td>
            <td>{{ form.username }}</td>
        </tr>
        <tr>
            <td>{{ form.password.label_tag }}</td>
            <td>{{ form.password }}</td>
        </tr>
        </table>

        <input type="submit" value="login" />
        <input type="hidden" name="next" value="{{ next }}" />
        </form>

        {# Assumes you setup the password_reset view in your URLconf #}
        <p><a href="{% url 'password_reset' %}">Lost password?</a></p>

        {% endblock %}
Если у вас реализован собственный механизм аутентификации (обратитесь к Собственная аутентификация) вы можете передать свою форму аутентификации в представление через параметр authentication_form. Данная форма должна принимать именованный аргумент request в её методе __init__ и предоставлять метод get_user, который должен возвращать объект аутентифицированного пользователя (метод будет вызываться только после успешной аутентификации).

Отмена авторизации пользователя.
---------------------------------
        logout(request, next_page=None, template_name='registration/logged_out.html', redirect_field_name='next', current_app=None, extra_context=None)

Необязательные аргументы:

- next_page: URL, на который будет осуществлено перенаправление.

- template_name: Путь до шаблона, который будет использовать представление при прекращении авторизации пользователя. По умолчанию, registration/logged_out.html.

- redirect_field_name: Имя GET поля, содержащего URL на который будет произведёно перенаправление после отмены авторизации. По умолчанию, next. Переопределяет next_page, если данный параметр был передан в GET.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.


Контекст шаблона:
-----------------
- title: Локализованная строка “Logged out”.

- site: Текущий Site, соответствующий параметру конфигурации SITE_ID. Если вы не активировали соответствующее приложение, переменной будет присвоен экземпляр RequestSite, который получает имя сайта и домен из текущего HttpRequest.

- site_name: Псевдоним для site.name. Если вы не активировали соответствующее приложение, переменной будет присвоено значение request.META['SERVER_NAME']. Для подробностей о работе с сайтами обратитесь к Фреймворк для сайтов.

- current_app: Подсказка, указывающая на приложение к которому принадлежит текущее представление. Обратитесь к стратегии разрешения URL пространства имён для получения подробностей.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

- logout_then_login(request, login_url=None, current_app=None, extra_context=None)
Отменяет авторизацию пользователя, затем перенаправляет на страницу авторизации.

Имя URL: Значения по умолчанию нет

Необязательные аргументы:

- login_url: URL страницы авторизации, на которую будет выполнено перенаправление. По умолчанию, settings.LOGIN_URL.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

- password_change(request, template_name='registration/password_change_form.html', post_change_redirect=None, password_change_form=PasswordChangeForm, current_app=None, extra_context=None)
Позволяет пользователю изменить его пароль.

Имя URL: password_change

Необязательные аргументы:

- template_name: Путь до шаблона, который будет использовать представление при изменении пароля. По умолчанию, registration/password_change_form.html.

- post_change_redirect: URL, на который будет производится перенаправление после успешного изменения пароля.

- password_change_form: Собственная форма для изменения пароля, которая должна принимать именованный аргумент user. Форма должна вызывать функцию для изменения пароля пользователя. По умолчанию, PasswordChangeForm.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.


Контекст шаблона:
-----------------
- form: Форма для изменения пароля (обратитесь к password_change_form выше).

- password_change_done(request, template_name='registration/password_change_done.html', current_app=None, extra_context=None)
Страница, отображаемая после того, как пользователь изменил свой пароль.

Имя URL: password_change_done

Необязательные аргументы:

- template_name: Путь до шаблона. По умолчанию, registration/password_change_done.html.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

password_reset(request, is_admin_site=False, template_name='registration/password_reset_form.html', email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt', password_reset_form=PasswordResetForm, token_generator=default_token_generator, post_reset_redirect=None, from_email=None, current_app=None, extra_context=None, html_email_template_name=None, extra_email_context=None)

Позволяет пользователю сбросить свой пароль, генерируя одноразовую ссылку, которая может быть использована для сброса пароля, и отправляя её на зарегистрированную электронную почто пользователя.

Если предоставленный адрес электронной почты не существует в системе, представление не будет выполнять отправку электронного сообщения, но и пользователь не получит никакого сообщения об ошибке. Это предотвращает утечку информации к потенциальным хацкерам. Если вам необходимо предоставлять сообщение об ошибке для этого случая, вы можете унаследовать форму PasswordResetForm и использовать аргумент password_reset_form.

Пользователь, отмеченный флагом отменённого пароля (см. set_unusable_password()), не может запросить сброс пароля. Так сделано, чтобы предотвратить неправильное использование при работе с внешними источниками аутентификации, например, с LDAP. Следует отметить, что они не получат никаких сообщений об ошибках, так как это вскрыло бы наличие аккаунта, и никакого сообщения на почту не будет отправлено.

Имя URL: password_reset

Необязательные аргументы:

- template_name: Путь до шаблона, который будет использоваться для отображения формы сброса пароля. По умолчанию, registration/password_reset_form.html.

- email_template_name: Путь до шаблона, который используется при генерации сообщения со ссылкой для сброса пароля, отправляемого на адрес электронной почты. По умолчанию, registration/password_reset_email.html.

- subject_template_name: Путь до шаблона, который используется при генерации заголовка сообщения со ссылкой для сброса пароля, отправляемого на адрес электронной почты. По умолчанию registration/password_reset_subject.txt.

- password_reset_form: Форма, которая будет использоваться для получения адреса электронной почты пользователя для сброса его пароля. По умолчанию, PasswordResetForm.

- token_generator: Экземпляр класса для проверки одноразовой ссылки. По умолчанию, default_token_generator, который является экземпляром django.contrib.auth.tokens.PasswordResetTokenGenerator.

- post_reset_redirect: URL, на который будет произведено перенаправление после успешного запроса на сброс пароля.

- from_email: Корректный адрес электронной почты. По умолчанию Django использует DEFAULT_FROM_EMAIL.

- current_app: Подсказка, указывающая на приложение к которому принадлежит текущее представление. Обратитесь к стратегии разрешения URL пространства имён для получения подробностей.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

- html_email_template_name: Путь до шаблона, который будет использоваться при генерации text/html блока электронного сообщения с ссылкой для сброса пароля. По умолчанию, сообщение в формате HTML не отправляется.

- extra_email_context: Словарь с контекстными данными, которые будут доступны в контексте шаблона сообщения.

Контекст шаблона:

    form: Форма (смотрите password_reset_form выше) для сброса пароля пользователя.

Контекст шаблона электронной почты:

email: Псевдоним для user.email

- user: Текущий User, соответствующий полю email формы. Толька активные пользователи имеют возможность сбрасывать свои пароли passwords (User.is_active is True).

- site_name: Псевдоним для site.name. Если вы не активировали соответствующее приложение, переменной будет присвоено значение request.META['SERVER_NAME']. Для подробностей о работе с сайтами обратитесь к Фреймворк для сайтов.

- domain: Псевдоним для site.domain. Если вы не используете приложение для работы с сайтами, то значением будет request.get_host().

- protocol: http или https

- uid: Первичный ключ пользователя, закодированный в base 64.

- token: Токен для проверки корректности ссылки для сброса пароля.

Пример registration/password_reset_email.html (шаблон тела письма):

        Someone asked for password reset for email {{ email }}. Follow the link below:
        {{ protocol}}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}
Такой же контекст используется для шаблона заголовка сообщения. Заголовок должен быть представлен одной строкой простого текста.

- password_reset_done(request, template_name='registration/password_reset_done.html', current_app=None, extra_context=None)
Эта страница отображается после отправки пользователю письма с ссылкой для сброса его пароля. Данное представление вызывается по умолчанию, если представлению password_reset() не было явно передан URL post_reset_redirect.

Имя URL: password_reset_done

Если предоставленный адрес электронной почты не существует в системе, пользователь не активирован или имеет деактивированный пароль, то пользователь будет перенаправляться на это представление, но никаких писем ему отправляться не будет.
Необязательные аргументы:

- template_name: Путь до шаблона. По умолчанию, registration/password_reset_done.html.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

- password_reset_confirm(request, uidb64=None, token=None, template_name='registration/password_reset_confirm.html', token_generator=default_token_generator, set_password_form=SetPasswordForm, post_reset_redirect=None, current_app=None, extra_context=None)
Представляет форму для ввода нового пароля.

Имя URL: password_reset_confirm

Необязательные аргументы:

- uidb64: Идентификатор пользователя закодированный в base 64. По умолчанию, None.

- token: Токен для проверки корректности пароля. По умолчанию, None.

- template_name: Путь до шаблона, который использует представление для подтверждения пароля. По умолчанию, registration/password_reset_confirm.html.

- token_generator: Эеземпляр класса для проверки пароля. По умолчанию, default_token_generator, это экземпляр django.contrib.auth.tokens.PasswordResetTokenGenerator.

- set_password_form: Форма, которая будет использоваться для установки пароля. По умолчанию, SetPasswordForm.

- post_reset_redirect: URL, на который будет произведено перенаправление после выполнения сброса пароля.По умолчанию, None.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

Контекст шаблона:

- form: Форма (см. set_password_form выше) для установки нового пароля для пользователя.

- validlink: Булево значение. True, если ссылка (комбинация uidb64 и token) корректна и не была ещё использована.

- password_reset_complete(request, template_name='registration/password_reset_complete.html', current_app=None, extra_context=None)
Представление, которое информирует пользователя об успешном изменении пароля.

Имя URL: password_reset_complete

Необязательные аргументы:

- template_name: Путь до шаблона. По умолчанию, registration/password_reset_complete.html.

- extra_context: Словарь с контекстными данными, которые будут добавлены в текущий контекст, перед его передачей в шаблон.

Вспомогательные функции
- redirect_to_login(next, login_url=None, redirect_field_name='next')
Перенаправляет на страницу аутентификации и, в случае её успешного прохождения, затем перебрасывает на другой URL.

Обязательные аргументы:

- next: URL на который происходит перенаправление после успешной авторизации.

Необязательные аргументы:

- login_url: URL страницы авторизации, на которую будет выполнено перенаправление. По умолчанию, settings.LOGIN_URL.

- redirect_field_name: Имя GET поля, содержащего URL на который будет произведёно перенаправление после отмены авторизации. Переопределяет next. если данный параметр был передан в GET.

Встроенные формы
================
Если вы не желаете использовать встроенные представления, но и формы переписывать не хотите, то система аутентификации предоставляет несколько встроенных форм, расположенных в django.contrib.auth.forms:

Встроенные формы делают некоторые предположения о модели пользователя, с которой они работают. Если вы используете собственную модель пользователя, может потребоваться определить собственные формы для системы аутентификации. 
class AdminPasswordChangeForm
-----------------------------
Форма, используемая в интерфейса администратора, для изменения пароля пользователя.

Принимает user в качестве первого неименованного параметра.

class AuthenticationForm
------------------------
Форма для аутентификации пользователя.

Принимает request в качестве первого неименованного аргумента, который сохраняется в экземпляре формы для использования подклассами.

confirm_login_allowed(user)
---------------------------
По умолчанию, форма AuthenticationForm игнорирует пользователей у которых флаг is_active установлен в False. Вы можете изменить это поведение на проверку некого права пройти аутентификацию для пользователей. Выполните это с помощью своей формы, которая унаследована от AuthenticationForm и переопределяет метод confirm_login_allowed(). Этот метод должен выбрасывать исключение ValidationError в случае, если указанный пользователь не может проходить аутентификацию.

Например, позволяем всем пользователям проходить аутентификацию, невзирая на их статус активности:

        from django.contrib.auth.forms import AuthenticationForm

        class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
            def confirm_login_allowed(self, user):
                pass
Или позволяем только некоторым активным пользователям проходить аутентификацию:

        class PickyAuthenticationForm(AuthenticationForm):
            def confirm_login_allowed(self, user):
                if not user.is_active:
                    raise forms.ValidationError(
                        _("This account is inactive."),
                        code='inactive',
                    )
                if user.username.startswith('b'):
                    raise forms.ValidationError(
                        _("Sorry, accounts starting with 'b' aren't welcome here."),
                        code='no_b_users',
                    )
class PasswordChangeForm
------------------------
Форма, через которую пользователь может менять свой пароль.

class PasswordResetForm
-----------------------
Форма для генерации и отправки одноразовой ссылки для сброса пользовательского пароля.

- send_email(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None)

Параметры:  
    subject_template_name – шаблон для заголовка.
    email_template_name – шаблон для тела письма.
    context – контекст передаётся в subject_template, email_template и html_email_template (если он не None).
    from_email – адрес электронной почты отправителя.
    to_email – адрес электронной почты пользователя.
    html_email_template_name – шаблон для HTML тела письма, по умолчанию, None, в этом случае отсылается обычный текст.
    По умолчанию, save() наполняет context теми же переменными, что и функция password_reset(), передавая их в контекст электронного сообщения.

class SetPasswordForm
----------------------
Форма, которая позволяет пользователю изменять свой пароль без ввода старого пароля.

class UserChangeForm
--------------------
Форма, используемая в интерфейсе администратора для изменения информации о пользователе и его списка прав.

class UserCreationForm
----------------------
Форма для создания нового пользователя.

Аутентификационные данные в шаблонах
------------------------------------
Авторизованный пользователь и его права доступны в шаблонном контексте при использовании RequestContext.

Техническая особенность
-----------------------
Технически, эти переменные становятся доступными в шаблонном контексте, только если вы используете RequestContext и активирован контекстный процессор 'django.contrib.auth.context_processors.auth'. По умолчанию проект так и настроен. 

Пользователи
============
При рендеринге RequestContext, авторизованный пользователь, неважно будет это экземпляр User или AnonymousUser, сохраняется в шаблонной переменной {{ user }}:

        {% if user.is_authenticated %}
            <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
        {% else %}
            <p>Welcome, new user. Please log in.</p>
        {% endif %}
Эта шаблонная переменная не доступна, если не используется RequestContext.

Права
=====
Права авторизованного пользователя хранятся в шаблонной переменной {{ perms }}. Она связана с экземпляром django.contrib.auth.context_processors.PermWrapper, который реализует доступ к правам.

В объекте {{ perms }} каждый атрибут — это “прокси” к методу User.has_module_perms. Этот пример отобразит True, если авторизованный пользователь любое право в приложении foo:

        {{ perms.foo }}
Каждый атрибут второго уровня — это “прокси” к User.has_perm. Этот пример отобразит True, если авторизованный пользователь имеет право foo.can_vote:

        {{ perms.foo.can_vote }}
Таким образом вы можете проверять права в шаблонном выражении {% if %}:

        {% if perms.foo %}
            <p>You have permission to do something in the foo app.</p>
            {% if perms.foo.can_vote %}
                <p>You can vote!</p>
            {% endif %}
            {% if perms.foo.can_drive %}
                <p>You can drive!</p>
            {% endif %}
        {% else %}
            <p>You don't have permission to do anything in the foo app.</p>
        {% endif %}
Также позможен поиск прав с помощью выражения {% if in %}. Например:

        {% if 'foo' in perms %}
            {% if 'foo.can_vote' in perms %}
                <p>In lookup works, too.</p>
            {% endif %}
        {% endif %}

Управление паролями в Django
============================

Как Django хранит пароли
-------------------------
Django предоставляет гибкую систему хранения паролей и по умолчанию использует PBKDF2.

Атрибут password объекта User является строкой следующего формата:

        <algorithm>$<iterations>$<salt>$<hash>

Данная строка показывает компоненты, которые используются для хранения пользовательского пароля и разделены знаком доллара, а именно: хэширующий алгоритм, количество итераций алгоритма (work factor), случайная соль и полученный хэш пароля. Алгоритмом может быть любой из ряда однонаправленных хэширующих алгоритмов, которые использует Django; см. далее. Итерации описывают количество применений алгоритма для получения хэша. Соль является случайными данным, а сам хэш получается в результате работы однонаправленной функции.

По умолчанию, Django использует алгоритм PBKDF2 с хэшем SHA256, механизм защиты паролей рекомендованный NIST. Этого должно хватить для большинства пользователей: достаточная защита, требующая большой объём вычислительного времени для взлома.

Тем не менее, в зависимости от ваших требований, вы можете выбрать другой алгоритм или даже реализовать собственный алгоритм, который будет соответствовать вашим требованиям к безопасности. Итак, большинство пользователей не должны думать об этом, если вы сомневаетесь, значит вам это точно не надою

Django выбирает алгоритм для использования в соответствии с указанием переменной конфигурации PASSWORD_HASHERS. Переменная содержит список классов реализующих алгоритмы хэширования, которые поддерживает Django. Первая запись этого списка (речь о settings.PASSWORD_HASHERS[0]) будет использоваться для сохранения паролей, а все остальные записи являются проверенными средствами, которые могут быть применены для проверки существующих паролей. Это означает, что вам потребуется использовать другой алгоритм хэширования, вам потребуется просто указать его первым в параметре конфигурации PASSWORD_HASHERS.

По умолчанию PASSWORD_HASHERS содержит:

        PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ]
Это означает, что Django будет использовать PBKDF2 для сохранения всех паролей, но будет поддерживать проверку паролей, сохранённых с помощью PBKDF2SHA1, bcrypt, SHA1 и так далее. 

Использование bcrypt с Django
-----------------------------
Bcrypt является популярным алгоритмом для хранения паролей, который специально разработан для хранения “долгих” паролей. Данный алгоритм не выбран в качестве стандартного в Django так как он требует использования внешних библиотек, но раз он используется многими, то Django поддерживает его, требуя минимальных усилий по его установке.

Для использования Bcrypt в качестве алгоритма по умолчанию, выполните следующие действия:

Установите bcrypt library. Это можно сделать с помощью команды pip install django[bcrypt] или скачайте библиотеку и установите её с помощью команды python setup.py install.

Измените PASSWORD_HASHERS так, чтобы BCryptSHA256PasswordHasher был указан первым. То есть, в файле конфигурации надо сделать так:

        PASSWORD_HASHERS = [
            'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ]

теперь Django по умолчанию будет использовать Bcrypt в качестве алгоритма хранения паролей.

Обрезание паролей с помощью BCryptPasswordHasher
------------------------------------------------
Разработчики алгоритма bcrypt обрезают все пароли до 72 символов, что означает bcrypt(password_with_100_chars) == bcrypt(password_with_100_chars[:72]). Оригинальный BCryptPasswordHasher не использует особую обработку и, следовательно, также имеет аналогичное ограничение на длину пароля. BCryptSHA256PasswordHasher исправляет это поведение, сначала хэшируя пароль с помощью sha256. Это действие предотвращает обрезание пароля, рекоментуем использовать эту реализацию вместо BCryptPasswordHasher. Причина применения такого обрезания проста, длина пароля обычного пользователя не превышает 72 символа и, даже будучи обрезанным до 72 символов, такой пароль всё равно требует значительных вычислительных ресурсов для его прямого подбора. Тем не менее, мы рекомендуем использовать BCryptSHA256PasswordHasher в любом случае по принципу “запас карман не тянет”.
Другие реализации bcrypt
-------------------------
Существует несколько других реализаций алгоритма, которые позволяют использовать bcrypt в Django. Django не поддерживает из из коробки. Для активации поддержки, вам потребуется привести хэши в вашей базе данных к виду bcrypt$(raw bcrypt output). Например:
        bcrypt$$2a$12$NT0I31Sa7ihGEWpka9ASYrEFkhuTNeBQ2xfZskIiiJeyFXhRgS.Sy.
Увеличение сложности хэша
-------------------------
Алгоритмы PBKDF2 и bcrypt используют ряд итераций или округлений для хэшей. Это значительно замедляют действия атакующих, усложняя выполнение атаки на хэшированные пароли. Однако, по мере увеличения вычислительной мощности, количество этих итераций следует увеличивать. Мы установили достаточное значение по умолчанию (и будем его увеличивать с каждым новым релизом Django), но вы можете пожелать увиличить или уменьшить это значение самостоятельно, в зависимости от вашей политики безопасности и вычислительной мощности, имеющейся в наличии. Чтобы сделать это, следует унаследоваться от класса нужного алгоритма и переопределить параметры iterations. Например, для увеличения количества итераций в алгоритме PBKDF2:

Унаследуйтесь от django.contrib.auth.hashers.PBKDF2PasswordHasher:

        from django.contrib.auth.hashers import PBKDF2PasswordHasher

        class MyPBKDF2PasswordHasher(PBKDF2PasswordHasher):
            """
            A subclass of PBKDF2PasswordHasher that uses 100 times more iterations.
            """
            iterations = PBKDF2PasswordHasher.iterations * 100
Сохраните это в ваш проект. Например, вы можете разместить это в файле подобном myproject/hashers.py.

Добавьте новый алгоритм хэширования в начало списка конфигурационного параметра PASSWORD_HASHERS:

        PASSWORD_HASHERS = [
            'myproject.hashers.MyPBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ]
теперь Django будет использовать большее количество итераций при сохранении паролей с помощью PBKDF2.

Обновление паролей
------------------
При аутентификации пользователей, если их пароли сохранены с помощью алгоритма, отличающегося от стандартного, то Django будет автоматически применять стандартный алгоритм хэширования. Это означает, что старые установки Django автоматически получат обновление в области аутентификации пользователей, и это также означает, что вы можете переключаться на новые (и более лучшие) алгоритмы хранения паролей по мере их изобретения.

Ручное управление паролями пользователей
-----------------------------------------
Модуль django.contrib.auth.hashers предоставляет набор функций для создания и проверки хэшированных паролей. Вы можете использовать эти функции независимо от модели User.

check_password(password, encoded)
---------------------------------
Если требуется вручную аутентифицировать пользователя с помощью сравнения открытого пароля с захэшированным паролем из базы данных, используйте вспомогательную функцию check_password(). Она принимает два аргумента: открытый пароль и полное значение поля password из базы данных, возвращает True при совпадении и False в противном случае.

make_password(password, salt=None, hasher='default')
----------------------------------------------------
Создаёт хэшированный пароль в формате, используемом этим приложением. Принимает один обязательный аргумент: открытый пароль. Опционально, если вам не надо использовать стандартные настройки (первая запись списка PASSWORD_HASHERS), вы можете указать “соль” и алгоритм, который следует использовать для хэширования, Сейчас поддерживаются следующие алгоритмы: 'pbkdf2_sha256', 'pbkdf2_sha1', 'bcrypt_sha256' (см. Использование bcrypt с Django), 'bcrypt', 'sha1', 'md5', 'unsalted_md5' (в целях обратной совместимости) и 'crypt', если соответствующая библиотека установлена в системе. Если аргумент с паролем содержит None, возвращается бесполезный пароль, который никогда не будет пропущен функцией check_password().

is_password_usable(encoded_password)
------------------------------------
Проверяет, является ли переданная строка хэшированным паролем, который имеет шанс пройти проверку с помощью функции check_password().

model

        @python_2_unicode_compatible
        class Profile(models.Model):
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

admin
        admin.site.register(Profile)

forms
        from django import forms
        from django.contrib.auth.models import User
        from .models import Profile

        class UserForm(forms.ModelForm):
            password = forms.CharField(widget=forms.PasswordInput())

            class Meta:
                model = User
                fields = ('username', 'email', 'password', 'first_name', 'last_name')

        class UserProfileForm(forms.ModelForm):
            class Meta:
                model = UserProfile
                exclude = ['user']
                #fields = '__all__'


views.py:
---------

        from blog.forms import UserForm, UserProfileForm

        def register(request):

            # A boolean value for telling the template whether the registration was successful.
            # Set to False initially. Code changes value to True when registration succeeds.
            registered = False

            # If it's a HTTP POST, we're interested in processing form data.
            if request.method == 'POST':
                # Attempt to grab information from the raw form information.
                # Note that we make use of both UserForm and UserProfileForm.
                user_form = UserForm(data=request.POST)
                profile_form = UserProfileForm(data=request.POST)

                # If the two forms are valid...
                if user_form.is_valid() and profile_form.is_valid():
                    # Save the user's form data to the database.
                    user = user_form.save()

                    # Now we hash the password with the set_password method.
                    # Once hashed, we can update the user object.
                    user.set_password(user.password)
                    user.save()

                    # Now sort out the UserProfile instance.
                    # Since we need to set the user attribute ourselves, we set commit=False.
                    # This delays saving the model until we're ready to avoid integrity problems.
                    profile = profile_form.save(commit=False)
                    profile.user = user

                    # Did the user provide a profile picture?
                    # If so, we need to get it from the input form and put it in the UserProfile model.
                    if 'profile_picture' in request.FILES:
                        profile.profile_picture = request.FILES['profile_picture']

                    # Now we save the UserProfile model instance.
                    profile.save()

                    # Update our variable to tell the template registration was successful.
                    registered = True

                # Invalid form or forms - mistakes or something else?
                # Print problems to the terminal.
                # They'll also be shown to the user.
                else:
                    print (user_form.errors, profile_form.errors)

            # Not a HTTP POST, so we render our form using two ModelForm instances.
            # These forms will be blank, ready for user input.
            else:
                user_form = UserForm()
                profile_form = UserProfileForm()

            # Render the template depending on the context.
            return render(request,
                    'profile/register.html',
                    {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

        def user_login(request):

            # If the request is a HTTP POST, try to pull out the relevant information.
            if request.method == 'POST':
                # Gather the email and password provided by the user.
                # This information is obtained from the login form.
                        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                        # because the request.POST.get('<variable>') returns None, if the value does not exist,
                        # while the request.POST['<variable>'] will raise key error exception
                username = request.POST.get('username')
                password = request.POST.get('password')

                # Use Django's machinery to attempt to see if the email/password
                # combination is valid - a User object is returned if it is.
                user = authenticate(username=username, password=password)

                # If we have a User object, the details are correct.
                # If None (Python's way of representing the absence of a value), no user
                # with matching credentials was found.
                if user:
                    # Is the account active? It could have been disabled.
                    if user.is_active:
                    # If the account is valid and active, we can log the user in.
                        # We'll send the user back to the homepage.
                        login(request, user)
                        return HttpResponseRedirect('/profile/')
                    else:
                        # An inactive account was used - no logging in!
                        return HttpResponse("Your Blog account is disabled.")
                else:
               # Bad login details were provided. So we can't log the user in.
                    print ("Invalid login details: {0}, {1}".format(username, password))
                    return HttpResponse("Invalid login details supplied.")

            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
            else:
                # No context variables to pass to the template system, hence the
                # blank dictionary object...
                # return render(request, 'profile/login.html', {})
                return render(request, 'profile/index.html', {})


        @login_required
        def restricted(request):
            return HttpResponse("Since you're logged in, you can see this text!")

        # Use the login_required() decorator to ensure only those logged in can access the view.

        @login_required
        def user_logout(request):
            # Since we know the user is logged in, we can now just log them out.
            logout(request)

            # Take the user back to the homepage.
            return HttpResponseRedirect('/profile/')


        from django.conf.urls import url

        from . import views

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
            url(r'^logout/$', views.user_logout, name='logout'),
        ]


Registration Template
======================

templates/profile/register.html:
------------------------------
        {% extends "base.html" %}
        {% block head_title %} {{ block.super }} - Register with Auth {% endblock %}

        {% block content %}
            <h2>Register with Janus Auth</h2>
            {% if registered %}
                Janus says: <strong>thank you for registering!</strong>
                <a href="/blog/">Return to the homepage.</a><br />
                {% else %}
                Janus says: <strong>register here!</strong><br />

                <form id="user_form" method="post" action="/profile/register/"
                        enctype="multipart/form-data">

                    {% csrf_token %}

                    <!-- Display each form. The as_p method wraps each element in a paragraph
                         (<p>) element. This ensures each element appears on a new line,
                         making everything look neater. -->
                    {{ user_form.as_p }}
                    {{ profile_form.as_p }}

                    <!-- Provide a button to click to submit the form. -->
                  <input type="submit" name="submit" value="Register" />
                </form>
                {% endif %}

        {% endblock %}


profile/views.py:
--------------

        from django.contrib.auth import authenticate, login

        from django.http import HttpResponseRedirect, HttpResponse

        def user_login(request):

            # If the request is a HTTP POST, try to pull out the relevant information.
            if request.method == 'POST':
                # Gather the username and password provided by the user.
                # This information is obtained from the login form.
                        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                        # because the request.POST.get('<variable>') returns None, if the value does not exist,
                        # while the request.POST['<variable>'] will raise key error exception
                username = request.POST.get('username')
                password = request.POST.get('password')

                # Use Django's machinery to attempt to see if the username/password
                # combination is valid - a User object is returned if it is.
                user = authenticate(username=username, password=password)

                # If we have a User object, the details are correct.
                # If None (Python's way of representing the absence of a value), no user
                # with matching credentials was found.
                if user:
                    # Is the account active? It could have been disabled.
                    if user.is_active:
                    # If the account is valid and active, we can log the user in.
                        # We'll send the user back to the homepage.
                        login(request, user)
                        return HttpResponseRedirect('/profile/')
                    else:
                        # An inactive account was used - no logging in!
                        return HttpResponse("Your Blog account is disabled.")
                else:
               # Bad login details were provided. So we can't log the user in.
                    print ("Invalid login details: {0}, {1}".format(username, password))
                    return HttpResponse("Invalid login details supplied.")

            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
            else:
                # No context variables to pass to the template system, hence the
                # blank dictionary object...
                return render(request, 'profile/index.html', {})
                # return render(request, 'profile/login.html', {})


Login Template
==============
templates/profile/login.html:
--------------------------

        <!DOCTYPE html>
        <html>
            <head>
                <!-- Is anyone getting tired of repeatedly entering the header over and over?? -->
                <title>profile</title>
            </head>

            <body>
                <h1>Login to profile</h1>

                <form id="login_form" method="post" action="/profile/login/">
                    {% csrf_token %}
                    Username: <input type="text" name="username" value="" size="50" />
                    <br />
                    Password: <input type="password" name="password" value="" size="50" />
                    <br />

                    <input type="submit" value="submit" />
                </form>

            </body>
        </html>


includes/mainmenu.html
----------------------

        <form class="navbar-form navbar-right" role="form" method="post" action="/profile/login/">
            {% csrf_token %}
            <div class="form-group">
              <input type="text" placeholder="Username" name="username" class="form-control">
            </div>
            <div class="form-group">
              <input type="password" placeholder="Password" name="password" class="form-control">
            </div>
            <button type="submit" class="btn btn-success">Sign in</button>
          </form>


Аутентификация пользователей
============================
Для аутентификации пользователя по имени и паролю используйте authenticate(). Параметры авторизации передаются как именованные аргументы, по умолчанию это username и password, если пароль и имя пользователя верны, будет возвращен объект User. Если пароль не правильный, authenticate() возвращает None.

        from django.contrib.auth import authenticate
        user = authenticate(username='john', password='secret')
        if user is not None:
            # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")

Если вам нужно будет ограничить доступ только авторизованным пользователям, используйте декоратор login_required().


{% if user.is_authenticated %}
===============================

        <h1>Janus says... hello {{ user.username }}!</h1>
        {% else %}
        <h1>Janus says... hello world!</h1>
        {% endif %}

Restricting Access
==================

views.py:
----------

        from django.contrib.auth.decorators import login_required

        @login_required
        def restricted(request):
            return HttpResponse("Since you're logged in, you can see this text!")

urls.py
--------

        urlpatterns = [

            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),

        ]

logout
======
views.py:
----------

        from django.contrib.auth import logout

        # Use the login_required() decorator to ensure only those logged in can access the view.
        @login_required
        def user_logout(request):
            # Since we know the user is logged in, we can now just log them out.
            logout(request)

            # Take the user back to the homepage.
            return HttpResponseRedirect('/')


urls.py:
-------------

        urlpatterns = [
            url(r'^register/$', views.register, name='register'),
            url(r'^login/$', views.user_login, name='login'), 
            url(r'^restricted/', views.restricted, name='restricted'),
            url(r'^logout/$', views.user_logout, name='logout'),

        ]


includes/mainmenu.html
-----------------------

            <div id="navbar" class="navbar-collapse collapse">

                 
                  <ul class="nav  navbar-nav navbar-right">
                    {% if user.is_authenticated %}
                    <li><a href="/profile/logout/">Logout</a></li>
                    {% else %}
                    <li><a href="/profile/register">Register</a></li>

                    <form class="navbar-form navbar-right" role="form" method="post" action="/profile/login/">
                    {% csrf_token %}
                    <div class="form-group">
                      <input type="text" placeholder="Username" name="username" class="form-control">
                    </div>
                    <div class="form-group">
                      <input type="password" placeholder="Password" name="password" class="form-control">
                    </div>
                    <button type="submit" class="btn btn-success">Sign in</button>
                  </form>
                  {% endif %}
                 </ul>
                  
                </div><!--/.navbar-collapse -->


