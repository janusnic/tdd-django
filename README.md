# tdd-django unit_18

Тестирование модели
===================
Selenium Web Driver (далее WD), входящий в Selenium 2.0, - это библиотека, эмулирующая браузер и позволяющая работать с элементами web-форм. В отличие от Selenium Server не требует предварительного запуска сервера, обрабатывающего команды Selenium.

ссылки:
-------
http://seleniumhq.org/docs/03_webdriver.html - официальная документация по WD;
http://selenium2.ru/docs/webdriver.html#webdriver - Selenium 2.0 и WebDriver, начало работы;
http://automated-testing.info - сайт, на котором много технических статей по использованию инструментов тестирования, в том числе Selenium WD.

Классы, их методы и свойства
============================
Основные импорты:
----------------
    from selenium import webdriver # работа с браузером
    from selenium.webdriver.support.ui import WebDriverWait # ожидания различных событий
    from selenium.webdriver.support.ui import Select # работа со списками
    from selenium.webdriver.common.action_chains import ActionChains # различные действия

Примеры запуска браузера:
-------------------------

    ffp = webdriver.FirefoxProfile(ff_Profile) # Установка профиля мозиллы, где ff_Profile - это путь к каталогу с профилем.

    page = webdriver.Firefox(firefox_profile=ffp, timeout=5)) # page - экземпляр класса <class 'selenium.webdriver.firefox.webdriver.WebDriver'>. Фактически - это окно браузера.

    page.maximize_window() # разворачивание окна браузера во весь экран


Список методов и свойств:
-------------------------
    
    ['NATIVE_EVENTS_ALLOWED', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_unwrap_value', '_wrap_value', 'add_cookie', 'back', 'close', 'create_web_element', 'current_url', 'current_window_handle', 'delete_all_cookies', 'delete_cookie', 'desired_capabilities', 'execute', 'execute_async_script', 'execute_script', 'find_element', 'find_element_by_class_name', 'find_element_by_css_selector', 'find_element_by_id', 'find_element_by_link_text', 'find_element_by_name', 'find_element_by_partial_link_text', 'find_element_by_tag_name', 'find_element_by_xpath', 'find_elements', 'find_elements_by_class_name', 'find_elements_by_css_selector', 'find_elements_by_id', 'find_elements_by_link_text', 'find_elements_by_name', 'find_elements_by_partial_link_text', 'find_elements_by_tag_name', 'find_elements_by_xpath', 'firefox_profile', 'forward', 'get', 'get_cookie', 'get_cookies', 'get_screenshot_as_base64', 'get_screenshot_as_file', 'get_window_position', 'get_window_size', 'implicitly_wait', 'maximize_window', 'name', 'orientation', 'page_source', 'quit', 'refresh', 'save_screenshot', 'set_page_load_timeout', 'set_script_timeout', 'set_window_position', 'set_window_size', 'start_client', 'start_session', 'stop_client', 'switch_to_active_element', 'switch_to_alert', 'switch_to_default_content', 'switch_to_frame', 'switch_to_window', 'title', 'window_handles']


manage.py startapp fts
----------------------

    mysite
    |-- fts
    |   |-- __init__.py
    |   |-- models.py
    |   |-- tests.py
    |   `-- views.py
    |-- manage.py
    `-- mysite
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        `-- wsgi.py



.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Nerd opens his web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # he sees the familiar 'Janus CMS' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Janus CMS', body.text)

            # TODO: use the admin site to create a Poll
            self.fail('finish this test for Janus CMS')


./manage.py test fts
--------------------

    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 25, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test')
    AssertionError: finish this test

    ----------------------------------------------------------------------
    Ran 1 test in 5.376s

    FAILED (failures=1)
    Destroying test database for alias 'default'...


Покрытие тестами админки для модели Polls
--------------------------------------------

    * ``find_elements_by_name`` - для поска полей input по имени
      
    * ``send_keys`` - установка значения полю и нажатие RETURN
      
    * ``find_elements_by_link_text`` - возвращает список WebElements

Метод send_keys() - печать в поля ввода
---------------------------------------
Примеры использования:

        # Ввод текста в поле формы, найденного по xPath:
        login = page.find_element_by_xpath("//input[@id='UserName']")
        login.send_keys('my_login') 
        # Или можно сразу:
        page.find_element_by_xpath("//input[@id='UserName']").send_keys('my_login')

Поиск
=====
Чтобы найти все элементы, удовлетворяющие условию поиска, используйте следующие методы (возвращается список):

        find_elements_by_name
        find_elements_by_xpath
        find_elements_by_link_text
        find_elements_by_partial_link_text
        find_elements_by_tag_name
        find_elements_by_class_name
        find_elements_by_css_selector


Помимо общедоступных (public) методов существует два приватных (private) метода, которые при знании указателей объектов страницы могут быть очень полезны: find_element and find_elements.

Пример использования:

        from selenium.webdriver.common.by import By

        driver.find_element(By.XPATH, '//button[text()="Some text"]')
        driver.find_elements(By.XPATH, '//button')

Для класса By доступны следующие атрибуты:

        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"

Поиск по Id
-----------
Используйте этот способ, когда известен id элемента. Если ни один элемент не удовлетворяет заданному значению id, будет вызвано исключение NoSuchElementException.

Для примера, рассмотрим следующий исходный код страницы:

        <html>
         <body>
          <form id="loginForm">
           <input name="username" type="text" />
           <input name="password" type="password" />
           <input name="continue" type="submit" value="Login" />
          </form>
         </body>
        <html>

Элемент form может быть определен следующим образом:

        login_form = driver.find_element_by_id('loginForm')

Поиск по Name
-------------
Используйте этот способ, когда известен атрибут name элемента. Результатом будет первый элемент с искомым значением атрибута name. Если ни один элемент не удовлетворяет заданному значению name, будет вызвано исключение NoSuchElementException.

Для примера, рассмотрим следующий исходный код страницы:

        <html>
         <body>
          <form id="loginForm">
           <input name="username" type="text" />
           <input name="password" type="password" />
           <input name="continue" type="submit" value="Login" />
           <input name="continue" type="button" value="Clear" />
          </form>
        </body>
        <html>

Элементы с именами username и password могут быть определены следующим образом:

        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')

Следующий код получит кнопку “Login”, находящуюся перед кнопкой “Clear”:

        continue = driver.find_element_by_name('continue')
    

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import TestCase
    from django.test import LiveServerTestCase
    from selenium import webdriver
    # we need the special ``Keys``class to send a carriage return to the password field.
    from selenium.webdriver.common.keys import Keys

    class PollsTest(LiveServerTestCase):

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Nerd opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # He sees the familiar 'Janus CMS' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Janus CMS', body.text)

            # Nerd types in his username and passwords and hits return
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('admin')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('adm1n')
            password_field.send_keys(Keys.RETURN)

            # his username and password are accepted, and he is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Site administration', body.text)

            # He now sees a couple of hyperlink that says "Polls"
            polls_links = self.browser.find_elements_by_link_text('Polls')
            self.assertEquals(len(polls_links), 2)

            # TODO: use the admin site to create a Poll
            self.fail('finish this test for Janus CMS')      


./manage.py test fts
--------------------

    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 36, in test_can_create_new_poll_via_admin_site
        self.assertIn('Site administration', body.text)
    AssertionError: 'Site administration' not found in 'Janus CMS\nLogin\nPlease enter the correct username and password for a staff account. Note that both fields may be case-sensitive.\nUsername\nPassword'

    ----------------------------------------------------------------------
    Ran 1 test in 7.359s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

username и password не работаюе  - мы их задавали литералами


Создаем test fixture
-----------------------

    mkdir fts/fixtures
    ./manage.py dumpdata auth.User --indent=2 > fts/fixtures/admin_user.json

JSON representation пользователей
---------------------------------

.. sourcecode:: python
    :filename: mysite/fts/fixtures/admin_user.json

    [
    {
      "model": "auth.user",
      "pk": 1,
      "fields": {
        "password": "pbkdf2_sha256$24000$yCMN0c8j8BhJ$9MA7TwwoWnDVQOeact5TSNk5On7L752QwenweaX4o8A=",
        "last_login": "2016-05-17T06:51:43.460Z",
        "is_superuser": true,
        "username": "janus",
        "first_name": "",
        "last_name": "",
        "email": "janusnic@gmail.com",
        "is_staff": true,
        "is_active": true,
        "date_joined": "2016-03-29T06:46:44.898Z",
        "groups": [],
        "user_permissions": []
      }
    },
    {
      "model": "auth.user",
      "pk": 2,
      "fields": {
        "password": "pbkdf2_sha256$24000$GZ4WMkrEL44H$PBuLXSmfGOI9j53AN+QGPYamJiD8n/bWtqe/kVDwHiA=",
        "last_login": "2016-04-26T08:52:09.595Z",
        "is_superuser": false,
        "username": "boo",
        "first_name": "",
        "last_name": "",
        "email": "boo@localhost.com",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2016-04-26T07:46:54.120Z",
        "groups": [],
        "user_permissions": []
      }
    },
    {
      "model": "auth.user",
      "pk": 3,
      "fields": {
        "password": "!bMOYmV4uADNU742wtymeCdAevqjEiTDKUcwuIHeQ",
        "last_login": "2016-05-11T12:48:19.057Z",
        "is_superuser": false,
        "username": "janusnic",
        "first_name": "Janus",
        "last_name": "Nicon",
        "email": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2016-05-11T11:45:23.887Z",
        "groups": [],
        "user_permissions": []
      }
    }
    ]



Загрузим fixture в тест. 
------------------------
.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import LiveServerTestCase
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    class PollsTest(LiveServerTestCase):
        fixtures = ['admin_user.json']

        def setUp(self):
            [...]

https://docs.djangoproject.com/en/1.9/topics/testing/#fixture-loading

./manage.py test fts

    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 43, in test_can_create_new_poll_via_admin_site
        self.assertEquals(len(polls_links), 2)
    AssertionError: 0 != 2

    ----------------------------------------------------------------------
    Ran 1 test in 12.558s

    FAILED (failures=1)
    Destroying test database for alias 'default'...

.. sourcecode:: python
    :filename: mysite/settings.py


    INSTALLED_APPS = [
        'home',
        'fts',
        'polls',
    ]

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    from django.test import TestCase
    from django.utils import timezone
    from polls.models import Choice, Poll

    class PollModelTest(TestCase):
        def test_creating_a_new_poll_and_saving_it_to_the_database(self):
            # start by creating a new Poll object with its "question" and
            # "pub_date" attributes set
            poll = Poll()
            poll.question = "What's up?"
            poll.pub_date = timezone.now()

            # check we can save it to the database
            poll.save()

            # now check we can find it in the database again
            all_polls_in_database = Poll.objects.all()
            self.assertEquals(len(all_polls_in_database), 1)
            only_poll_in_database = all_polls_in_database[0]
            self.assertEquals(only_poll_in_database, poll)

            # and check that it's saved its two attributes: question and pub_date
            self.assertEquals(only_poll_in_database.question, "What's up?")
            self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)


manage.py test polls

          File "/home/janus/github/tdd-django/mysite/polls/tests.py", line 3, in <module>
            from polls.models import Choice, Poll
        ImportError: cannot import name 'Choice'

.. sourcecode:: python
    :filename: mysite/polls/models.py
    
    from django.db import models

    class Poll(object):
        pass 

    class Choice(object):
        pass

manage.py test polls

      File "/home/janus/github/tdd-django/mysite/polls/tests.py", line 14, in test_creating_a_new_poll_and_saving_it_to_the_database
        poll.save()
    AttributeError: 'Poll' object has no attribute 'save'

.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Poll(models.Model):
        pass

.. sourcecode:: python
    :filename: mysite/polls/models.py

    manage.py test polls

    from django.db import models

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField()

    class Choice(models.Model):
        pass

./manage.py test polls

        Creating test database for alias 'default'...
        .
        ----------------------------------------------------------------------
        Ran 1 test in 0.001s

        OK
        Destroying test database for alias 'default'...

Зарегистрируем модель в admin.py
--------------------------------

    python manage.py test fts

.. sourcecode:: python
    :filename: mysite/polls/admin.py

    from django.contrib import admin
    from polls.models import Poll

    admin.site.register(Poll)


.. sourcecode:: python
    :filename: mysite/pages/dashdoard.py

        self.children.append(
            modules.ModelList(
                _('Polls'),
                column=1,
                collapsible=True,
                models=('polls.models.*', )
            )
        )


./manage.py test fts

        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 43, in test_can_create_new_poll_via_admin_site
            self.assertEquals(len(polls_links), 2)
        AssertionError: 1 != 2

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # He now sees a couple of hyperlink that says "Polls"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 1)

        # TODO: use the admin site to create a Poll
        self.fail('finish this test for Janus CMS')

./manage.py test fts

    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 46, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test for Janus CMS')
    AssertionError: finish this test for Janus CMS


Настраиваем admin site
=======================

Выясним что нужно для построения теста
--------------------------------------

    python manage.py runserver

    http://localhost:8000/admin/``. Login


.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # he now sees a couple of hyperlink that says "Polls"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 2)

        # The second one looks more exciting, so he clicks it
        polls_links[0].click()

        # he is taken to the polls listing page, which shows he has
        # no polls yet
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 total', body.text)

        # he sees a link to 'add' a new poll, so he clicks it
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()

        # TODO: use the admin site to create a Poll
        self.fail('finish this test for Janus CMS')


./manage.py test fts

    Creating test database for alias 'default'...
    F
    ======================================================================
    FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 58, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test for Janus CMS')
    AssertionError: finish this test for Janus CMS


.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # he sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question', body.text)
        self.assertIn('Pub date', body.text)


"Date Published", much nicer.

.. sourcecode:: python
    :filename: mysite/polls/models.py

    from django.db import models

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

    class Choice(models.Model):
        pass

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # he sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question', body.text)
        self.assertIn('Date published', body.text)



Метод get() - переход по URL
---------------------------

Примеры использования:

    page = webdriver.Firefox(firefox_profile=ffp, timeout=5)) # открываем браузер
    page.get('google.com') # Переходим на Google.

    # Переходим по ссылке, содержащейся в теге а, для которого есть текстовое описание 'Настройка синхронизации':
    page.get(page.find_element_by_xpath("//a[contains(text(),'Настройка синхронизации')]").get_attribute('href'))


Метод get_screenshot_as_file() - снятие скриншота web-страницы в .png-файл
--------------------------------------------------------------------------
Примеры использования:

        # Снять скриншот с текущего экземпляра браузера:
        ffp = webdriver.FirefoxProfile(ff_Profile) # указываем профиль
        page = webdriver.Firefox(firefox_profile=ffp, timeout=5)) # открываем браузер
        page.get_screenshot_as_file('full_path.png') # делаем скриншот

Метод switch_to_alert() - переключение на окно сообщения
--------------------------------------------------------
Примеры использования:

    alert = page.switch_to_alert() # Переключаемся на окно алерта. switch_to_alert возвращает класс Alert:
    alert.text # Возвращает текст алерта.
    alert.dismiss() # Выполняет действие "отказаться" от алерта.
    alert.accept() # Выполняет действие "принять" алерт.
    alert.send_keys() # Выполняет действие "напечатать" в окне алерта.


Свойство text  - возвращает текстовое значение элемента web-страницы
--------------------------------------------------------------------
Примеры использования:

        # Получение текстового значения некоторой ссылки, искомой по xpath:
        link = page.find_element_by_xpath("//tr[@class='odd-row']/td/a")
        a = link.text
        # Или можно сразу получить это значение:
        b = page.find_element_by_xpath("//tr[@class='odd-row']/td/a").text

Свойство tag_name - имя тега элемента web-страницы
--------------------------------------------------
Примеры использования:

        # Получение имени тега, для некоторого элемента, найденного по xpath:
        element = page.find_element_by_xpath("//div[@id='main']/..//input[@id='Title']")
        a = element.tag_name # получим имя тега, в данном случае a = 'input'
        # Или можно сразу:
        b = page.find_element_by_xpath("//div[@id='main']/..//input[@id='Title']").tag_name

Метод clear() - очистка текстового содержимого элемента
-------------------------------------------------------
Примеры использования:

        # Удаляем текст, введенный в input:
        page.find_element_by_xpath("//input[@id='Login']").clear()

Метод get_attribute() - получить имя некоторого атрибута для тега элемента web-страницы
---------------------------------------------------------------------------------------
Примеры использования:

        # 1. Получение значения атрибута, для некоторого тега найденного по xpath:
        tag = page.find_element_by_xpath("//div[@id='main']/..//input[@id='Title']")
        a = tag.get_attribute('value') # Получаем значение атрибута 'value' для тега input
        # Или можно сразу:
        b = page.find_element_by_xpath("//div[@id='main']/..//input[@id='Title']").get_attribute('value')

        # 2. Переход по ссылке для пункта меню "Настройка синхронизации":
        page.get(page.find_element_by_xpath("//a[contains(text(),'Настройка синхронизации')]").get_attribute('href'))


Метод click() - щелчок левой кнопки на элементе
-----------------------------------------------
Примеры использования:

        # Щелчок левой кнопки мыши на иконку выпадающего списка, найденную по xpath:
        element = page.find_element_by_xpath("//img[@id='osSelect']")
        element.click()
        # Или можно сразу:
        page.find_element_by_xpath("//img[@id='osSelect']").click()

Метод is_displayed() - проверка видимости элемента
--------------------------------------------------
Примеры использования:

        # 1. Определение того, является ли элемент, найденный по xpath, видимым на форме:
        element = page.find_element_by_xpath("//div[@id='treeWrapper']") # В данном случае определяется, виден ли выпадающий список
        flag = element.is_displayed() # flag = True - если элемент видим, flag = False - если нет
        # Или можно сразу:
        flag = page.find_element_by_xpath("//div[@id='treeWrapper']").is_displayed()

        # 2. Использование в блоке ожидания появления элемента на форме:
        WebDriverWait(page, 5).until(
            lambda element: element.find_element_by_xpath("//div[@id='treeWrapper']").is_displayed(),
            'Timeout while waiting popup-tree list.') # Ждём 5 сек. пока не появится выпадающий список, иначе - пишем сообщение.

find_element_by_xpath
---------------------
Для идентификации элементов на web-форме, чаще всего при работе с Selenium используют xPath
Метод find_element_by_xpath() - поиск элемента web-страницы по xPath

Примеры использования:
----------------------
    # Обращение к элементам страницы по xpath:
    login = page.find_element_by_xpath("//input[@id='UserName']")
    pwd = page.find_element_by_xpath("//input[@id='Password']")


    # Печать в поля ввода:
    login.send_keys(self.login)
    pwd.send_keys(self.password)

    # Или можно сразу:
    page.find_element_by_xpath("//*[@type='submit']").click()
    
Метод until() - проверка выполнения логического условия
-------------------------------------------------------
Примеры использования:

        opTimeout = 5 # задаём таймаут 5 сек.
        # Ждем появления некоторых элементов на форме, найденных по xpath, с указанным таймаутом. Until() принимает в качестве параметра логическое условие.
        # В данном случае - ожидается появление надписи 'Основные параметры' и кнопки Сохранить внизу страницы. Если они не появятся, в лог запишется сообщение:
        WebDriverWait(page, opTimeout).until(lambda element: 
            (element.find_element_by_xpath("//div[@id='main']/..//div[contains(text(), 'Основные параметры')]")) and
            (element.find_element_by_xpath("//div[@id='main']/..//input[@id='save']")), 'Таймаут! Элементы на форме не появились!')

Метод select_by_index() - выбор строк в селекторе по индексу
-------------------------------------------------------------
Примеры использования:

        # Обращение к существующей строке селектора по индексу, если селектор найден по xPath:
        Select(page.find_element_by_xpath("//select[@id='SelectedAttackType']")).select_by_index(1) # Выбирает 2-ю строку в селекторе (отсчет с нуля).

Метод select_by_value() - выбор строк в селекторе по значению
-------------------------------------------------------------
        Примеры использования:
        # Обращение к существующей строке селектора по значению атрибута value, если селектор найден по xPath:

        Select(page.find_element_by_xpath("//select[@id='SelectedStatusId']")).select_by_value(2) # Выбирает строку в селекторе с value=2.

Метод move_to_element() - перемещение курсора мыши на элемент
-------------------------------------------------------------
Примеры использования:

        # Переместить мышь на элемент, найденный по xPath:
        administrationTab = page.find_element_by_xpath("//ul[@class='dropdown']/li[11]/div") # Ищем выпадающее меню.
        hover = ActionChains(page).move_to_element(administrationTab) # Действие по перемещению мыши сохраняется в объекте ActionChains. Затем нужно использовать метод perform()

Метод perform() - выполнение сохраненных действий
-------------------------------------------------
Примеры использования:

        # Переместить мышь на пункт меню и подождать выпадающее меню:
        administrationTab = page.find_element_by_xpath("//ul[@class='dropdown']/li[11]/div") # Ищем выпадающее меню.
        hover = ActionChains(page).move_to_element(administrationTab) # Сохраняем действие в объекте ActionChains.
        hover.perform() # применяем действие
        # Ждем, пока выпадающее меню не откроется, то есть не станет видимой одна из его ссылок:
        WebDriverWait(page, opTimeout).until(
            lambda el: el.find_element_by_xpath("//a[@href='/polidon2/ScheduledEntity']").is_displayed(),
            'Timeout while we are wait pop-up menu.')
    

http://seleniumhq.org/docs/03_webdriver.html
http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py


.. sourcecode:: html
    :filename: html source for admin site

    <label for="id_question" class="required">Question:</label>
    <input id="id_question" type="text" class="vTextField" name="question" maxlength="200" />

    <label for="id_pub_date_0" class="required">Date published:</label>
    <p class="datetime">
        Date: 
        <input id="id_pub_date_0" type="text" class="vDateField" name="pub_date_0" size="10" />
        <br />
        Time:
        <input id="id_pub_date_1" type="text" class="vTimeField" name="pub_date_1" size="8" />
    </p>
                        


.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # he sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question', body.text)
        self.assertIn('Date published', body.text)

        # he types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys("How awesome is Test-Driven Development?")

        # he sets the date and time of publication - it'll be a new year's
        # poll!
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('18/05/16')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')


Можно использовать CSS selector для поска кнопки "Save"

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()


.. sourcecode:: python
    :filename: mysite/fts/tests.py

        # he is returned to the "Polls" listing, where he can see his
        # new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text(
                "How awesome is Test-Driven Development?"
        )
        self.assertEquals(len(new_poll_links), 1)

        # Satisfied, he goes back to sleep


./manage.py test fts

        Creating test database for alias 'default'...
        F
        ======================================================================
        FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 83, in test_can_create_new_poll_via_admin_site
            self.assertEquals(len(new_poll_links), 1)
        AssertionError: 0 != 1


.. sourcecode:: python
    :filename: mysite/polls/models.py

    from django.db import models

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField(verbose_name='Date published')

        def __str__(self):
            return self.question

    class Choice(models.Model):
        pass


./manage.py test fts

        Creating test database for alias 'default'...
        F
        ======================================================================
        FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 87, in test_can_create_new_poll_via_admin_site
            self.fail('finish this test for Janus CMS')
        AssertionError: finish this test for Janus CMS


Добавляем Choices к админ странице Poll
=======================================

https://docs.djangoproject.com/en/1.9/intro/tutorial02/#adding-related-objects

.. sourcecode:: python
    :filename: mysite/fts/tests.py

        [...]
        time_field.send_keys('00:00')

        # he sees he can enter choices for the Poll.  he adds three
        choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
        choice_1.send_keys('Very awesome')
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Quite awesome')
        choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
        choice_3.send_keys('Moderately awesome')

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        [...]


Взаимосвязь моделей: Polls и Choices
-------------------------------------

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    class ChoiceModelTest(TestCase):

        def test_creating_some_choices_for_a_poll(self):
            # start by creating a new Poll object
            poll = Poll()
            poll.question="What's up?"
            poll.pub_date = timezone.now()
            poll.save()

            # now create a Choice object
            choice = Choice()

            # link it with our Poll
            choice.poll = poll

            # give it some text
            choice.choice = "doin' fine..."

            # and let's say it's had some votes
            choice.votes = 3

            # save it
            choice.save()

            # try retrieving it from the database, using the poll object's reverse
            # lookup
            poll_choices = poll.choice_set.all()
            self.assertEquals(poll_choices.count(), 1)

            # finally, check its attributes have been saved
            choice_from_db = poll_choices[0]
            self.assertEquals(choice_from_db, choice)
            self.assertEquals(choice_from_db.choice, "doin' fine...")
            self.assertEquals(choice_from_db.votes, 3)

Также подключаем модели

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    from polls.models import Choice, Poll


.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(object):
        pass


    python manage.py test polls

    ======================================================================
    ERROR: test_creating_some_choices_for_a_poll (polls.tests.ChoiceModelTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/polls/tests.py", line 62, in test_creating_some_choices_for_a_poll
        choice.save()
    AttributeError: 'Choice' object has no attribute 'save'

    ----------------------------------------------------------------------
    Ran 4 tests in 0.745s

    FAILED (errors=1)

Напишем класс Choice:

    class Choice(models.Model):
        pass

https://docs.djangoproject.com/en/1.9/intro/tutorial01/#playing-with-the-api


.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200, default='')
        votes = models.IntegerField(default=0)

зарускаем тест

    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK

Админка: related objects inline
-------------------------------

   python manage.py test fts
   Creating test database for alias 'default'...
   E
   ======================================================================
   ERROR: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "/home/harry/workspace/mysite/fts/tests.py", line 71, in test_can_create_new_poll_via_admin_site
       choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
     File "/usr/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 285, in find_element_by_name
       return self.find_element(by=By.NAME, value=name)
     File "/usr/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 671, in find_element
   {'using': by, 'value': value})['value']
     File "/usr/lib/python2.7/site-packages/selenium/webdriver/remote/webdriver.py", line 156, in execute
       self.error_handler.check_response(response)
     File "/usr/lib/python2.7/site-packages/selenium/webdriver/remote/errorhandler.py", line 147, in check_response
       raise exception_class(message, screen, stacktrace)
   NoSuchElementException: Message: u'Unable to locate element: {"method":"name","selector":"choice_set-0-choice"}' 
   
   ----------------------------------------------------------------------
   Ran 1 test in 14.098s
   
   FAILED (errors=1)


.. sourcecode:: python
    :filename: mysite/polls/admin.py

    from django.contrib import admin
    from polls.models import Choice, Poll

    class ChoiceInline(admin.StackedInline):
        model = Choice
        extra = 3

    class PollAdmin(admin.ModelAdmin):
        inlines = [ChoiceInline]

    admin.site.register(Poll, PollAdmin)


https://docs.djangoproject.com/en/1.9/intro/tutorial02/#adding-related-objects

запускаем FT снова::

    ======================================================================
    FAIL: test_voting_on_a_new_poll (test_polls.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 48, in test_voting_on_a_new_poll
        self._setup_polls_via_admin()
      File "/home/harry/workspace/TDDjango/mysite/fts/test_polls.py", line 42, in _setup_polls_via_admin
        self.assertEquals(len(new_poll_links), 1)
    AssertionError: 0 != 1

    ----------------------------------------------------------------------

.. sourcecode:: python
    :filename: mysite/polls/tests.py

    def test_choice_defaults(self):
        choice = Choice()
        self.assertEquals(choice.votes, 0)


    python manage.py test polls
    [...]
    AssertionError: None != 0


.. sourcecode:: python
    :filename: mysite/polls/models.py

    class Choice(models.Model):
        poll = models.ForeignKey(Poll)
        choice = models.CharField(max_length=200)
        votes = models.IntegerField(default=0)

Окончательно test::

    .
    ----------------------------------------------------------------------
    Ran 2 tests in 21.043s

    OK

Заполнение админки
==================

http://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python)

.. sourcecode:: python
    :filename: mysite/fts/tests.py

    from django.test import TestCase
    from collections import namedtuple
    from django.test import LiveServerTestCase
    from selenium import webdriver
    # we need the special ``Keys``class to send a carriage return to the password field.
    from selenium.webdriver.common.keys import Keys

    import time
    PollInfo = namedtuple('PollInfo', ['question', 'choices'])
    POLL1 = PollInfo(
        question="How awesome is Test-Driven Development?",
        choices=[
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ],
    )
    POLL2 = PollInfo(
        question="Which workshop treat do you prefer?",
        choices=[
            'Beer',
            'Pizza',
            'The Acquisition of Knowledge',
        ],
    )

    class PollsTest(LiveServerTestCase):

        fixtures = ['admin_user.json']

        def setUp(self):
            self.browser = webdriver.Firefox()
            self.browser.implicitly_wait(3)

        def tearDown(self):
            self.browser.quit()

        def test_can_create_new_poll_via_admin_site(self):
            # Nerd opens her web browser, and goes to the admin page
            self.browser.get(self.live_server_url + '/admin/')

            # He sees the familiar 'Janus CMS' heading
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Janus CMS', body.text)

            # Nerd types in his username and passwords and hits return
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('janus')

            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('ghbdtnjanus')
            password_field.send_keys(Keys.RETURN)

            # his username and password are accepted, and he is taken to
            # the Site Administration page
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Site administration', body.text)

            # He now sees a couple of hyperlink that says "Polls"
            polls_links = self.browser.find_elements_by_link_text('Polls')
            self.assertEquals(len(polls_links), 1)

            # The second one looks more exciting, so he clicks it
            polls_links[0].click()

            # he is taken to the polls listing page, which shows he has
            # no polls yet
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('0 total', body.text)

            # he sees a link to 'add' a new poll, so he clicks it
            new_poll_link = self.browser.find_element_by_link_text('Add poll')
            new_poll_link.click()

            # he sees some input fields for "Question" and "Date published"
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('Question', body.text)
            # self.assertIn('Pub date', body.text)
            self.assertIn('Date published', body.text)

            # he types in an interesting question for the Poll
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys("How awesome is Test-Driven Development?")

            # he sets the date and time of publication - it'll be a new year's
            # poll!
            date_field = self.browser.find_element_by_name('pub_date_0')
            date_field.send_keys('05/05/16')
            time_field = self.browser.find_element_by_name('pub_date_1')
            time_field.send_keys('00:00')

            # he sees he can enter choices for the Poll.  he adds three
            self.browser.find_element_by_id('choice_set0').click()
            time.sleep(2)
            choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
            #time.sleep(10)
            #flag = choice_1.is_displayed() # flag = True - если элемент видим, flag = False - если нет
            #self.assertEquals(flag, True)
            
            choice_1.send_keys('Very awesome')
            self.browser.find_element_by_id('choice_set1').click()
            time.sleep(2)
            choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
            choice_2.send_keys('Quite awesome')
            self.browser.find_element_by_id('choice_set2').click()
            time.sleep(2)
            choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
            choice_3.send_keys('Moderately awesome')

            

            # Gertrude clicks the save button
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # She is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link
            new_poll_links = self.browser.find_elements_by_link_text(
                    "How awesome is Test-Driven Development?"
            )
            self.assertEquals(len(new_poll_links), 1)


            # TODO: use the admin site to create a Poll
            self.fail('finish this test for Janus CMS')

        def _setup_polls_via_admin(self):
            # Gertrude logs into the admin site
            self.browser.get(self.live_server_url + '/admin/')
            username_field = self.browser.find_element_by_name('username')
            username_field.send_keys('janus')
            password_field = self.browser.find_element_by_name('password')
            password_field.send_keys('ghbdtnjanus')
            password_field.send_keys(Keys.RETURN)

            # She has a number of polls to enter.  For each one, she:
            for poll_info in [POLL1, POLL2]:
                # Follows the link to the Polls app, and adds a new Poll
                self.browser.find_elements_by_link_text('Polls')[0].click()
                self.browser.find_element_by_link_text('Add poll').click()

                # Enters its name, and uses the 'today' and 'now' buttons to set
                # the publish date
                question_field = self.browser.find_element_by_name('question')
                question_field.send_keys(poll_info.question)
                date_field = self.browser.find_element_by_name('pub_date_0')
                date_field.send_keys('05/05/16')
                time_field = self.browser.find_element_by_name('pub_date_1')
                time_field.send_keys('00:00')
                #self.browser.find_element_by_link_text('Today').click()
                #self.browser.find_element_by_link_text('Now').click()

                # Sees she can enter choices for the Poll on this same page,
                # so she does
                for i, choice_text in enumerate(poll_info.choices):
                    self.browser.find_element_by_id('choice_set%d' % i).click()
                    time.sleep(2)
                    choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                    choice_field.send_keys(choice_text)

                # Saves her new poll
                save_button = self.browser.find_element_by_css_selector("input[value='Save']")
                save_button.click()

                # Is returned to the "Polls" listing, where she can see her
                # new poll, listed as a clickable link by its name
                new_poll_links = self.browser.find_elements_by_link_text(
                        poll_info.question
                )
                self.assertEquals(len(new_poll_links), 1)

                # She goes back to the root of the admin site
                self.browser.get(self.live_server_url + '/admin/')

            # She logs out of the admin site
            self.browser.find_element_by_link_text('Log out').click()


        def test_voting_on_a_new_poll(self):
            # First, Gertrude the administrator logs into the admin site and
            # creates a couple of new Polls, and their response choices
            self._setup_polls_via_admin()

            # Now, Herbert the regular user goes to the homepage of the site. He
            # sees a list of polls.
            self.browser.get(self.live_server_url)
            heading = self.browser.find_element_by_tag_name('h1')
            self.assertEquals(heading.text, 'Polls')

            # He clicks on the link to the first Poll, which is called
            # 'How awesome is test-driven development?'
            first_poll_title = 'How awesome is Test-Driven Development?'
            self.browser.find_element_by_link_text(first_poll_title).click()

            # He is taken to a poll 'results' page, which says
            # "no-one has voted on this poll yet"
            main_heading = self.browser.find_element_by_tag_name('h1')
            self.assertEquals(main_heading.text, 'Poll Results')
            sub_heading = self.browser.find_element_by_tag_name('h2')
            self.assertEquals(sub_heading.text, first_poll_title)
            body = self.browser.find_element_by_tag_name('body')
            self.assertIn('No-one has voted on this poll yet', body.text)

            # He also sees a form, which offers him several choices.
            # There are three options with radio buttons
            choice_inputs = self.browser.find_elements_by_css_selector(
                    "input[type='radio']"
            )
            self.assertEquals(len(choice_inputs), 3)

            # The buttons have labels to explain them
            choice_labels = self.browser.find_elements_by_tag_name('label')
            choices_text = [c.text for c in choice_labels]
            self.assertEquals(choices_text, [
                'Vote:', # this label is auto-generated for the whole form
                'Very awesome',
                'Quite awesome',
                'Moderately awesome',
            ])
            # He decided to select "very awesome", which is answer #1
            chosen = self.browser.find_element_by_css_selector(
                    "input[value='1']"
            )
            chosen.click()

            # Herbert clicks 'submit'
            self.browser.find_element_by_css_selector(
                    "input[type='submit']"
                ).click()

            # The page refreshes, and he sees that his choice
            # has updated the results.  they now say
            # "100 %: very awesome".
            body_text = self.browser.find_element_by_tag_name('body').text
            self.assertIn('100 %: Very awesome', body_text)

            # The page also says "1 vote"
            self.assertIn('1 vote', body_text)

            # But not "1 votes" -- Herbert is impressed at the attention to detail
            self.assertNotIn('1 votes', body_text)

            # Herbert suspects that the website isn't very well protected
            # against people submitting multiple votes yet, so he tries
            # to do a little astroturfing
            self.browser.find_element_by_css_selector("input[value='1']").click()
            self.browser.find_element_by_css_selector("input[type='submit']").click()

            # The page refreshes, and he sees that his choice has updated the
            # results.  it still says # "100 %: very awesome".
            body_text = self.browser.find_element_by_tag_name('body').text
            self.assertIn('100 %: Very awesome', body_text)

            # But the page now says "2 votes"
            self.assertIn('2 votes', body_text)

            # Cackling manically over his l33t haxx0ring skills, he tries
            # voting for a different choice
            self.browser.find_element_by_css_selector("input[value='2']").click()
            self.browser.find_element_by_css_selector("input[type='submit']").click()

            # Now, the percentages update, as well as the votes
            body_text = self.browser.find_element_by_tag_name('body').text
            self.assertIn('67 %: Very awesome', body_text)
            self.assertIn('33 %: Quite awesome', body_text)
            self.assertIn('3 votes', body_text)

            # Satisfied, he goes back to sleep

Мы должны получить AssertionError "TODO"::

        FAIL: test_can_create_new_poll_via_admin_site (fts.tests.PollsTest)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/home/janus/github/tdd-django/mysite/fts/tests.py", line 125, in test_can_create_new_poll_via_admin_site
        self.fail('finish this test for Janus CMS')
    AssertionError: finish this test for Janus CMS



