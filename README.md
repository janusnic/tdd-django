# tdd-django unit_01

Install Python
==============

Unix & Linux Installation:
--------------------------

- Переходим на http://www.python.org/download/
- Распаковываем загруженный файл.
- Редактируем Modules/Setup файл.
- Выполняем
1. ./configure script
2. make
3. make install

python обысно устанавливается в /usr/local/bin, а его библиотеки - в /usr/local/lib/pythonXX.

Windows Installation
---------------------
- Переходим на http://www.python.org/download/
- Загружаем и запускаем python-XYZ.msi.

Macintosh Installation
-----------------------
- Обычно на Macs Python установлен. Если нет, читаем http://www.python.org/download/mac/.
- Иструкция Jack Jansen Website : http://www.cwi.nl/~jack/macpython.html

Setting up PATH
================

Setting path at Unix/Linux
---------------------------
- В csh shell: набрать setenv PATH "$PATH:/usr/local/bin/python" и нажать Enter.
- В bash shell (Linux): набрать export PATH="$PATH:/usr/local/bin/python" и нажать Enter.
- В sh или ksh shell: набрать PATH="$PATH:/usr/local/bin/python" и нажать Enter.

/usr/local/bin/python - стандартный path Python

Setting path at Windows
------------------------
- В command prompt : набрать path %path%;C:\Python и нажать Enter.

C:\Python - стандартный path Python

# Настройка рабочего окружения

# Установка easy_install и pip
## easy_install

Easy Install — это модуль Python (easy_install), идущий в комплекте библиотеки setuptools, которая позволяет автоматически загружать, собирать, устанавливать и управлять пакетами языка Python. 
Пакеты носят название «eggs» и имеют расширение .egg. Как правило, эти пакеты распространяются в формате архива ZIP.

### Использование easy_install

Для начала установим пакет setuptools для Python версии 2.7:
```
$ wget pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg
$ sudo sh setuptools-0.6c11-py2.7.egg
```
Теперь можно установить любой пакет, находящийся в центральном репозитарии модулей языка Python, который называется PyPI (Python Package Index): pypi.python.org/pypi. Работа с easy_install напоминает работу с пакетными менеджерами apt-get, rpm, yum и подобными. 
Для примера установим пакет, содержащий оболочку IPython:
```
sudo easy_install ipython
```
В качестве аргумента указывается либо имя пакета, либо путь до пакета .egg, находящегося на диске. Обратите внимание, что для выполнения установки требуются права суперпользователя, так как easy_install установлен и сам устанавливает пакеты в глобальный для Python каталог site-packages. Установка easy_install в домашнюю директорию производится следующим образом: sh setuptools-0.6c11-py2.7.egg --prefix=~

Поиск пакета на веб-странице:
```
easy_install -f code.google.com/p/liten/ liten
```
Первый аргумент в данном примере — это на какой странице искать, второй — что искать.
Также предусмотрена возможность HTTP Basic аутентификации на сайтах:
```
easy_install -f user:password@example.com/path/
```
Установка архива с исходными кодами по указанному URL:
```
easy_install liten.googlecode.com/files/liten-0.1.5.tar.gz
```
В качестве аргумента достаточно передать адрес архива, а easy_install автоматически распознает архив и установит дистрибутив. Чтобы этот способ сработал, в корневом каталоге архива должен находиться файл setup.py.

Для обновления пакета используется ключ --upgrade:
```
easy_install --upgrade PyProtocols
```
Изменение активной версии установленного пакета:
```
easy_install liten=0.1.3
```
В данном случае производится откат пакета liten до версии 0.1.3.

Преобразование отдельного файла .py в пакет .egg
```
easy_install -f "http://some.example.com/downloads/foo.py#egg=foo-1.0" foo
```
Это полезно, когда, например, необходимо обеспечить доступ к отдельному файлу из любой точки файловой системы. Как вариант, можно добавить путь к файлу в переменную PYTHONPATH. В этом примере #egg=foo-1.0 — это версия пакета, а foo — это его имя.

### Использование конфигурационных файлов

Для опытных пользователей и администраторов предусмотрена возможность создания конфигурационных файлов. Значения параметров по умолчанию можно задать в конфигурационном файле, который имеет формат ini-файла. easy_install осуществляет поиск конфигурационного файла в следующем порядке: 
- текущий_каталог/setup.cfg, 
- ~/.pydistutils.cfg 
- в файле distutils.cfg, в каталоге пакета distutils.

Пример такого файла:
```
[easy_install]

# где искать пакеты
find_links = code.example.com/downloads

# ограничить поиск по доменам
allow_hosts = *.example.com

# куда устанавливать пакеты (каталог должен находиться в переменной окружения PYTHONPATH)
install_dir = /src/lib/python
```
pip - Python Package Installer
==============================
## Python 2.7.9+ and 3.4+

Download get-pip.py
--------------------
https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py

Выполнить
```
python get-pip.py
```

## Получение Administrative credentials

To start a command prompt as an administrator

1. Click Start, click All Programs, and then click Accessories.
2. Right-click Command prompt, and then click Run as administrator.
3. If the User Account Control dialog box appears, confirm that the action it displays is what you want, and then click Continue.

To start a command prompt as an administrator (alternative method)

1. Click Start.
2. In the Start Search box, type cmd, and then press CTRL+SHIFT+ENTER.
3. If the User Account Control dialog box appears, confirm that the action it displays is what you want, and then click Continue.

## Установка для Windows:

1. Install setuptools http://www.lfd.uci.edu/~gohlke/pythonlibs/#setuptools
2. Install pip http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip

Установит Pip в C:\Python27\Scripts\pip.exe. 
Нужно добавить путь C:\Python27\Scripts) в установки path (Start / Edit environment variables).

Установить пакет
```
pip install httpie
```
Установка для Windows:

1. Загрузить http://pypi.python.org/pypi/pip#downloads
2. Распаковать
3. Загрузить installer для Windows: (.exe http://pypi.python.org/pypi/setuptools ). 
4. Установить
5. Сковировать каталог pip в C:\Python2x\ (только содеожимое)
6. Выполнить

python setup.py install

7. Добавить C:\Python2x\Scripts в переменную path

# Virtual Environments
Виртуальное окружение — это независимый от установленных в системе набор библиотек, модулей и самого интерпретатора Python, которые используются при работе с текущим проектом. 

## Установка virtualenv
```
$ pip install virtualenv
```
Создать virtual environment:
```
$ cd my_project_folder
$ virtualenv venv
```
Для выбранной версии Python.
----------------------------
```
$ virtualenv -p /usr/bin/python2.7 venv
```
Активировать virtual:
-------------
```
$ source venv/bin/activate
```
Установка пакетов:
------------------
```
$ pip install requests
```
Деактивировать virtualenv:
---------------
```
$ deactivate
```
Удалить virtualenv
--------
```
rm -rf venv
```
Заморозка “freeze”
------------------
```
$ pip freeze > requirements.txt
```
Разморозка:
-----------
```
$ pip install -r requirements.txt
```
# virtualenvwrapper

Установка (virtualenv должен быть установлен):
----------------------------------------------
```
$ pip install virtualenvwrapper
$ export WORKON_HOME=~/Envs
$ source /usr/local/bin/virtualenvwrapper.sh

```
Для Windows используйте virtualenvwrapper-win.
----------------------------------------------
```
$ pip install virtualenvwrapper-win
```
Для Windows путь WORKON_HOME - %USERPROFILE%Envs
------------------------------------------------

Создаем виртуальное окружение командой:
---------------------------------------
```
mkvirtualenv venv

mkvirtualenv -p python3.4 dj21
```
Эта команда создаст виртуальное окружение с названием venv внутри ~/Envs.

Эта команда активирует virtual environment:
-------------------------------------------
```
$ workon venv
```
Деактивировать:
---------------
```
$ deactivate
```
Удалить:
---------
```
$ rmvirtualenv venv
```
Список environments.
--------------------
```
lsvirtualenv

dj21
====
env1
====

```
Переход в каталог текущего virtual environment
----------------------------------------------
```
cdvirtualenv
```
Показать контент каталога site-packages
---------------------------------------
```
lssitepackages
```
# autoenv
При входе в каталог, содержащий .env, autoenv автоматически активирует окружение.

Установка в Mac OS X с помощью brew:
```
$ brew install autoenv
```
Установка в Linux:
```
$ git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
$ echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc
```

Install Django & Virtualenv on Mac OS X / Linux with PIP
--------------------------------------------------------
```
cd ~/Desktop

mkdir Development

cd Development

Create a new virtualenv:

virtualenv env3dj -p python3

Activate virtualenv:

source bin/activate

The result in Terminal should be something like:

(env3dj):~$
```
Install Django:
----------------
```
pip install django==1.9.4
```

# Основы Version Control
Распределённая система управления версиями файлов. Проект был создан Линусом Торвальдсом для управления разработкой ядра Linux, первая версия выпущена 7 апреля 2005 года.

## Установка GIT

### Установка в Linux
Fedora:
```
$ yum install git-core
```
Debian, Ubuntu:
```
$ apt-get install git
```
### Установка на Mac

Есть два простых способа установить Git на Mac. Самый простой — использовать графический инсталлятор Git'а, который вы можете скачать со страницы на SourceForge:

http://sourceforge.net/projects/git-osx-installer/

Другой распространённый способ установки Git'а — через MacPorts (http://www.macports.org). Если у вас установлен MacPorts, установите Git так:
```
$ sudo port install git-core +svn +doc +bash_completion +gitweb
```

### Установка в Windows
Просто скачайте exe-файл инсталлятора со страницы проекта на GitHub'е и запустите его:
```
http://msysgit.github.com/
```
После установки у вас будет как консольная версия (включающая SSH-клиент), так и стандартная графическая.

Пожалуйста, используйте Git только из командой оболочки, входящей в состав msysGit.

## Основы Git
### Первоначальная настройка Git

В состав Git'а входит утилита git config, которая позволяет просматривать и устанавливать параметры, контролирующие все аспекты работы Git'а и его внешний вид. Эти параметры могут быть сохранены в трёх местах:

- Файл /etc/gitconfig содержит значения, общие для всех пользователей системы и для всех их репозиториев. Если при запуске git config указать параметр --system, то параметры будут читаться и сохраняться именно в этот файл.
- Файл ~/.gitconfig хранит настройки конкретного пользователя. Этот файл используется при указании параметра --global.
- Конфигурационный файл в каталоге Git'а (.git/config) в том репозитории, где вы находитесь в данный момент. Эти параметры действуют только для данного конкретного репозитория. Настройки на каждом следующем уровне подменяют настройки из предыдущих уровней, то есть значения в .git/config перекрывают соответствующие значения в /etc/gitconfig.

В системах семейства Windows Git ищет файл .gitconfig в каталоге $HOME (C:\Documents and Settings\$USER или C:\Users\$USER). Кроме того Git ищет файл /etc/gitconfig, но уже относительно корневого каталога MSys, который находится там, куда вы решили установить Git, когда запускали инсталлятор.

## Имя пользователя
Первое, что вам следует сделать после установки Git'а, — указать ваше имя и адрес электронной почты. Это важно, потому что каждый коммит в Git'е содержит эту информацию, и она включена в коммиты, передаваемые вами, и не может быть далее изменена:
```
$ git config --global user.name "John Doe"
$ git config --global user.email johndoe@example.com
```
если указана опция --global, то эти настройки достаточно сделать только один раз, поскольку в этом случае Git будет использовать эти данные для всего, что вы делаете в этой системе. Если для каких-то отдельных проектов вы хотите указать другое имя или электронную почту, можно выполнить эту же команду без параметра --global в каталоге с нужным проектом.

## Выбор редактора
По умолчанию Git использует стандартный редактор вашей системы, обычно это Vi или Vim. Если вы хотите использовать другой текстовый редактор, например, Emacs, можно сделать следующее:
```
$ git config --global core.editor emacs
```
## Утилита сравнения
встроенная diff-утилита - для разрешения конфликтов слияния. Например, если вы хотите использовать vimdiff:
```
$ git config --global merge.tool vimdiff
````
Git умеет делать слияния при помощи kdiff3, tkdiff, meld, xxdiff, emerge, vimdiff, gvimdiff, ecmerge и opendiff, но вы можете настроить и другую утилиту.

## Проверка настроек

```
$ git config --list
```
Некоторые ключи настроек могут появиться несколько раз, потому что Git читает один и тот же ключ из разных файлов (например из /etc/gitconfig и ~/.gitconfig). В этом случае Git использует последнее значение для каждого ключа.

проверить значение конкретного ключа, выполнив git config {ключ}:
```
$ git config user.name
```
Если вам нужна помощь при использовании Git'а, есть три способа открыть страницу руководства по любой команде Git'а:
```
$ git help <команда>
$ git <команда> --help
$ man git-<команда>
```
открыть руководство по команде config:
```
$ git help config
```

## Создание Git-репозитория

### Создание репозитория в существующем каталоге
Если вы собираетесь начать использовать Git для существующего проекта, то вам необходимо перейти в проектный каталог и в командной строке ввести

$ git init
Эта команда создаёт в текущем каталоге новый подкаталог с именем .git содержащий все необходимые файлы репозитория — основу Git-репозитория. На этом этапе ваш проект ещё не находится под версионным контролем.

Если вы хотите добавить под версионный контроль существующие файлы (в отличие от пустого каталога), вам стоит проиндексировать эти файлы и осуществить первую фиксацию изменений. Осуществить это вы можете с помощью нескольких команд git add указывающих индексируемые файлы, а затем commit:
```
$ git add *.c
$ git add README
$ git commit -m 'initial project version'
```
## Клонирование существующего репозитория

Клонирование репозитория осуществляется командой git clone [url]:
```
$ git clone https://github.com/janusnic/tdd-django
```
Эта команда создаёт каталог с именем grit, инициализирует в нём каталог .git, скачивает все данные для этого репозитория и создаёт (checks out) рабочую копию последней версии. Если вы зайдёте в новый каталог grit, вы увидите в нём проектные файлы, пригодные для работы и использования. Если вы хотите клонировать репозиторий в каталог, отличный от grit, можно это указать в следующем параметре командной строки:
```
$ git clone  https://github.com/janusnic/tdd-django mygrit
```

В Git'е реализовано несколько транспортных протоколов, которые вы можете использовать. В предыдущем примере использовался протокол git://, вы также можете встретить http(s):// или user@server:/path.git, использующий протокол передачи SSH. 

## Запись изменений в репозиторий
каждый файл в вашем рабочем каталоге может находиться в одном из двух состояний: под версионным контролем (отслеживаемые) и нет (неотслеживаемые). Отслеживаемые файлы — это те файлы, которые были в последнем слепке состояния проекта (snapshot); они могут быть неизменёнными, изменёнными или подготовленными к коммиту (staged). Неотслеживаемые файлы — это всё остальное, любые файлы в вашем рабочем каталоге, которые не входили в ваш последний слепок состояния и не подготовлены к коммиту. Когда вы впервые клонируете репозиторий, все файлы будут отслеживаемыми и неизменёнными, потому что вы только взяли их из хранилища (checked them out) и ничего пока не редактировали.

Как только вы отредактируете файлы, Git будет рассматривать их как изменённые, т.к. вы изменили их с момента последнего коммита. Вы индексируете (stage) эти изменения и затем фиксируете все индексированные изменения, а затем цикл повторяется. 

## Определение состояния файлов
Основной инструмент, используемый для определения, какие файлы в каком состоянии находятся — это команда git status. Если вы выполните эту команду сразу после клонирования, вы увидите что-то вроде этого:
```
$ git status
git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Changes not staged for commit:
  (используйте "git add <file>..." чтобы обновить данные для закрепления)
  (используйте "git checkout -- <file>..." чтобы отменить изменения в рабочей директории)

    modified:   README.md

Несопровождаемые файлы:
  (используйте "git add <file>..." чтобы включить то, что должно быть закреплено)

    unit_01/

нет изменений, добавленных в коммит (используйте "git add" и/или "git commit -a")

```
Это означает, что у вас чистый рабочий каталог — в нём нет отслеживаемых изменённых файлов. Git также не обнаружил неотслеживаемых файлов, в противном случае они бы были перечислены здесь. И наконец, команда сообщает вам на какой ветке (branch) вы сейчас находитесь. Пока что это всегда ветка master — это ветка по умолчанию

Предположим, вы добавили в свой проект новый файл, простой файл README. Если этого файла раньше не было, и вы выполните git status, вы увидите свой неотслеживаемый файл вот так:
```
Несопровождаемые файлы:
  (используйте "git add <file>..." чтобы включить то, что должно быть закреплено)

    unit_01/

нет изменений, добавленных в коммит (используйте "git add" и/или "git commit -a")
```
Понять, что новый файл README неотслеживаемый можно по тому, что он находится в секции "Untracked files" в выводе команды status. Статус "неотслеживаемый файл", по сути, означает, что Git видит файл, отсутствующий в предыдущем снимке состояния (коммите); Git не станет добавлять его в ваши коммиты, пока вы его явно об этом не попросите. Это предохранит вас от случайного добавления в репозиторий сгенерированных бинарных файлов или каких-либо других, которые вы и не думали добавлять. 


## Отслеживание новых файлов
Для того чтобы начать отслеживать (добавить под версионный контроль) новый файл, используется команда git add. Чтобы начать отслеживание файла README, вы можете выполнить следующее:
```
$ git add README
```
Если вы снова выполните команду status, то увидите, что файл README теперь отслеживаемый и индексированный:
```
git add unit_01
$ git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    new file:   unit_01/README.md
    new file:   unit_01/benchmarks.py
    new file:   unit_01/get-pip.py

```
Вы можете видеть, что файл проиндексирован по тому, что он находится в секции “Changes to be committed”. Если вы выполните коммит в этот момент, то версия файла, существовавшая на момент выполнения вами команды git add, будет добавлена в историю снимков состояния. Команда git add принимает параметром путь к файлу или каталогу, если это каталог, команда рекурсивно добавляет (индексирует) все файлы в данном каталоге.

### Индексация изменённых файлов
Давайте модифицируем файл, уже находящийся под версионным контролем. Если вы измените отслеживаемый файл README.md и после этого снова выполните команду status, то результат будет примерно следующим:
```
$ git status
Changes not staged for commit:
  (используйте "git add <file>..." чтобы обновить данные для закрепления)
  (используйте "git checkout -- <file>..." чтобы отменить изменения в рабочей директории)

    modified:   README.md
```
Файл README.md находится в секции “Changes not staged for commit” — это означает, что отслеживаемый файл был изменён в рабочем каталоге, но пока не проиндексирован. Чтобы проиндексировать его, необходимо выполнить команду git add (это многофункциональная команда, она используется для добавления под версионный контроль новых файлов, для индексации изменений, а также для других целей, например для указания файлов с исправленным конфликтом слияния). Выполним git add, чтобы проиндексировать README.md, а затем снова выполним git status:
```
git add unit_01/benchmarks.py 
$ git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    new file:   unit_01/README.md

```

Если вы изменили файл после выполнения git add, вам придётся снова выполнить git add, чтобы проиндексировать последнюю версию файла:
```
git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    new file:   unit_01/README.md
    
Changes not staged for commit:
  (используйте "git add <file>..." чтобы обновить данные для закрепления)
  (используйте "git checkout -- <file>..." чтобы отменить изменения в рабочей директории)

    modified:   README.md
    
```
## Игнорирование файлов
Зачастую, у вас имеется группа файлов, которые вы не только не хотите автоматически добавлять в репозиторий, но и видеть в списках неотслеживаемых. К таким файлам обычно относятся автоматически генерируемые файлы (различные логи, результаты сборки программ и т.п.). В таком случае, вы можете создать файл .gitignore с перечислением шаблонов соответствующих таким файлам. Вот пример файла .gitignore:
```
$ cat .gitignore
*.pyo
*.pyc
*~
```
Первая строка предписывает Git'у игнорировать любые файлы заканчивающиеся на .pyo или .pyc — файлы, которые могут появиться во время сборки кода. Вторая строка предписывает игнорировать все файлы заканчивающиеся на тильду (~), которая используется во многих текстовых редакторах, например Emacs, для обозначения временных файлов. Вы можете также включить каталоги log, tmp или pid; автоматически создаваемую документацию; и т.д. и т.п. Хорошая практика заключается в настройке файла .gitignore до того, как начать серьёзно работать, это защитит вас от случайного добавления в репозиторий файлов, которых вы там видеть не хотите.

К шаблонам в файле .gitignore применяются следующие правила:
------------------------------------------------------------
- Пустые строки, а также строки, начинающиеся с #, игнорируются.
- Можно использовать стандартные glob шаблоны.
- Можно заканчивать шаблон символом слэша (/) для указания каталога.
- Можно инвертировать шаблон, использовав восклицательный знак (!) в качестве первого символа.
Glob-шаблоны представляют собой упрощённые регулярные выражения используемые командными интерпретаторами. Символ * соответствует 0 или более символам; последовательность [abc] — любому символу из указанных в скобках (в данном примере p, y или c); знак вопроса (?) соответствует одному символу; [0-9] соответствует любому символу из интервала (в данном случае от 0 до 9).

Вот ещё один пример файла .gitignore:
```
# комментарий — эта строка игнорируется
# не обрабатывать файлы, имя которых заканчивается на
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]

# НО отслеживать файл lib.a, несмотря на то, что мы игнорируем все .a файлы с помощью предыдущего правила
!lib.a
# C extensions
*.so

# игнорировать файл TODO находящийся в корневом каталоге, не относится к файлам вида subdir/TODO
/TODO
# игнорировать все файлы в каталоге
# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# игнорировать doc/notes.txt, но не doc/server/arch.txt
doc/*.txt
# игнорировать все .txt файлы в каталоге doc/
doc/**/*.txt


# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover

# Translations
*.mo
*.pot

# Django stuff:
*.log

# Sphinx documentation
docs/_build/

# PyBuilder
target/

```

git status
```
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    modified:   README.md
    new file:   unit_01/README.md
    new file:   unit_01/benchmarks.py
    new file:   unit_01/get-pip.py

```
## Просмотр индексированных и неиндексированных изменений
Если результат работы команды git status недостаточно информативен для вас — вам хочется знать, что конкретно поменялось, а не только какие файлы были изменены — вы можете использовать команду git diff. 
git diff показывает вам непосредственно добавленные и удалённые строки — собственно заплатку (patch).

Допустим, вы снова изменили и проиндексировали файл README, а затем изменили файл benchmarks.py без индексирования. Если вы выполните команду status, вы опять увидите что-то вроде:

```
git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    modified:   README.md
    new file:   unit_01/README.md
    new file:   unit_01/benchmarks.py
    new file:   unit_01/get-pip.py

Changes not staged for commit:
  (используйте "git add <file>..." чтобы обновить данные для закрепления)
  (используйте "git checkout -- <file>..." чтобы отменить изменения в рабочей директории)

    modified:   unit_01/benchmarks.py

```
Чтобы увидеть, что же вы изменили, но пока не проиндексировали, наберите git diff без аргументов:

```
git diff
diff --git a/unit_01/benchmarks.py b/unit_01/benchmarks.py
index 52bdb68..a0f3889 100644
--- a/unit_01/benchmarks.py
+++ b/unit_01/benchmarks.py
@@ -1,2 +1,3 @@
 # -*- coding:utf-8 -*-
-print "Hello"
\ No newline at end of file
+print "Hello"
+print "World"
\ No newline at end of file
```
Эта команда сравнивает содержимое вашего рабочего каталога с содержимым индекса. Результат показывает ещё не проиндексированные изменения.

Если вы хотите посмотреть, что вы проиндексировали и что войдёт в следующий коммит, вы можете выполнить git diff --cached. (В Git'е версии 1.6.1 и выше, вы также можете использовать git diff --staged, которая легче запоминается.) Эта команда сравнивает ваши индексированные изменения с последним коммитом:
```
git diff --staged
diff --git a/README.md b/README.md
index 7ab9346..b93ac2c 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,81 @@
 # p21v-django
+
+# Django
+https://www.djangoproject.com/

```
Важно отметить, что git diff сама по себе не показывает все изменения сделанные с последнего коммита — только те, что ещё не проиндексированы. 

Другой пример: вы проиндексировали файл benchmarks.py и затем изменили его, вы можете использовать git diff для просмотра как индексированных изменений в этом файле, так и тех, что пока не проиндексированы:
```
$ git add benchmarks.py
$ git status
git status
В ветке master
Your branch is up-to-date with 'origin/master'.

Изменения для закрепления:
  (используйте "git reset HEAD <file>..."  чтобы убрать из буфера)

    modified:   README.md
    new file:   unit_01/README.md
    new file:   unit_01/benchmarks.py
    new file:   unit_01/get-pip.py

Changes not staged for commit:
  (используйте "git add <file>..." чтобы обновить данные для закрепления)
  (используйте "git checkout -- <file>..." чтобы отменить изменения в рабочей директории)

    modified:   unit_01/benchmarks.py
```
Теперь вы можете используя git diff посмотреть непроиндексированные изменения
```
$ git diff
iff --git a/unit_01/benchmarks.py b/unit_01/benchmarks.py
index a0f3889..7afc8ab 100644
--- a/unit_01/benchmarks.py
+++ b/unit_01/benchmarks.py
@@ -1,3 +1,5 @@
 # -*- coding:utf-8 -*-
 print "Hello"
-print "World"
\ No newline at end of file
+print "World"
+
+print ''
\ No newline at end of file
```

а также уже проиндексированные, используя git diff --cached:
```
$ git diff --cached
diff --git a/README.md b/README.md
index 7ab9346..b93ac2c 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,81 @@
 # p21v-django
```

## Фиксация изменений
```
$ git commit
```
Эта команда откроет выбранный вами текстовый редактор. (Редактор устанавливается системной переменной $EDITOR — обычно это vim или emacs, хотя вы можете установить ваш любимый с помощью команды git config --global core.editor).

В редакторе будет отображён следующий текст (это пример окна Vim'а):
```
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
# On branch master
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       new file:   README
#       modified:   benchmarks.py
~
~
~
".git/COMMIT_EDITMSG" 10L, 283C
```
Вы можете видеть, что комментарий по умолчанию для коммита содержит закомментированный результат работы ("выхлоп") команды git status и ещё одну пустую строку сверху. Вы можете удалить эти комментарии и набрать своё сообщение или же оставить их для напоминания о том, что вы фиксируете. (Для ещё более подробного напоминания, что же именно вы поменяли, можете передать аргумент -v в команду git commit. Это приведёт к тому, что в комментарий будет также помещена дельта/diff изменений, таким образом вы сможете точно увидеть всё, что сделано.) Когда вы выходите из редактора, Git создаёт для вас коммит с этим сообщением (удаляя комментарии и вывод diff'а).

Есть и другой способ — вы можете набрать свой комментарий к коммиту в командной строке вместе с командой commit, указав его после параметра -m, как в следующем примере:
```
git commit -m 'Story Fix benchmarks for speed'
[master 55b0cfc] Story Fix benchmarks for speed
 4 files changed, 18543 insertions(+)
 create mode 100644 unit_01/README.md
 create mode 100644 unit_01/benchmarks.py
 create mode 100644 unit_01/get-pip.py

```

коммит сохраняет снимок состояния вашего индекса. Всё, что вы не проиндексировали, так и торчит в рабочем каталоге как изменённое; вы можете сделать ещё один коммит, чтобы добавить эти изменения в репозиторий. Каждый раз, когда вы делаете коммит, вы сохраняете снимок состояния вашего проекта, который позже вы можете восстановить или с которым можно сравнить текущее состояние.

## Игнорирование индексации
Если у вас есть желание пропустить этап индексирования, Git предоставляет простой способ. Добавление параметра -a в команду git commit заставляет Git автоматически индексировать каждый уже отслеживаемый на момент коммита файл, позволяя вам обойтись без git add:

```
$ git commit -a -m 'added new benchmarks'
```

## Удаление файлов
Для того чтобы удалить файл из Git'а, вам необходимо удалить его из отслеживаемых файлов (точнее, удалить его из вашего индекса) а затем выполнить коммит. Это позволяет сделать команда git rm, которая также удаляет файл из вашего рабочего каталога, так что вы в следующий раз не увидите его как “неотслеживаемый”.

Если вы просто удалите файл из своего рабочего каталога, он будет показан в секции “Changes not staged for commit” (“Изменённые но не обновлённые”

удалить файл из индекса, оставив его при этом в рабочем каталоге. Чтобы сделать это, используйте опцию --cached:
```
$ git rm --cached readme.txt
```
В команду git rm можно передавать файлы, каталоги или glob-шаблоны. Это означает, что вы можете вытворять что-то вроде:
```
$ git rm log/\*.log
```

## Перемещение файлов

Если вам хочется переименовать файл в Git'е, вы можете сделать что-то вроде:
```
$ git mv file_from file_to
```
и это отлично сработает. На самом деле, если вы выполните что-то вроде этого и посмотрите на статус, вы увидите, что Git считает, что произошло переименование файла:
```
$ git mv README.txt README
$ git status
# On branch master
# Your branch is ahead of 'origin/master' by 1 commit.
#
# Changes to be committed:
#   (use "git reset HEAD <file>..." to unstage)
#
#       renamed:    README.txt -> README
#
```
Однако, это эквивалентно выполнению следующих команд:
```
$ mv README.txt README
$ git rm README.txt
$ git add README
```
Git неявно определяет, что произошло переименование, поэтому неважно, переименуете вы файл так или используя команду mv. Единственное отличие состоит лишь в том, что mv — это одна команда вместо трёх — это функция для удобства. 

