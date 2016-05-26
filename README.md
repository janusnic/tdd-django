# tdd-django unit_20

Хостинг на Heroku - Размещение Django app на Heroku
====================================================
https://devcenter.heroku.com/articles/django-app-configuration

Heroku была одной из первых платформ, предоставляющих услуги PaaS. В начале, она предлагала услуги размещения только Ruby приложений, но позднее была включена поддержка многих других языков таких как Java, Node.js и Python.

Установка Heroku
----------------
- Создать Heroku user account http://heroku.com/
- Установить Heroku Toolbelt https://toolbelt.heroku.com/
- Доступ к Heroku осуществояется с помощью command-line client https://devcenter.heroku.com/categories/command-line


Toolbelt
========
Первое, что нужно сделать, это установить в систему "тулбелт" - приложение, которое позволяет управдять инстансами heroku из командной строки. Для debian/ubuntu команда будет такая

    $ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh

для других систем смотрим на https://toolbelt.heroku.com

Heroku клиент
--------------
Heroku предлагает утилиту «Heroku клиент» для создания и управления нашим приложением. Эта утилита может быть запущена под управлением Windows, Mac OS X и Linux. 

Для входа на Heroku:
--------------------

    $ heroku login

Heroku запросит у вас email и пароль от вашего аккаунта. При первой авторизации, клиент отправит ваш ssh ключ на сервера Heroku.

        $ heroku login
        Enter your Heroku credentials.
        Email: adam@example.com
        Password (typing will be hidden):
        Authentication successful.
        You're now ready to create your first Heroku app:


Последующие команды можно будет выполнять без авторизации.


        $ cd ~/myapp
        $ heroku create
        Creating stark-fog-398... done, stack is cedar-14
        http://stark-fog-398.herokuapp.com/ | https://git.heroku.com/stark-fog-398.git
        Git remote heroku added


Creating a new Django project
-----------------------------
https://github.com/heroku/heroku-django-template

    $ django-admin startproject --template=https://github.com/heroku/heroku-django-template/archive/master.zip --name=Procfile  myproject

Создание базы данных Heroku PostgreSQL
--------------------------------------
Sqlite не подходит для использования на heroku. На heroku используется так называемая ephemeral filesystem - https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem. Каждый dyno обладает такой файловой системой. На нее можно писать, с нее можно читать, но она время от времени сбрасывается. Так же она очищается при деплое. Поэтому нельзя использовать файловую систему для хранения перманентных данных.

в качестве базы данных нужно использовать Postgres. Heroku предоставляет бесплатный инстанс базы данных PostgreSQL с ограницением в 10k строк. Это ограничение нужно учитывать при выборе Heroku как бесплатного сервиса.

Однако если приложение не использует каких-то особенностей Postgres, то можно оставить среду разработки на sqlite, чтобы не устанавливать Postgres локально.

Heroku Postgres работает как адд-он к приложению. Аддон можно установить командой

    $ heroku addons:add heroku-postgresql:<PLANNAME>

где - название тарифного плана, для free плана это hobby-dev.

    heroku addons:add heroku-postgresql:dev

Про ограничения этого плана можно почитать здесь https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier

После этого в нашем приложении появится переменная окружения DATABASE_URL для подключения к инстансу Postgres.

Следующее, что нам нужно сделать, это установить psycopg2 для использования Python совместно с Postgres.

$ sudo apt-get install python3-dev # для нужной версии питона
$ sudo apt-get install libpq-dev
$ pip install psycopg2

Конфигурация базы данных

На Heroku есть такое понятие, как Config Vars. Это, по сути, набор констант. Хранятся они вместе с контейнером, и передаются в среду выполнения как переменные окружения. В них рекомендуется хранить приватные настройки, такие как логины и пароли.

Там же Heroku хранит и настройки подключения к ДБ Posgres, в переменной DATABASE_URL.

Чтобы внедрить эти параметры в наш settings.py, на помощь приходит пакет dj-database-url. Он парсит DATABASE_URL и подставляет данные подключения в DATABASES['default'] в нашем проекте джанго.

    $ pip install dj-database-url
    $ pip freeze > requirements.txt

В settings.py добавляем (убирать ничего не нужно) настройки подключения к ДБ в соответствии с $DATABASE_URL:

    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)

Database connection persistence
-------------------------------
По умолчанию, Django будет создавать постоянное подключение к базе данных только для каждого цикла запроса приложения.

Постоянные соединения представляют собой связи с базами данных, которые не закрываются при завершении скрипта. При получении запроса на постоянное соединение сервер вначале проверяет, имеется ли идентичное постоянное соединение (которое было открыто при предыдущих обращениях) и, если таковое было найдено, использует его.

Это весьма накладное поведение, которое может замедлить выполение Django приложения.

Django может обеспечивать постоянные соеденения, которые дают значительное улучшение производительности приложения.
https://devcenter.heroku.com/articles/python-concurrency-and-database-connections

settings.py:
------------
    # Update database configuration with $DATABASE_URL.
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

django-toolbelt
---------------
После установки django-toolbelt будут установлены слудующие packages:

– django
– psycopg2
– gunicorn (WSGI server)
– dj-database-url (a Django configuration helper)
– dj-static (a Django static file server)

Из вашего virtual environment active:
-------------------------------------

    $ pip install django-toolbelt


Procfile
---------
https://devcenter.heroku.com/articles/procfile

Каждый проект должен иметь Procfile. Он определяет тип процессов приложения и точку входа. Должен располагаться в корне проекта.

Этот файл весьма прост, он просто определяет имена процессов и команды ассоциированные с ними (файл Procfile):

web: gunicorn myproject.wsgi --log-file -

Эта строка определяет одиночный тип процесса, web, и команду для его запуска. 

Имя web здесь важно. Оно означает, что этот процесс будет приаттачен к стеку HTTP роутинга сервиса Heroku, и получать веб траффик после деплоя. 

Веб сервер
----------
Heroku не предоставляет свой веб сервер. Вместо этого, ожидает что приложение запустит свой собственный сервер на порту, номер которого получит из переменной окружения $PORT.

Gunicorn
--------
Запуск приложения будет осуществляться с помощью Gunicorn, веб-сервера приложений, рекомендуемого Heroku.

Установим Gunicorn:

    $ pip install gunicorn

    $ pip freeze > requirements.txt


Dependencies Файл requirements.txt
----------------------------------

На нашем локальном ПК, мы управляли зависимостями при помощи виртуального окружения, устанавливая в него модули при помощи pip.

Heroku должен правильно определить, что приложение у нас написано на Python. Происходит это очень просто - по наличию файла requirements.txt в корне проекта. Даже если нет зависимых пакетов, requirements.txt должен присутствовать.

Heroku устанавливает все модули перечисленные в нем при помощи pip.

Для создания файла requirements.txt мы должны использовать опцию freeze при вызове pip


    $ pip freeze > requirements.txt

В список необходимо добавить сервер gunicorn, а также драйвер psycopg2, который необходим SQLAlchemy для подключения к базе данных PostgreSQL. 

requirements.txt
----------------
    # This file is here because many Platforms as a Service look for
    #   requirements.txt in the root directory of a project.
    -r requirements/production.txt


Когда происходит деплой, heroku сообщает о найденном приложении python:

    $ git push heroku master
    ...
    remote: -----> Python app detected
    remote: -----> Installing python-2.7.11
    Это означает, что heroku будет разворачивать наше приложение, используя питон версии 2.7.11. Причем не имеет значения, какую версию питона мы используем при разработке.

runtime.txt
-----------
Чтобы изменить версию питона на продакшене, нужно указать ее в файле runtime.txt:

    $ echo "python-3.5.1" >> runtime.txt
    $ git add runtime.txt
    $ git commit -am "add runtime.txt"
    $ git push heroku master
    remote: -----> Python app detected
    remote: -----> Installing python-3.5.1

Не все версии питона одинаково поддерживаются (поддерживаются python-2.7.11 и python-3.5.1). Можно указать и другие версии, однако heroku одобряет и поддерживает именно эти. 

Foreman
-------
Для использования локальной версии Procfile и Foreman:

    $ foreman start


Обслуживание статики
====================

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    STATIC_URL = '/static/'

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )

Django and Static Assets.
-------------------------
https://devcenter.heroku.com/articles/django-assets

Whitenoise
----------
По умолчанию, Django не поддерживает обслуживание статики в продакшене. Heroku рекомендует использовать проект WhiteNoise для наилучшего обслуживания статики на продакшене.

Installing Whitenoise

    $ pip install whitenoise

    $ pip freeze > requirements.txt

settings.py
-----------
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

wsgi.py
-------
    import os
    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<project>.settings")

    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)


heroku buildpacks
-----------------
Каждый buildpack устанавливает в контейнер heroku какой-то набор окружения. Есть официальные buildpack'и и неофициальные. У нас приложение на python, поэтому у нас автоматически установится buildpack heroku/python.

Bower - для установки зависимостей

Нам нужно установть три buildpack'а - именно в такой последовательности - nodejs, bower, python:

    $ heroku buildpacks:clear
    $ heroku buildpacks:set heroku/nodejs
    $ heroku buildpacks:add https://github.com/ejholmes/heroku-buildpack-bower
    $ heroku buildpacks:add heroku/python

bower должен установиться и установать зависимости.

grunt
------
        module.exports = function (grunt) {

          var appConfig = grunt.file.readJSON('package.json');

          // Load grunt tasks automatically
          // see: https://github.com/sindresorhus/load-grunt-tasks
          require('load-grunt-tasks')(grunt);

          // Time how long tasks take. Can help when optimizing build times
          // see: https://npmjs.org/package/time-grunt
          require('time-grunt')(grunt);

          var pathsConfig = function (appName) {
            this.app = appName || appConfig.name;

            return {
              app: this.app,
              templates: this.app + '/templates',
              css: this.app + '/static/css',
              sass: this.app + '/static/sass',
              fonts: this.app + '/static/fonts',
              images: this.app + '/static/images',
              js: this.app + '/static/js',
              manageScript: 'manage.py',
            }
          };

          grunt.initConfig({

            paths: pathsConfig(),
            pkg: appConfig,

            // see: https://github.com/gruntjs/grunt-contrib-watch
            watch: {
              gruntfile: {
                files: ['Gruntfile.js']
              },
              sass: {
                files: ['<%= paths.sass %>/**/*.{scss,sass}'],
                tasks: ['sass:dev'],
                options: {
                  atBegin: true
                }
              },
              livereload: {
                files: [
                  '<%= paths.js %>/**/*.js',
                  '<%= paths.sass %>/**/*.{scss,sass}',
                  '<%= paths.app %>/**/*.html'
                  ],
                options: {
                  spawn: false,
                  livereload: true,
                },
              },
            },

            // see: https://github.com/sindresorhus/grunt-sass
            sass: {
              dev: {
                  options: {
                      outputStyle: 'nested',
                      sourceMap: false,
                      precision: 10
                  },
                  files: {
                      '<%= paths.css %>/project.css': '<%= paths.sass %>/project.scss'
                  },
              },
              dist: {
                  options: {
                      outputStyle: 'compressed',
                      sourceMap: false,
                      precision: 10
                  },
                  files: {
                      '<%= paths.css %>/project.css': '<%= paths.sass %>/project.scss'
                  },
              }
            },

            //see https://github.com/nDmitry/grunt-postcss
            postcss: {
              options: {
                map: true, // inline sourcemaps

                processors: [
                  require('pixrem')(), // add fallbacks for rem units
                  require('autoprefixer-core')({browsers: [
                    'Android 2.3',
                    'Android >= 4',
                    'Chrome >= 20',
                    'Firefox >= 24',
                    'Explorer >= 8',
                    'iOS >= 6',
                    'Opera >= 12',
                    'Safari >= 6'
                  ]}), // add vendor prefixes
                  require('cssnano')() // minify the result
                ]
              },
              dist: {
                src: '<%= paths.css %>/*.css'
              }
            },

            // see: https://npmjs.org/package/grunt-bg-shell
            bgShell: {
              _defaults: {
                bg: true
              },
              runDjango: {
                cmd: 'python <%= paths.manageScript %> runserver'
              },
              
            }
          });

          grunt.registerTask('serve', [
            
            'bgShell:runDjango',
            'watch'
          ]);

          grunt.registerTask('build', [
            'sass:dist',
            'postcss'
          ]);

          grunt.registerTask('default', [
            'build'
          ]);

        };


POSTGRES
--------
    -- Database: mysite

    -- DROP DATABASE mysite;

    CREATE DATABASE mysite
      WITH OWNER = janus
           ENCODING = 'UTF8'
           TABLESPACE = pg_default
           LC_COLLATE = 'ru_UA.UTF-8'
           LC_CTYPE = 'ru_UA.UTF-8'
           CONNECTION LIMIT = -1;

.env
----
    POSTGRES_PASSWORD=ghbdtn
    POSTGRES_USER=janus

    DJANGO_ADMIN_URL=
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=b73!yg0sew+2l!h5*d%&ct33*+b*wdfkdvjg&=jbf@3ub12^_y
    DJANGO_ALLOWED_HOSTS=.janic.my
    DJANGO_AWS_ACCESS_KEY_ID=
    DJANGO_AWS_SECRET_ACCESS_KEY=
    DJANGO_AWS_STORAGE_BUCKET_NAME=
    DJANGO_MAILGUN_API_KEY=
    DJANGO_MAILGUN_SERVER_NAME=
    DJANGO_SERVER_EMAIL=
    DJANGO_SECURE_SSL_REDIRECT=False
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=True
    DJANGO_SENTRY_DSN=

    NEW_RELIC_LICENSE_KEY=
    NEW_RELIC_APP_NAME=mysite

    DJANGO_OPBEAT_ORGANIZATION_ID
    DJANGO_OPBEAT_APP_ID
    DJANGO_OPBEAT_SECRET_TOKEN

manage.py
---------
    #!/usr/bin/env python
    import os
    import sys

    if __name__ == '__main__':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

requirements
------------
    pip install -r requirements/local.txt

Django settings
----------------
config/settings/local:
---------------------

        # -*- coding: utf-8 -*-
        """
        Local settings

        - Run in Debug mode
        - Use console backend for emails
        - Add Django Debug Toolbar
        - Add django-extensions as app
        """

        from .common import *  # noqa

        # DEBUG
        # ------------------------------------------------------------------------------
        DEBUG = env.bool('DJANGO_DEBUG', default=True)
        TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

        # SECRET CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
        # Note: This key only used for development and testing.
        SECRET_KEY = env('DJANGO_SECRET_KEY', default='_okd*(x*+v#k%w940_51h5)se@ej3x0l=4zw!c1mlbqq_q#g&c')

        # Mail settings
        # ------------------------------------------------------------------------------

        EMAIL_PORT = 1025

        EMAIL_HOST = env("EMAIL_HOST", default='mailhog')


        # CACHING
        # ------------------------------------------------------------------------------
        CACHES = {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': ''
            }
        }

        # django-debug-toolbar
        # ------------------------------------------------------------------------------
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
        INSTALLED_APPS += ('debug_toolbar', )

        INTERNAL_IPS = ('127.0.0.1', '10.0.2.2',)

        DEBUG_TOOLBAR_CONFIG = {
            'DISABLE_PANELS': [
                'debug_toolbar.panels.redirects.RedirectsPanel',
            ],
            'SHOW_TEMPLATE_CONTEXT': True,
        }

        # django-extensions
        # ------------------------------------------------------------------------------
        INSTALLED_APPS += ('django_extensions', )

        # TESTING
        # ------------------------------------------------------------------------------
        TEST_RUNNER = 'django.test.runner.DiscoverRunner'

        ########## CELERY
        # In development, all tasks will be executed locally by blocking until the task returns
        CELERY_ALWAYS_EAGER = True
        ########## END CELERY

        # Your local stuff: Below this line define 3rd party library settings


2. config/settings/common:
-------------------------

        # -*- coding: utf-8 -*-
        """
        Django settings for Janus Nic project.

        For more information on this file, see
        https://docs.djangoproject.com/en/dev/topics/settings/

        For the full list of settings and their values, see
        https://docs.djangoproject.com/en/dev/ref/settings/
        """
        from __future__ import absolute_import, unicode_literals

        import environ

        ROOT_DIR = environ.Path(__file__) - 3  # (janic/config/settings/common.py - 3 = mysite/)
        APPS_DIR = ROOT_DIR.path('mysite')

        env = environ.Env()

        # APP CONFIGURATION
        # ------------------------------------------------------------------------------
        DJANGO_APPS = (
            # Default Django apps:
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            # Useful template tags:
            # 'django.contrib.humanize',

            # Admin
            'django.contrib.admin',
        )
        THIRD_PARTY_APPS = (
            'crispy_forms',  # Form layouts
            'allauth',  # registration
            'allauth.account',  # registration
            'allauth.socialaccount',  # registration
        )

        # Apps specific for this project go here.
        LOCAL_APPS = (
            'mysite.users',  # custom users app
            # Your stuff: custom apps go here
        )

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
        INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

        # MIDDLEWARE CONFIGURATION
        # ------------------------------------------------------------------------------
        MIDDLEWARE_CLASSES = (
            # Make sure djangosecure.middleware.SecurityMiddleware is listed first
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        )

        # MIGRATIONS CONFIGURATION
        # ------------------------------------------------------------------------------
        MIGRATION_MODULES = {
            'sites': 'mysite.contrib.sites.migrations'
        }

        # DEBUG
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
        DEBUG = env.bool('DJANGO_DEBUG', False)

        # FIXTURE CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
        FIXTURE_DIRS = (
            str(APPS_DIR.path('fixtures')),
        )

        # EMAIL CONFIGURATION
        # ------------------------------------------------------------------------------
        EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

        # MANAGER CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
        ADMINS = (
            ("""Janus""", 'janusnic@gmail.com'),
        )

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
        MANAGERS = ADMINS

        # DATABASE CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
        DATABASES = {
            # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
            'default': env.db('DATABASE_URL', default='postgres:///mysite'),
        }
        DATABASES['default']['ATOMIC_REQUESTS'] = True


        # GENERAL CONFIGURATION
        # ------------------------------------------------------------------------------
        # Local time zone for this installation. Choices can be found here:
        # http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
        # although not all choices may be available on all operating systems.
        # In a Windows environment this must be set to your system time zone.
        TIME_ZONE = 'UTC'

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
        LANGUAGE_CODE = 'en-us'

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
        SITE_ID = 1

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
        USE_I18N = True

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
        USE_L10N = True

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
        USE_TZ = True

        # TEMPLATE CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
        TEMPLATES = [
            {
                # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
                'DIRS': [
                    str(APPS_DIR.path('templates')),
                ],
                'OPTIONS': {
                    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
                    'debug': DEBUG,
                    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
                    # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
                    'loaders': [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ],
                    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                        # Your stuff: custom template context processors go here
                    ],
                },
            },
        ]

        # See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
        CRISPY_TEMPLATE_PACK = 'bootstrap3'

        # STATIC FILE CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
        STATIC_ROOT = str(ROOT_DIR('staticfiles'))

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
        STATIC_URL = '/static/'

        # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
        STATICFILES_DIRS = (
            str(APPS_DIR.path('static')),
        )

        # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
        STATICFILES_FINDERS = (
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        )

        # MEDIA CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
        MEDIA_ROOT = str(APPS_DIR('media'))

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
        MEDIA_URL = '/media/'

        # URL Configuration
        # ------------------------------------------------------------------------------
        ROOT_URLCONF = 'config.urls'

        # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
        WSGI_APPLICATION = 'config.wsgi.application'

        # AUTHENTICATION CONFIGURATION
        # ------------------------------------------------------------------------------
        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'allauth.account.auth_backends.AuthenticationBackend',
        )

        # Some really nice defaults
        ACCOUNT_AUTHENTICATION_METHOD = 'username'
        ACCOUNT_EMAIL_REQUIRED = True
        ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

        ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
        ACCOUNT_ADAPTER = 'mysite.users.adapters.AccountAdapter'
        SOCIALACCOUNT_ADAPTER = 'mysite.users.adapters.SocialAccountAdapter'

        # Custom user app defaults
        # Select the correct user model
        AUTH_USER_MODEL = 'users.User'
        LOGIN_REDIRECT_URL = 'users:redirect'
        LOGIN_URL = 'account_login'

        # SLUGLIFIER
        AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

        ########## CELERY
        INSTALLED_APPS += ('mysite.taskapp.celery.CeleryConfig',)
        # if you are not using the django database broker (e.g. rabbitmq, redis, memcached), you can remove the next line.
        INSTALLED_APPS += ('kombu.transport.django',)
        BROKER_URL = env('CELERY_BROKER_URL', default='django://')
        ########## END CELERY


        # Location of root django.contrib.admin URL, use {% url 'admin:index' %}
        ADMIN_URL = r'^admin/'

        # Your common stuff: Below this line define 3rd party library settings



3.config/settings/production:
-----------------------------

        # -*- coding: utf-8 -*-
        """
        Production Configurations

        - Use djangosecure
        - Use Amazon's S3 for storing static files and uploaded media
        - Use mailgun to send emails
        - Use Redis on Heroku

        - Use sentry for error logging


        - Use opbeat for error reporting

        """
        from __future__ import absolute_import, unicode_literals

        from boto.s3.connection import OrdinaryCallingFormat
        from django.utils import six

        import logging


        from .common import *  # noqa

        # SECRET CONFIGURATION
        # ------------------------------------------------------------------------------
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
        # Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
        SECRET_KEY = env('DJANGO_SECRET_KEY')

        # This ensures that Django will be able to detect a secure connection
        # properly on Heroku.
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

        # django-secure
        # ------------------------------------------------------------------------------
        INSTALLED_APPS += ('djangosecure', )
        # raven sentry client
        # See https://docs.getsentry.com/hosted/clients/python/integrations/django/
        INSTALLED_APPS += ('raven.contrib.django.raven_compat', )
        SECURITY_MIDDLEWARE = (
            'djangosecure.middleware.SecurityMiddleware',
        )
        # Use Whitenoise to serve static files
        # See: https://whitenoise.readthedocs.io/
        WHITENOISE_MIDDLEWARE = (
            'whitenoise.middleware.WhiteNoiseMiddleware',
        )
        MIDDLEWARE_CLASSES = WHITENOISE_MIDDLEWARE + MIDDLEWARE_CLASSES
        RAVEN_MIDDLEWARE = (
            'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
        )
        MIDDLEWARE_CLASSES = RAVEN_MIDDLEWARE + MIDDLEWARE_CLASSES

        # Make sure djangosecure.middleware.SecurityMiddleware is listed first
        MIDDLEWARE_CLASSES = SECURITY_MIDDLEWARE + MIDDLEWARE_CLASSES

        # opbeat integration
        # See https://opbeat.com/languages/django/
        INSTALLED_APPS += ('opbeat.contrib.django',)
        OPBEAT = {
            'ORGANIZATION_ID': env('DJANGO_OPBEAT_ORGANIZATION_ID'),
            'APP_ID': env('DJANGO_OPBEAT_APP_ID'),
            'SECRET_TOKEN': env('DJANGO_OPBEAT_SECRET_TOKEN')
        }
        MIDDLEWARE_CLASSES = (
            'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
        ) + MIDDLEWARE_CLASSES
        # set this to 60 seconds and then to 518400 when you can prove it works
        SECURE_HSTS_SECONDS = 60
        SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
            'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
        SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
            'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
        SECURE_BROWSER_XSS_FILTER = True
        SESSION_COOKIE_SECURE = False
        SESSION_COOKIE_HTTPONLY = True
        SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)

        # SITE CONFIGURATION
        # ------------------------------------------------------------------------------
        # Hosts/domain names that are valid for this site
        # See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
        ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['janic.my'])
        # END SITE CONFIGURATION

        INSTALLED_APPS += ('gunicorn', )

        # STORAGE CONFIGURATION
        # ------------------------------------------------------------------------------
        # Uploaded Media Files
        # ------------------------
        # See: http://django-storages.readthedocs.io/en/latest/index.html
        INSTALLED_APPS += (
            'storages',
        )

        AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
        AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
        AWS_AUTO_CREATE_BUCKET = True
        AWS_QUERYSTRING_AUTH = False
        AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()

        # AWS cache settings, don't change unless you know what you're doing:
        AWS_EXPIRY = 60 * 60 * 24 * 7

        # TODO See: https://github.com/jschneier/django-storages/issues/47
        # Revert the following and use str after the above-mentioned bug is fixed in
        # either django-storage-redux or boto
        AWS_HEADERS = {
            'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
                AWS_EXPIRY, AWS_EXPIRY))
        }

        # URL that handles the media served from MEDIA_ROOT, used for managing
        # stored files.
        MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME


        # Static Assets
        # ------------------------
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


        # EMAIL
        # ------------------------------------------------------------------------------
        DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                                 default='Janus Nic <noreply@janic.my>')
        EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
        MAILGUN_ACCESS_KEY = env('DJANGO_MAILGUN_API_KEY')
        MAILGUN_SERVER_NAME = env('DJANGO_MAILGUN_SERVER_NAME')
        EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Janus Nic] ')
        SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
        NEW_RELIC_LICENSE_KEY = env('NEW_RELIC_LICENSE_KEY')
        NEW_RELIC_APP_NAME = env('NEW_RELIC_APP_NAME')

        # TEMPLATE CONFIGURATION
        # ------------------------------------------------------------------------------
        # See:
        # https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
        TEMPLATES[0]['OPTIONS']['loaders'] = [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
        ]

        # DATABASE CONFIGURATION
        # ------------------------------------------------------------------------------
        # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        DATABASES['default'] = env.db('DATABASE_URL')

        # CACHING
        # ------------------------------------------------------------------------------
        # Heroku URL does not pass the DB number, so we parse it in
        CACHES = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0),
                'OPTIONS': {
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                                # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
                }
            }
        }


        # Sentry Configuration
        SENTRY_DSN = env('DJANGO_SENTRY_DSN')
        SENTRY_CLIENT = env('DJANGO_SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'root': {
                'level': 'WARNING',
                'handlers': ['sentry'],
            },
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s '
                              '%(process)d %(thread)d %(message)s'
                },
            },
            'handlers': {
                'sentry': {
                    'level': 'ERROR',
                    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'ERROR',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'raven': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'sentry.errors': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'django.security.DisallowedHost': {
                    'level': 'ERROR',
                    'handlers': ['console', 'sentry'],
                    'propagate': False,
                },
            },
        }
        SENTRY_CELERY_LOGLEVEL = env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO)
        RAVEN_CONFIG = {
            'CELERY_LOGLEVEL': env.int('DJANGO_SENTRY_LOG_LEVEL', logging.INFO),
            'DSN': SENTRY_DSN
        }

        # Custom Admin URL, use {% url 'admin:index' %}
        ADMIN_URL = env('DJANGO_ADMIN_URL')

        # Your production stuff: Below this line define 3rd party library settings



wsgi.py
----------
Изменить в wsgi.py:

        WSGI config for Janus Nic project.

        This module contains the WSGI application used by Django's development server
        and any production WSGI deployments. It should expose a module-level variable
        named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
        this application via the ``WSGI_APPLICATION`` setting.

        Usually you will have the standard Django WSGI application here, but it also
        might make sense to replace the whole Django WSGI application with a custom one
        that later delegates to the Django one. For example, you could introduce WSGI
        middleware here, or combine a Django application with an application of another
        framework.

        """
        import os

        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
            import newrelic.agent
            newrelic.agent.initialize()
        from django.core.wsgi import get_wsgi_application
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
            from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

        # We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
        # if running multiple sites in the same mod_wsgi process. To fix this, use
        # mod_wsgi daemon mode with each site in its own daemon process, or use
        # os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

        # This application object is used by any WSGI server configured to use this
        """
        # file. This includes Django's development server, if the WSGI_APPLICATION
        # setting points here.
        application = get_wsgi_application()
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
            application = Sentry(application)
        if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
            application = newrelic.agent.WSGIApplicationWrapper(application)
        # Apply WSGI middleware here.
        # from helloworld.wsgi import HelloWorldApplication
        # application = HelloWorldApplication(application)

Настройка Git
---------------
git представляет собой основу разворачивания приложений на Heroku, поэтому он также должен быть установлен. Если вы установили набор инструментов Heroku, то git у вас уже установлен.

Для разворачивания приложения на Heroku, оно должно присутствовать в локальном репозитарии

Git и Heroku
---------------

    $ touch .gitignore

Отредактировать:

    myenv

    *.pyc

    myproject/ignore_directory

Инициировать новый Git repository:
-----------------------------------

    $ git init

    $ git add .

    $ git commit -m “First commit of my django app”

Создать приложение Heroku:
---------------------------

    heroku create janusnic
    Creating janusnic... done, stack is cedar-14
    https://janusnic.herokuapp.com/ | https://git.heroku.com/janusnic.git
    Git remote heroku added


В дополнение к установкам URL, эта команда добавляет нашему репозитарию удаленный репозитарий (git remote), который используем для загрузки кода приложения в облако.

Развертывание приложения:
------------------------

    $ git push heroku master

Метка heroku, которую мы используем в нашей команде git push, была автоматически зарегистрирована в нашем репозитарии git когда мы создавали наше приложение при помощи heroku create. Чтобы посмотреть, как настроен этот удаленный репозитарий, вы можете запустить git remote -v в папке приложения.

Если возникла ошибка Permission denied (publickey)

    $ heroku keys:add ~/.ssh/id_rsa.pub

если ключ у вас есть

    $ heroku keys:add

если хотите ключ создать.

Открыть ваше приложение

    $ heroku open

Убедитесь, что у вас есть dyno

    $ heroku ps:scale web=1

Изменить имя вашего приложения.
------------------------------


    $ git remote rm heroku

    $ git remote add heroku git@heroku.com:yourappname.git

Обновите ваши установки
```````````````````````

    ALLOWED_HOSTS.


При каждом изменении в проекте:

    $ git add .

Удалить последнюю команду:

    $ git reset

Закоммитить:

    $ git commit -m “Describe your changes”

    $ git push heroku master


Можно проверить состояние нод с помощью команды ps: 
--------------------------------------------------

    $ heroku ps
    === web: `gunicorn projectname.wsgi`
    web.1: up for 10s

Лог можно посмотреть с помощью команды log: 
-------------------------------------------

    $ heroku logs
    $ heroku logs -n 200  # показать 200 последних строк
    $ heroku logs --tail  # не возвращать управление, выводить новые сообщения
    $ heroku help logs    # вывести справку по команде logs

Запускать команды Django можно с помощью команды run: 
-----------------------------------------------------

    $ heroku run python manage.py syncdb
    $ heroku run python manage.py shell


PostgreSQL Database – Heroku
----------------------------
Проверка:

    $ heroku addons | grep POSTGRES

Создать новую free postgres database (dev option):
--------------------------------------------------

    heroku addons:create heroku-postgresql:dev
     !    That add-on plan is only available to select users.



    HEROKU_POSTGRESQL_COLOR_URL 

    $ heroku config | grep HEROKU_POSTGRESQL

DATABASE_URL:

    $ heroku pg:promote HEROKU_POSTGRESQL_YELLOW_URL

PostgreSQL databases

    $ heroku pg:info

To establish a psql session

    $ heroku pg:psql


Добавить изменения:

    $ git add .

    $ git commit -m “PostgreSQL set”

    $ git push heroku master


Миграции Django models
----------------------
https://devcenter.heroku.com/articles/one-off-dynos


    $ heroku run python manage.py migrate

Можно и с помощью Django shell:

    $ heroku run python manage.py shell


Языковая поддержка
------------------
settings.py

    $ mkdir locale

Редактировать settings.py:

    ugettext = lambda s : s
    LANGUAGES = (
        (‘en’, ugettext(‘English’)),
        (‘ca’, ugettext(‘Catalan’)),
    )
    LOCALE_PATHS = os.path.join(BASE_DIR, ‘locale’)

And finally, add the locale middleware in the correct position:

    MIDDLEWARE_CLASSES = (
        …
        ‘django.contrib.sessions.middleware.SessionMiddleware’,
        ‘django.middleware.locale.LocaleMiddleware’,
        ‘django.middleware.common.CommonMiddleware’,
        …
    )


Time zone
-------------

    TIME_ZONE = ‘Europe/Kiev’


Удалить базу
-------------

    $ drop mylocaldb

pull database:
--------------

    $ heroku pg:pull myapponheroku::YELLOW mylocaldb

Установка user и password для local database:
---------------------------------------------

    $ PGUSER=user PGPASSWORD=password heroku pg:pull myapponheroku::YELLOW mylocaldb


push database в Heroku:
-----------------------

    $ heroku pg:push mylocaldb HEROKU_POSTGRESQL_YELLOW –app myapponheroku

Если удаленная database не пустая, очистить ее
Django app на PythonAnywhere
    $ heroku pg:reset HEROKU_POSTGRESQL_YELLOW

Размещение Django app на PythonAnywhere
=======================================

www.pythonanywhere.com

1. Создание PythonAnywhere Account
--------------------------------------
Зарегистрировать, создать бесплатный аккаунт уровня "Beginner" на PythonAnywhere - https://www.pythonanywhere.com/pricing/.
После слздания вашего account, доменное имя вашего проекта будет - http://username.pythonanywhere.com, где username - ваш PythonAnywhere username. 

2. PythonAnywhere Web Interface
-----------------------------------
PythonAnywhere web interface сожержит dashboard со следующим функцилналом:

- вкладка consoles, позволяет запускать Python и Bash скрипты;
- вкладка files, управление вашими файлами;
- вкладка web, позволяет конфигурировать ваши установки для хлстинга web application;
- вкладка schedule, позволяет запускать ваши задачи;
- вкладка databases, для конфигурации базы данных MySQL.

PythonAnywhere wiki - https://www.pythonanywhere.com/wiki/.

3. Создание Virtual Environment
---------------------------------

1. Зарегистрипутесь на PythonAnywhere и создайте новое Web app:
2. Перейти в "Web" tab.
3. Выберите "Add a new web app" слева. Нажмите "Next"
4. Выбрать "Manual configuration". Нажмите "Next" - дождитесь создания приложения.
5. Адрес вашего web app -- yourusername.pythonanywhere.com.

Создадим собственное virtualenv и изменим Virtualenv path option.

Создание virtualenv и установка django
----------------------------------------
1. Перейти в "Consoles" tab м запустить Bash console

    ~ $ mkvirtualenv django

- Если хотите использовать Python 3 в virtualenv, используйте mkvirtualenv --python=/usr/bin/python3.4 django18

- Если возникла ошибка mkvirtualenv: command not found, установите VirtualenvWrapper.


    echo '' >> ~/.bashrc && echo 'source virtualenvwrapper.sh' >> .bashrc

    source virtualenvwrapper.sh


Проверим pip:


    (django) ~ $ which pip
    /home/myusername/.virtualenvs/django/bin/pip



Если pip не найден, активируйте virtualenv:
-------------------------------------------

workon django


Установить Django:
-------------------

    (django) ~ $ pip install django==1.9.6

Проверить:

    (django) ~ $ which django-admin.py
    /home/myusername/.virtualenvs/django/bin/django-admin.py

    (django) ~ $ django-admin.py --version


Создать новый django project:
-----------------------------
    (django) ~ $ django-admin.py startproject mysite

Проверить:
----------------

    (django) ~ $ tree mysite
    mysite
    ├── manage.py
    └── mysite
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py


Использование virtualenv в вашем web app
----------------------------------------
Перейти в Web tab и отредактировать WSGI file:

    # +++++++++++ DJANGO +++++++++++
    # To use your own django app use code like this:
    import os
    import sys

    # assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
    path = '/home/myusername/mysite'
    if path not in sys.path:
        sys.path.append(path)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()


- Затем отредактировать ауть к вашему virtualenv в секции Virtualenv. Необходимо указать полный путь, /home/myusername/.virtualenvs/django, или короткое имя virtualenv, _django.
- Сохранить изменения, нпжать кнопку Reload для вашего домена.

Проверить.
----------
Перейти на сайт -- должны увидеть "it worked!" page.

Extra packages
--------------
Для установки MySQL:

    (django) ~/mysite $ pip install mysql-python

Static files
--------------

- Перейти в "Web" tab, выбрать domain, выбрать "Static files" table:
- Нажать "Enter URL" и ввести /static/admin/.
- Нажать "Enter path" и ввести /home/myusername/.virtualenvs/django/lib/python2.7/site-packages/django/contrib/admin/static/admin.
- Нажать кнопку Reload.

Работа с вашим virtualenv
-------------------------------

Если нудно установить новый пакет, нужно запустить:

    (django) ~ $ source virtualenvwrapper.sh

и

    (django) ~ $ workon django18


из GitHub на PythonAnywhere
---------------------------
загрузим наш код из GitHub на PythonAnywhere, создав "клон" репозитория. 
Ввести следующую команду в консоли на PythonAnywhere (заменить your-github-username на свою учётку GitHub):


    $ git clone https://github.com/your-github-username/myblog.git

Эта команда загрузит копию кода на PythonAnywhere. 

Проверить

    tree myblog

Сбор статических файлов.
------------------------

whitenoise - Это утилита для работы с статическими файлами. 

нужно запускать дополнительную команду collectstatic, на сервере. Это даст Django знать, что он должен собрать все статические файлы, которые потребуются серверу.


    (django) $ python manage.py collectstatic


Создаем базу данных на PythonAnywhere
---------------------------------------

Нам нужно инициализировать базу данных на сервере с помощью команд migrate и createsuperuser:

    (django) ~ $ python manage.py migrate

    (django) ~ $ python manage.py createsuperuser

