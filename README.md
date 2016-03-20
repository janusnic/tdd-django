# tdd-django unit_02

# Selenium

http://docs.seleniumhq.org/

Selenium – это проект, в рамках которого разрабатывается серия программных продуктов с открытым исходным кодом (open source):

- Selenium WebDriver,
- Selenium RC,
- Selenium Server,
- Selenium Grid,
- Selenium IDE.

Называть просто словом Selenium любой из этих пяти продуктов, вообще говоря, неправильно, хотя так часто делают, если из контекста понятно, о каком именно из продуктов идёт речь, или если речь идёт о нескольких продуктах одновременно, или обо всех сразу.

## Selenium RC

Selenium RC – это предыдущая версия библиотеки для управления браузерами. Аббревиатура RC в названии этого продукта расшифровывается как Remote Control, то есть это средство для «удалённого» управления браузером.

## Selenium Server

Selenium Server – это сервер, который позволяет управлять браузером с удалённой машины, по сети. 

## Selenium Grid

Selenium Grid – это кластер, состоящий из нескольких Selenium-серверов. 

## Selenium IDE

Selenium IDE – плагин к браузеру Firefox, который может записывать действия пользователя, воспроизводить их, а также генерировать код для WebDriver или Selenium RC, в котором выполняются те же самые действия.

# Selenium WebDriver

http://selenium-python.readthedocs.org/en/latest/api.html

Selenium WebDriver – это программная библиотека для управления браузерами. WebDriver представляет собой драйверы для различных браузеров и клиентские библиотеки на разных языках программирования, предназначенные для управления этими драйверами.

Часто употребляется также более короткое название WebDriver.

использование такого веб-драйвера сводится к созданию бота, выполняющего всю ручную работу с браузером автоматизированно.

Библиотеки WebDriver доступны на языках Java, .Net (C#), Python, Ruby, JavaScript, драйверы реализованы для браузеров Firefox, InternetExplorer, Safari, Andriod, iOS, Chrome и Opera.

Чаще всего Selenium WebDriver используется для тестирования функционала веб-сайтов/веб-ориентированных приложений. Автоматизированное тестирование удобно, потому что позволяет многократно запускать повторяющиеся тесты. Регрессионное тестирование, то есть, проверка, что старый код не перестал работать правильно после внесения новых изменений, является типичным примером, когда необходима автоматизация. WebDriver предоставляет все необходимые методы, обеспечивает высокую скорость теста и гарантирует корректность проверки (поскольку человеский фактор исключен). В официальной документации Selenium приводятся следующие плюсы автоматизированного тестирования веб-приложений:

- возможность проводить чаще регрессионное тестирование;
- быстрое предоставление разработчикам отчета о состоянии продукта;
- получение потенциально бесконечного числа прогонов тестов;
- обеспечение поддержки Agile и экстремальным методам разработки;
- сохранение строгой документации тестов;
- обнаружение ошибок, которые были пропущены на стадии ручного тестирования.

Привязка Python-Selenium предоставляет удобный API для доступа к таким веб-драйверам Selenium как Firefox, Ie, Chrome, Remote и других. На данный момент поддерживаются версии Python 2.7, 3.2, 3.3, 3.4 и 3.5.

Загрузка Selenium для Python
-----------------------------
        pip install -U selenium

        Collecting selenium
          Downloading selenium-2.53.1.tar.gz (815kB)
            100% |████████████████████████████████| 819kB 1.2MB/s 
        Building wheels for collected packages: selenium
          Running setup.py bdist_wheel for selenium ... done
          Stored in directory: /home/janus/.cache/pip/wheels/6e/46/f4/1636b1ae525c3bfba962e767bfc02ce7695007a4b2e454a9b7
        Successfully built selenium
        Installing collected packages: selenium
          Found existing installation: selenium 2.49.2
            Uninstalling selenium-2.49.2:
              Successfully uninstalled selenium-2.49.2
        Successfully installed selenium-2.53.1



## В виртуальное окружение ставим Selenium

        $ workon venv

        (venv)$ pip install django==1.9.4 
        (venv)$ pip install -U selenium

        # (venv)$ pip install unittest2 # (only if using Python 2.6)


# Подробная инструкция для пользователей Windows

1. Установите Python 3.4 через файл MSI, доступный на странице загрузок сайта python.org.
2. Запустите командную строку через программу cmd.exe и запустите команду pip установки selenium.
```
C:\Python34\Scripts\pip.exe install selenium
```
Теперь вы можете запускать свои тестовые скрипты, используя Python:
```
C:\Python34\python.exe C:\my_selenium_script.py
```

pip list
---------

        alabaster (0.7.7)
        Babel (2.2.0)
        Django (1.9.4)
        pip (8.1.0)
        Pygments (2.1)
        pytz (2015.7)
        selenium (2.53.1)
        setuptools (19.7)
        six (1.10.0)
        snowballstemmer (1.2.1)
        Sphinx (1.3.4)
        sphinx-rtd-theme (0.1.9)
        wheel (0.24.0)

Проверка работы selenium
========================
        
        mkdir functional_tests
        cd functional_tests/
        touch tests.py

        subl tests.py 

# Python. Модули и пакеты
Программное обеспечение (приложение или библиотека) на Python оформляется в виде модулей, которые в свою очередь могут быть собраны в пакеты. Модули могут располагаться как в каталогах, так и в ZIP-архивах. Модули могут быть двух типов по своему происхождению: модули, написанные на «чистом» Python, и модули расширения (extension modules), написанные на других языках программирования. Например, в стандартной библиотеке есть «чистый» модуль pickle и его аналог на Си: cPickle. Модуль оформляется в виде отдельного файла, а пакет — в виде отдельного каталога. Подключение модуля к программе осуществляется оператором import. После импорта модуль представлен отдельным объектом, дающим доступ к пространству имён модуля. В ходе выполнения программы модуль можно перезагрузить функцией reload().

# Подключение модуля из стандартной библиотеки

Подключить модуль можно с помощью инструкции import:
```
import os # модуль os для получения текущей директории
os.getcwd() # 'C:\\Python33'
```
Одной инструкцией можно подключить несколько модулей.
```
import time, random
time.time() # 1376047104.056417
random.random() # 0.9874550833306869
```
После импортирования модуля его название становится переменной, через которую можно получить доступ к атрибутам модуля. 
```
import math
math.e # 2.718281828459045
```
если указанный атрибут модуля не будет найден, возбудится исключение AttributeError. А если не удастся найти модуль для импортирования, то ImportError.
```
import notexist
```
# Функция dir()
Встроенная функция dir() используется для получения имён, определённых в модуле.

# Использование псевдонимов
Если название модуля слишком длинное, то для него можно создать псевдоним, с помощью ключевого слова as.
```
import math as m

from math import e, ceil as c
e # 2.718281828459045
c(4.6) # 5
```
Импортируемые атрибуты можно разместить на нескольких строках, если их много:
```
from math import (sin, cos,
          tan, atan)

from позволяет подключить все переменные из модуля. 
from sys import *
```

tests.py
--------

        # -*- coding: utf-8 -*-
        from selenium import webdriver

        # Создаем новый instance от Firefox driver
        driver = webdriver.Firefox()

        # идем на страницу google
        # Метод driver.get перенаправляет к странице URL. 
        # WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. Стоит отметить, что если страница использует много AJAX-кода при загрузке, то WebDriver может не распознать, загрузилась ли она полностью:
        
        driver.get("http://www.google.com")

        # найдем элемент body

        body = browser.find_element_by_tag_name('body')

        # это утверждение (assertion), что body.text содержит слово “Google” 
        
        assert 'Google' in body.text

        # В завершение, окно браузера закрывается.

        browser.quit()


tests.py
--------

        # -*- coding: utf-8 -*-
        from selenium import webdriver

        browser = webdriver.Firefox()
        browser.get('http://google.com/')

        # найдем элемент body

        body = browser.find_element_by_tag_name('body')

        # assert позволяет проверять предположения о значениях произвольных данных в произвольном месте программы. По своей сути assert напоминает констатацию факта, расположенную посреди кода программы. 
        
        # В случаях, когда произнесенное утверждение не верно, assert возбуждает исключение. 

        # Такое поведение позволяет контролировать выполнение программы в строго определенном русле. 

        # Отличие assert от условий заключается в том, что программа с assert не приемлет иного хода событий, считая дальнейшее выполнение программы или функции бессмысленным.

        assert 'Google' in body.text
          
        print('Hello Google')

        browser.quit()


# Errors
Существует (как минимум) два различимых вида ошибок: синтаксические ошибки (syntax errors) и исключения (exceptions).

# Синтаксические ошибки
```
while True print 'Hello world'
  File "<stdin>", line 1, in ?
    while True print 'Hello world'
                   ^
SyntaxError: invalid syntax
```

Даже, если ваша программа работает правильно, неверные данные и ошибки ввода могут привести к непредсказуемым результатам. 
Перехват ошибок - что мы с ними после перехвата можем сделать. 
--------------------------------------------------------------
```
import sys
C = float(sys.argv[1])

if C < -273.15:
    print '%g degrees Celsius is non-physical!' % C
    print 'The Fahrenheit temperature will not be computed.'
else:
    F = 9.0/5*C + 32
    print F
print 'end of program'
```

мы забыли передать аргумент:
```
prog.py Traceback (most recent call last):
File "prog.py", line 2, in
C = float(sys.argv[1])
IndexError: list index out of range
```
Python прервал выполнение программы, показал что ошибка находится во второй строке и указал на тип ошибки — IndexError и краткое объяснение что не так. 
Из этой информации, просмотрев код программы, можно сделать вывод, что индекс 1 выходит за пределы списка (index out of range) - и это правильно, ведь в списке sys.argv только нулевой элемент, название программы. Значит есть всего один возможный индекс 0.

как эту ошибку обработать? 
--------------------------
Предварительно проверять длину списка:

```
if len(sys.argv) < 2:
    print 'You failed to provide Celsius degrees as input '\
        'on  the  command  line!'
    sys.exit(1)   #  прекращаем ввиду ошибки
F = 9.0*C/5 + 32
print '%gC is %.1fF' % (C, F)
```
Для преднамеренного прекращения программы используется функция exit модуля sys. В случае прекращения программы без ошибок функции передается 0, в случае наличия ошибки любое отличное от нуля значение (например, 1). 

# Исключения
Исключения согласуются с философией Python (10-й пункт «дзена Python» — «Ошибки никогда не должны умалчиваться») и являются одним из средств поддержки «утиной типизации».

Исключения свидетельствуют об ошибках и прерывают нормальный ход выполнения программы. 

Исключения возбуждаются с помощью инструкции raise. В общем случае инструкция raise имеет следующий вид:

raise Exception([value]), где Exception – тип исключения, а value – необязательное значение с дополнительной информацией об исключении.

Например:
```
raise RuntimeError(“Неустранимая ошибка”)

```

# Обработка исключений

Обработка исключений поддерживается в Python посредством операторов try, except, else, finally, raise, образующих блок обработки исключения.
```
try:
    # Здесь код, который может вызвать исключение
    raise Exception("message")  # Exception, это один из стандартных типов исключения (всего лишь класс),
    # может использоваться любой другой, в том числе свой

except (Тип исключения1, Тип исключения2, …) as Переменная:
    # Код в блоке выполняется, если тип исключения совпадает с одним из типов
    # (Тип исключения1, Тип исключения2, …) или является наследником одного
    # из этих типов.
    # Полученное исключение доступно в необязательной Переменной.

except (Тип исключения3, Тип исключения4, …) as Переменная:
    # Количество блоков except не ограничено
    raise  # Сгенерировать исключение "поверх" полученного; без параметров - повторно сгенерировать полученное

except:
    # Будет выполнено при любом исключении, не обработанном типизированными блоками except

else:
    # Код блока выполняется, если не было поймано исключений.

finally:
    # Будет исполнено в любом случае, возможно после соответствующего
    # блока except или else
```

Иногда вместо явной обработки исключений удобнее использовать блок with (доступен, начиная с Python 2.5).

# Перехватить исключение с помощью инструкций try и except:

Исключения из обоих мест попадут в except OSError, где можно будет что-то сделать с ошибкой.
Питон делает явный выбор в пользу исключений перед возвратом кода ошибки в своём ядре и стандартной библиотеке.
```
import sys
try:
    C = float(sys.argv[1])
except:
    print 'You failed to provide Celsius degrees as input '\
          'on the command line!'
    sys.exit(1)

F = 9.0*C/5 + 32
print '%gC is %.1fF' % (C, F)
```
Теперь, если мы не передадим аргументов, то найти sys.argv[1] невозможно, значит возникло исключение и мы отправляемся в блок except. Если же передать аргумент, то выполняется только блок try. Проверим:
```
prog.py
You failed to provide Celsius degrees as input on the command line!

prog.py 21
21C is 69.8F
```
## Особые исключения

В Python есть удобная возможность разделять инструкции для ошибок различного рода:
```
import sys
try:
    C = float(sys.argv[1])
except IndexError:
    print 'Celsius degrees must be supplied on the command line'
    sys.exit(1)
except ValueError:
    print 'Celsius degrees must be a pure number, '\
          'not  "%s"' % sys.argv[1]
    sys.exit(1)

F = 9.0*C/5 + 32
print '%gC is %.1fF' % (C, F)
```
Теперь в зависимости от ошибки совершенной пользователем, мы и сами можем сказать пользователю, что он сделал не так и как это исправить.

Возбуждение исключений полезно, когда мы хотим уточнить какую-то ошибку, например понятную нам из физического смысла или каких-то других соображений. Пусть для ввода температуры и подойдет аргумент в виде числа, но мы помним про абсолютный ноль и предостерегаем пользователя:
```
def read_C():
    try:
        C = float(sys.argv[1])
    except IndexError:
        raise IndexError('Celsius degrees must be supplied on the command line')
    except  ValueError:
        raise ValueError('Celsius  degrees must be a pure number, '\
                         'not "%s"' % sys.argv[1])
    if C < -273.15:
        raise ValueError('C=%g is a non-physical value!' % C)
    return C
```
Далее имеются две возможности использовать функцию read_C(). Простой:
```
C = read_C()
```
Неправильный ввод приведет к:
```
prog.py
Traceback (most recent call last):
File "prog.py", line 5, in ?
raise IndexError
IndexError: Celsius degrees must be supplied on the command line.
```
Для людей, незнакомых с Python, возникающие на экране слова Traceback, raise, IndexError могут вызвать недоумение. Самая важная информация для человека, работающего с вашей программой расположена в самом конце. Существует возможность выводить только эту строку. В этом случае функцию мы вызываем так:
```
try:
    C = read_C()
except Exception, e:
    print e
    sys.exit(1)
```
Exception это имена всех возможных исключений, e — сообщение исключения. В нашем случае у нас в функции записаны два типа исключений, поэтому:
```
try:
    C = read_C()
except  (ValueError, IndexError), e:
    print e
    sys.exit(1)
```
После блока определения функции и блока try-except пишем блок вычислений и проверяем программу:
```
import sys

def read_C():
    try:
        C = float(sys.argv[1])
    except IndexError:
        raise IndexError\
        ('Celsius degrees must be supplied on the command line')
    except ValueError:
        raise ValueError\
        ('Celsius degrees must be a pure number, '\
         'not "%s"' % sys.argv[1])
    # C is read correctly as a number, but can have wrong value:
    if C < -273.15:
        raise ValueError('C=%g is a non-physical value!' % C)
    return C

try:
    C = read_C()
except (IndexError, ValueError), e:
    print e
    sys.exit(1)
    
F = 9.0*C/5 + 32
print '%gC is %.1fF' % (C, F)

prog.py
Celsius degrees must be supplied on the command line
prog.py 21C
Celsius degrees must be a pure number, not "21C"
prog.py -500
C=-500 is a non-physical value!
prog.py 21
21C is 69.8F
```
программа теперь не только обрабатывает получаемые данные и выдает ответ, но может работать и с неверными данными, определяя ошибку и выдавая информативное сообщение без лишней раздражающей информации.

# Типы исключений
```
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
  ```
- Самый базовый класс — BaseException. Он и его простые потомки (SystemExit, KeyboardInterrupt,GeneratorExit) не предназначены для перехвата обыкновенным программистом — только Питон и редкие библиотеки должны работать с этими типами. Нарушение правила ведет, например, к тому что программу невозможно корректно завершить.

Использование индекса, выходящего за пределы списка, приводит к ошибке IndexError:
```
>>> data = [1.0/i for i in range(1,10)]
>>> data[9]
...
IndexError: list index out of range
```
Python всегда останавливает программу, когда встречает неправильный индекс.

В случае, если содержимое строки не представляет собой только число, конвертирование заканчивается неудачей и ошибкой ValueError:
```
>>> C = float('21 C')
...
ValueError: invalid literal for float(): 21 C
```
В случае, если вызывается переменная, которой не задано значение, возникает ошибка NameError:
```
>>> print a
...
NameError: name 'a' is not defined
```
Деление на ноль:
```
>>> 3.0/0
...
ZeroDivisionError: float division
```
В случае, если вы ошибаетесь в написании ключевых слов языка, возникает SyntaxError:
```
>>> forr d in data:
...
    forr d in data:
         ^
SyntaxError: invalid syntax
```
Если мы захотим перемножить число на строку:
```
>>> 'a  string'*3.14
...
TypeError: can’t multiply sequence by non-int of type 'float'
```
Исключение TypeError возникает, поскольку объекты таких типов не могут быть перемножены (str и float). Но, вообще говоря, это не значит что число и строка не могут быть перемножены.

Перемножение возможно, если число целое (int). Под операцией умножения здесь понимается повторение строки указанное число раз. Это же правило действует и на списки:
```
>>> '--'*10     #  десять двойных дефисов = 20 дефисов
'--------------------'
>>> n  = 4
>>> [1, 2, 3]*n
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
>>> [0]*n
[0, 0, 0, 0]

```
Также не нужно перехватывать все исключения:
```
try:
    ...
except:
    ...
```
работает как
```
try:
    ...
except BaseException:
    ...
```
# используем операторы try и except, чтобы корректно и красиво завершить скрипт

```
'''функция диалога.
Первым аргументом принимаем ответ пользователя,
вторым - выдаём сообщение при неверном вводе'''

def answer(prompt, choice='Только Yes или no!'):
        while True:
                result = raw_input(prompt)
                if result in ('y', 'Y', 'yes', 'Yes'):
                        print '\nВы выбрали "YES" - заканчиваем\n'
                        '''тут можно использовать оператор break вместо return
                        так же и в ответе No'''
                        return False

                elif result in ('n', 'N', 'no', 'No'):
                        print "\nВы выбрали NO - Я продолжаю работу...\n"

                        print_menu()
                        return True
                else:

                        print(choice)
```

- при Ctrl+C (KeyboardInterrupt - SIGINT)
- или Ctrl+D (EOFError - SIGQUIT) команда

```
elif menu_choice == '7':
    try:
        if  (answer("\nВы уверены, что хотите закончить работу? ('y' или 'n', Ctrl+C для выхода) ")==False):
            break
    except (KeyboardInterrupt, EOFError):
        exit('\nВыход\n')
```

# Проиерка обязательных параметров

```
first_name = input("Имя сотрудника: ")
#validate
while first_name == '':
    print('\n Имя сотрудника required.  Try again.')
    first_name = input("Имя сотрудника: ")
last_name = input("Фамилия сотрудника: ")
#validate
while last_name == '':
    print('\n Фамилия сотрудника required.  Try again.')
    last_name = input("Фамилия сотрудника: ")

```

# Проверка допустимых значений параметров

```
ID_valid = False

      ID = input("Идентификатор сотрудника: ")

      while ID_valid == False:

          try:
              ID = float(ID)
              if ID > 0:
                  ID_valid = True
              else:
                  print("\nID должен быть > 0.  Пробуем еще.")
                  ID = input("Идентификатор сотрудника: ")
          except ValueError:
              print("\nID должен быть числом.  Пробуем еще..")
              ID = input("Идентификатор сотрудника:: ")
```

- Всё, что может быть нужно программисту — это Exception и унаследованные от него классы.

лучше ловить как можно более конкретные классы исключений
```
import os

filename = 'file.txt'
try:
    f = open (filename, 'r')
    try:
        print f.read()
    finally:
        f.close()
except (os.error, IOError) as ex:
    print "Cannot process file", filename, ": Error is", ex
```
нструкция finally служит для реализации завершающих действий, сопутствующих операциям, выполняемым в блоке try. Например:

```

try:
    # Выполнить некоторые действия

finally:

def print_staff():
    try:
        n = 0
        for emp in mystaff.employee_list:
            n += 1
            print(emp)

        if n==0 :
            raise MyError(2)
    except MyError as e:
        print '\nНет данных о сотрудниках :', e.value
    else:
        print  'Хранилище содержит ', n, ' строк'
    finally:
        print  'Дата проверки состояния записей ', datetime.now()

```
Блок finally не используется для обработки ошибок. Он используется для реализации действий, которые должны выполняться всегда, независимо от того, возникла ошибка или нет. Если в блоке try исключений не возникло, блок finally будет выполнен сразу же вcлед за ним. Если возникло исключение, управление сначала будет передано первой инструкции в блоке finally, а затем это исключение будет возбуждено повторно, чтобы обеспечить возможность его обработки в другом обработчике.

```
def fetcher(obj, index):
    return obj[index]

x = 'spam'
fetcher(x, 3)           # Like x[3] 'm'

try:
    fetcher(x, 3)
finally:
    print 'after fetch'

fetcher(x, 3)
print 'after fetch'

# KeyboardInterrupt.

while True:
    try:
        x = int(input("Введите, пожалуйста, число: "))
        break
    except ValueError:
        print("Ой!  Это некорректное число.  Попробуйте ещё раз...")
```

# Оператор try работает следующим образом:

- В начале исполняется блок try (операторы между ключевыми словами try и except).

- Если при этом не появляется исключений, блок except не выполняется и оператор try заканчивает работу.

- Если во время выполнения блока try было возбуждено какое-либо исключение, оставшаяся часть блока не выполняется.

- Затем, если тип этого исключения совпадает с исключением, указанным после ключевого слова except, выполняется блок except, а по его завершению выполнение продолжается сразу после оператора try-except.

- Если порождается исключение, не совпадающее по типу с указанным в блоке except — оно передаётся внешним операторам try; 

- если ни одного обработчика не найдено, исключение считается необработанным (unhandled exception), и выполнение полностью останавливается и выводится сообщение.

# Оператор try может иметь более одного блока except
```
except (RuntimeError, TypeError, NameError):
    pass

```
# необязательный блок else
```
def print_staff():
    try:
        n = 0
        for emp in mystaff.employee_list:
            n += 1
            print(emp)

        if n==0 :
            raise MyError(2)
    except MyError as e:
        print '\nНет данных о сотрудниках :', e.value
    else:
        print  'Хранилище содержит ', n, ' строк'

```

# Семейство OSError

Полный список наследников OSError:
```
OSError
 +-- BlockingIOError
 +-- ChildProcessError
 +-- ConnectionError
 |    +-- BrokenPipeError
 |    +-- ConnectionAbortedError
 |    +-- ConnectionRefusedError
 |    +-- ConnectionResetError
 +-- FileExistsError
 +-- FileNotFoundError
 +-- InterruptedError
 +-- IsADirectoryError
 +-- NotADirectoryError
 +-- PermissionError
 +-- ProcessLookupError
 +-- TimeoutError
```

Поиск Google
------------
search_tests.py
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # начиная с версии 2.4.0
from selenium.webdriver.support import expected_conditions as EC # начиная с версии 2.26.0

# Создаем новый instance от Firefox driver
driver = webdriver.Firefox()

# идем на страницу google
# Метод driver.get перенаправляет к странице URL. 
# WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. Стоит отметить, что если страница использует много AJAX-кода при загрузке, то WebDriver может не распознать, загрузилась ли она полностью:
driver.get("http://www.google.com")

# страница динамическая, поэтому title найдем здесь:
print (driver.title)

# Google

assert "Google" in driver.title

# это утверждение (assertion), что заголовок содержит слово “Google” [assert позволяет проверять предположения о значениях произвольных данных в произвольном месте программы. По своей сути assert напоминает констатацию факта, расположенную посреди кода программы. В случаях, когда произнесенное утверждение не верно, assert возбуждает исключение. Такое поведение позволяет контролировать выполнение программы в строго определенном русле. Отличие assert от условий заключается в том, что программа с assert не приемлет иного хода событий, считая дальнейшее выполнение программы или функции бессмысленным.]

# WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

# найдем элемент с атрибутом name = q (google search box)
inputElement = driver.find_element_by_name("q")

# После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys
# inputElement.send_keys(Keys.RETURN)

# набираем строку поиска
inputElement.send_keys("cheese!")

# сабмитим форму (обычно google автоматически выполняет поиск без submitting)
inputElement.submit()

# После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

# assert "No results found." not in driver.page_source

try:
    # ждем обновления страницы, ждем обновления title
    WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

    # Должны увидеть "cheese! - Поиск в Google"
    print (driver.title)

# В завершение, окно браузера закрывается. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью:
finally:
    driver.quit()
```

python search_tests.py 
----------------------
```
Google
cheese! - Пошук Google

```

## Selenium для написания тестов
Selenium чаще всего используется для написания тестовых ситуаций. Сам пакет selenium не предоставляет никаких тестовых утилит или инструментов разработки. Вы можете писать тесты с помощью модуля Python unittest, py.test или nose.

### тесты с помощью модуля Python unittest
Данный скрипт тестирует функциональность поиска на сайте www.google.com:

py_search_tests.py
```
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class PythonOrgSearch(unittest.TestCase):

# setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):
        self.driver = webdriver.Firefox()

# Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.

    def test_search_in_python_org(self):
        driver = self.driver

        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        driver.get("http://www.google.com")

        # утверждение, что заголовок содержит слово “Google”:

        self.assertIn("Google", driver.title)
        
        # WebDriver предоставляет ряд способов получения элементов с помощью методов find_element_by_*. Для примера, элемент ввода текста input может быть найден по его атрибуту name методом find_element_by_name. 

        elem = driver.find_element_by_name("q")

        # После этого мы посылаем нажатия клавиш (аналогично введению клавиш с клавиатуры). Специальные команды могут быть переданы с помощью класса Keys импортированного из selenium.webdriver.common.keys:

        elem.send_keys("django")

        # После ответа страницы, вы получите результат, если таковой ожидается. Чтобы удостовериться, что мы получили какой-либо результат, добавим утверждение:

        assert "No results found." not in driver.page_source
        elem.send_keys(Keys.RETURN)

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):
        self.driver.close()

# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == "__main__":
    unittest.main()
```

запустить тест python py_search_tests.py 
------------------------------------
```
python py_search_tests.py 
.
----------------------------------------------------------------------
Ran 1 test in 9.733s

OK
```
тест завершился успешно

git add
--------
        git add --all
        git commit -m 'added selenium functional tests'
        [unit_02 5d99404] added selenium functional tests
         4 files changed, 1371 insertions(+), 841 deletions(-)
         rewrite README.md (97%)
         create mode 100644 functional_tests/py_search_tests.py
         create mode 100644 functional_tests/search_tests.py
         create mode 100644 functional_tests/tests.py

Setup Project
=============

```
django-admin startproject mysite

-- mysite
    |-- manage.py
    `-- mysite
        |-- __init__.py
        |-- settings.py
        |-- urls.py
        `-- wsgi.py
```

## Наш первый functional test:

```
cd mysite
mkdir functional_tests
cd functional_tests/
touch test_1.py
```

test_1.py
----------

        # -*- coding: utf-8 -*-

        from selenium import webdriver

        browser = webdriver.Firefox()
        browser.get('http://localhost:8000')

        assert 'Django' in browser.title

python test_1.py 
-----------------
```
Попытка соединения не удалась

Traceback (most recent call last):
  File "test_1.py", line 8, in <module>
    assert 'Django' in browser.title
AssertionError

```

python manage.py runserver
--------------------------
```
./manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

March 18, 2016 - 16:42:09
Django version 1.9.4, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```
python test_1.py 
-----------------

## Наш первый functional test для нашего сайта: 

test_2.py
---------
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Welcome"))

    # You should see "Welcome to Django This is my cool Site!"
    print (browser.title,' This is my cool Site!')

finally:
    browser.quit()
```

python test_2.py 
----------------
```
Welcome to Django
Welcome to Django  This is my cool Site!

```
Selenium WebDriver – это спецификация интерфейса для управления браузером
--------------------------------------------------------------------------
WebDriver – это драйвер браузера, то есть не имеющая пользовательского интерфейса программная библиотека, которая позволяет различным другим программам взаимодействовать с браузером, управлять его поведением, получать от браузера какие-то данные и заставлять браузер выполнять какие-то команды.

Исходя из этого определения, ясно, что WebDriver не имеет прямого отношения к тестированию. Он всего лишь предоставляет автотестам доступ к браузеру. 

Самое главное отличие WebDriver от всех остальных драйверов заключается в том, что это «стандартный» драйвер, а все остальные – «нестандартные».

Организация W3C действительно приняла WebDriver за основу при разработке стандарта интерфейса для управления браузером.

реализация интерфейса WebDriver возложена на производителей браузеров.

В рамках проекта Selenium было разработано несколько референсных реализаций для различных браузеров, но постепенно эта деятельность переходит в ведение производителей браузеров. Драйвер для браузера Chrome разрабатывается в рамках проекта Chromium, его делает та же команда, которая занимается разработкой самого браузера. Драйвер для браузера Opera разрабатывается в компании Opera Software. Драйвер для браузера Firefox разрабатывается участниками проекта Selenium, но в недрах компании Mozilla уже готовится ему замена, которая носит кодовое название Marionette. Этот новый драйвер для Firefox уже доступен в девелоперских сборках браузера. На очереди Internet Explorer и Safari, к их разработке сотрудники соответствующих компаний пока не подключились.

В общем, можно сказать, что Selenium это единственный проект по созданию средств автоматизации управления браузерами, в котором участвуют непосредственно компании, разрабатывающие браузеры. 

ChromeDriver - WebDriver for Chrome
-----------------------------------
https://sites.google.com/a/chromium.org/chromedriver/getting-started
```
import time
from selenium import webdriver

driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!
driver.quit()
```
Controlling ChromeDriver's lifetime
-----------------------------------
```
import time

from selenium import webdriver
import selenium.webdriver.chrome.service as service

service = service.Service('/path/to/chromedriver')
service.start()
capabilities = {'chrome.binary': '/path/to/custom/chrome'}
driver = webdriver.Remote(service.service_url, capabilities)
driver.get('http://www.google.com/xhtml');
time.sleep(5) # Let the user actually see something!
driver.quit()
```

# Functional Test == Acceptance Test == End-to-End Test

test_3.py
---------
```
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'This is my cool Site!' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Site"))
 
    print (browser.title)

finally:
    browser.quit()

```
python test_3.py 
```
Traceback (most recent call last):
  File "test_3.py", line 11, in <module>
    assert 'This is my cool Site!' in browser.title
AssertionError
```
test_welcome.py 

```
# Сначала были импортированы все основные необходимые модули. Модуль unittest встроен в Python и реализован на Java’s JUnit. Этот модуль предоставляет собой утилиту для организации тестов.

from selenium import webdriver
import unittest

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class NewVisitorTest(unittest.TestCase):  

    # setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):  
        self.browser = webdriver.Firefox()

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def tearDown(self):  
        self.browser.quit()

    # Метод теста всегда должен начинаться с фразы test. Первая строка метода создает локальную ссылку на объект драйвера, созданный методом setUp.
    
    def test_can_start_a_list_and_retrieve_it_later(self):  
        
        # Метод driver.get перенаправляет к странице URL в параметре. WebDriver будет ждать пока страница не загрузится полностью (то есть, событие “onload” игнорируется), прежде чем передать контроль вашему тесту или скрипту. 

        self.browser.get('http://localhost:8000')
        
        # утверждение, что заголовок содержит слово “This is my cool Site!”:
        self.assertIn('This is my cool Site!', self.browser.title)  
        
        # self.fail ничего не получилось, генерирует сообщение об ошибке. Используется в качестве напоминания, чтобы закончить тест.

        self.fail('Finish the test!')  
            
# Завершающий код — это стандартная вставка кода для запуска набора тестов [Сравнение __name__ с "__main__" означает, что модуль (файл программы) запущен как отдельная программа («main» — «основная», «главная») (а не импортирован из другого модуля). Если вы импортируете модуль, атрибут модуля __name__ будет равен имени файла без каталога и расширения.]:

if __name__ == '__main__':  
    unittest.main(warnings='ignore')  
```
warnings='ignore' подавляет избыточные предупреждения ResourceWarning,  которые генерируются в момент выполнения. 


python test_welcome.py 
```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_welcome.py", line 29, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('This is my cool Site!', self.browser.title)
AssertionError: 'This is my cool Site!' not found in 'Welcome to Django'

----------------------------------------------------------------------
Ran 1 test in 5.304s

FAILED (failures=1)

```
# Implicit waits - Неявные ожидания
добавить implicitly_wait в настройки setUp:

```
    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

```
test_welcome.py
---------------
```
# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3) # Implicit waits - Неявные ожидания

    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Welcome to Django', self.browser.title)
        
    def tearDown(self):  
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):  
        self.browser.get('http://localhost:8000')
        self.assertIn('This is my cool Site!', self.browser.title)  
        self.fail('Finish the test!')  

if __name__ == '__main__':  
    unittest.main(warnings='ignore')
```
python test_welcome.py
----------------------
```
F.
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_welcome.py", line 34, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('This is my cool Site!', self.browser.title)
AssertionError: 'This is my cool Site!' not found in 'Welcome to Django'

----------------------------------------------------------------------
Ran 2 tests in 10.223s

FAILED (failures=1)

```

./manage.py startapp home
--------------------------

        mysite/
        ├── db.sqlite3
        ├── functional_tests
        ├── home
        │   ├── admin.py
        │   ├── __init__.py
        │   ├── migrations
        │   │   └── __init__.py
        │   ├── apps.py
        │   ├── models.py
        │   ├── tests.py
        │   └── views.py
        ├── manage.py
        └── mysite
            ├── __init__.py
            ├── __pycache__
            ├── settings.py
            ├── urls.py
            └── wsgi.py

git commit -m 'Added home app'
-----------------------------
        git add --all :/
        git rm -r mysite/mysite/__pycache__

        $ git status

        echo "__pycache__" >> .gitignore
        echo "*.pyc" >> .gitignore

        git status

        git add .gitignore

        git commit -m 'added gitignore and home app'

        $ git status


## Unit Tests

Основное различие между юнит-тестами и функциональными тестами является то, что функциональные тесты используются для тестирования приложения с точки зрения пользователя. Модульные тесты используются для тестирования приложения с точки зрения программиста.

TDD подход будет выглядеть так:
-------------------------------
- Начнем с написания функциональных тестов, описывая новые возможности с точки зрения пользователя.
- После того, как у нас есть функциональный тест, который не удается, мы начинаем думать о том, как написать код, который может заставить его пройти. Сейчас мы используем один или несколько юнит-тестов, чтобы определить, как должен вести себя наш код.
- После того, как у нас есть юнит-тест и он не проходит, мы пишем некоторое количество кода приложения, достаточное чтобы пройти наш тест. Мы можем повторять шаги 2 и 3 несколько раз, пока не получим желаемое.
- Теперь мы можем повторно вызвать наши функциональные тесты и посмотреть, проходят ли они. 

# Unit Testing in Django

home/tests.py

```
from django.test import TestCase

# Create your tests here.
```
home/tests.py
-------------
```
from django.test import TestCase

# Create your tests here.
class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
```

./manage.py test      
```
 ./manage.py test
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_bad_maths (home.tests.EqualTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 8, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...

```

# Django MVC, URLs, and View Functions

### Рабочий процесс в Django:

- HTTP-запрос приходит на определенной URL.
- Django использует некоторые правила и решает, какой метод контроллера должен откликнуться на запрос (это называется разрешением URL).
- Метод контроллера обрабатывает запрос и возвращает ответ HTTP.

Проверим две идеи:
------------------
- Можем ли мы разрешить URL для корня сайта ("/") и в каком методе это сделать?
- Может ли метод вернуть некоторый HTML, который получит функциональный тест?

home/tests.py. 
--------------
```
from django.core.urlresolvers import resolve
from django.test import TestCase
from home.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  

```

При вызове "/"(корень сайта), Django находит метод с именем home_page.

Этот метод мы и напишем. Мы планируем сохранить его в home/views.py.

home/views.py. 
```
from django.shortcuts import render

# Create your views here.
home_page = None

```
./manage.py test
```
Creating test database for alias 'default'...
FE
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 11, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 534, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 404, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.core.urlresolvers.Resolver404: {'path': '', 'tried': [[<RegexURLResolver <RegexURLPattern list> (admin:admin) ^admin/>]]}

```
## urls.py

mysite/urls.py. 
```
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]


```
mysite/urls.py. 
```
from django.conf.urls import include, url
from django.contrib import admin

from home import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^admin/', include(admin.site.urls)),
]

```

./manage.py test
```
ERROR: test_root_url_resolves_to_home_page_view (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 11, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 534, in resolve
    return get_resolver(urlconf).resolve(path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 376, in resolve
    sub_match = pattern.resolve(new_path)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 248, in resolve
    return ResolverMatch(self.callback, args, kwargs, self.name)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 255, in callback
    self._callback = get_callable(self._callback_str)
  File "/home/janus/Envs/dj21/lib/python3.4/functools.py", line 448, in wrapper
    result = user_function(*args, **kwds)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/core/urlresolvers.py", line 102, in get_callable
    "'%s' is not a callable or a dot-notation path" % lookup_view
django.core.exceptions.ViewDoesNotExist: 'None' is not a callable or a dot-notation path

```

home/views.py. 
--------------
```
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

./manage.py test
```
Creating test database for alias 'default'...
..
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK

```

## Unit Test метод

home/tests.py. 
```
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from home.views import home_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):

        # создали HttpRequest object, который использует Django когда пользователь запрашивает страницу.

        request = HttpRequest()  
        
        # перенаправляем запрос на метод home_page view, который формирует response - экземпляр класса HttpResponse. Далее проверяем является ли .content в response HTML-текстом который мы отдаем пользователю.

        response = home_page(request)  
        
        # HTML-текст должен начинаться с html тега, который должен закрываться вконце. response.content является сырым литералом (raw bytes), а не Python-строкой, поэтому мы используем b'' синтаксис.

        self.assertTrue(response.content.startswith(b'<html>'))  
        
        # Мы хотим поместить тег title, содержащий наш заголовок.

        self.assertIn(b'<title>Welcome to Django. This is my cool Site!</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>'))  

class EqualTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 2)
```

./manage.py test

```

ERROR: test_home_page_returns_correct_html (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 34, in test_home_page_returns_correct_html
    response = home_page(request)
TypeError: home_page() takes 0 positional arguments but 1 was given

----------------------------------------------------------------------
Ran 3 tests in 0.036s

```

home/views.py. 
--------------
```
def home_page(request):
    pass
```
./manage.py test
```
ERROR: test_home_page_returns_correct_html (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 38, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AttributeError: 'NoneType' object has no attribute 'content'

```
home/views.py. 
```
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    return HttpResponse()
```

./manage.py test
```
FAIL: test_home_page_returns_correct_html (home.tests.HomePageTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 38, in test_home_page_returns_correct_html
    self.assertTrue(response.content.startswith(b'<html>'))
AssertionError: False is not true

```
home/views.py. 
--------------
```
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):

    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title></html>")

```
./manage.py test
```
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK

```

functional tests
-----------------
```
touch functional_tests/__init__.py
```
- Все файлы тестов должны начинаться с test, например test_all_users.py.

- Тестируем заголовок на совпадение с “My Cool Django Site”
- Тестируем цвет h1 header в home page на совпадение с rgba(0, 0, 0, 1).

test_all_users.py:
-------------------
```
# -*- coding: utf-8 -*-
from selenium import webdriver
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import LiveServerTestCase  
 
class HomeNewVisitorTest(LiveServerTestCase): 
 
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
 
    def tearDown(self):
        self.browser.quit()
 
    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)
 
    def test_home_title(self):
        self.browser.get(self.get_full_url("home"))
        self.assertIn("My Cool Django Site", self.browser.title)
 
    def test_h1_css(self):
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"), 
                         "rgba(0, 0, 1, 1)")
```

Шаг за шагом:
--------------
1. Определили function get_full_url, принимающую 1 аргумент - namespace (namespace определен в url). 
2. self.live_server_url определяет local host url. Нужно из-за того, что server использует другой url (обычно http://127.0.0.1:8021).
3. reverse дает подходящий url для указанного namespace, именно - /
4. test_home_title  method проверяет что home page title содержит "My Cool Django Site".
5. test_h1_css method тестирут color. 


./manage.py test functional_tests.test_all_users
------------------------------------------------
```
E.F
======================================================================
ERROR: test_h1_css (functional_tests.test_all_users.HomeNewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/functional_tests/test_all_users.py", line 24, in test_h1_css
    h1 = self.browser.find_element_by_tag_name("h1")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 386, in find_element_by_tag_name
    return self.find_element(by=By.TAG_NAME, value=name)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 744, in find_element
    {'using': by, 'value': value})['value']
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/webdriver.py", line 233, in execute
    self.error_handler.check_response(response)
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/selenium/webdriver/remote/errorhandler.py", line 194, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: {"method":"tag name","selector":"h1"}
Stacktrace:
    at FirefoxDriver.prototype.findElementInternal_ (file:///tmp/tmp2byp9iy3/extensions/fxdriver@googlecode.com/components/driver-component.js:10770)
    at fxdriver.Timer.prototype.setTimeout/<.notify (file:///tmp/tmp2byp9iy3/extensions/fxdriver@googlecode.com/components/driver-component.js:625)

======================================================================
FAIL: test_home_title (functional_tests.test_all_users.HomeNewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/functional_tests/test_all_users.py", line 20, in test_home_title
    self.assertIn("My Cool Django Site", self.browser.title)
AssertionError: 'My Cool Django Site' not found in 'Welcome to Django. This is my cool Site!'

```
Цикл TDD:
---------

home/tests.py:
--------------
```
# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
 
class TestAllUsers(TestCase):
 
    def test_uses_index_template(self):
        response = self.client.get(reverse("main"))
        self.assertTemplateUsed(response, "home/index.html")
 
    def test_uses_base_template(self):
        response = self.client.get(reverse("main"))
        self.assertTemplateUsed(response, "base.html")

``` 
 
./manage.py test home.tests
----------------------------
```
FAIL: test_uses_base_template (home.tests.TestAllUsers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 55, in test_uses_base_template
    self.assertTemplateUsed(response, "base.html")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/test/testcases.py", line 579, in assertTemplateUsed
    self.fail(msg_prefix + "No templates used to render the response")
AssertionError: No templates used to render the response

======================================================================
FAIL: test_uses_index_template (home.tests.TestAllUsers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/janus/github/tdd-django/mysite/home/tests.py", line 51, in test_uses_index_template
    self.assertTemplateUsed(response, "home/index.html")
  File "/home/janus/Envs/dj21/lib/python3.4/site-packages/django/test/testcases.py", line 579, in assertTemplateUsed
    self.fail(msg_prefix + "No templates used to render the response")
AssertionError: No templates used to render the response

----------------------------------------------------------------------

```

Static Files Settings
=====================

Settings file (settings.py)
---------------------------
```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    
    'django.contrib.staticfiles',
]
```

Static files (CSS, JavaScript, Images)
---------------------------------------
https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL
----------
        STATIC_URL = '/static/'


STATICFILES DIR
---------------
```
mkdir static
```

settings.py:
------------
```
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

STATICFILES_DIRS:
-----------------
```
STATIC_URL = '/static/'

STATIC_ROOT = (
    os.path.join(BASE_DIR, "static"),
)

```

Templates Settings
------------------
```
mkdir templates
```

Templates files
---------------
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                 django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Initializr: HTML5 Boilerplate and Twitter Bootstrap
---------------------------------------------------
http://www.initializr.com/

После загрузки и распаковки:
----------------------------
- Переместить index.html, 404.html, humans.txt и robots.txt в templates folder.
- Переименовать index.html в base.html. 
- Остальные файлы переместить в static
- Создайте свой favicon.ico.
- Можно удалить файлы apple-touch-icon.png, browserconfig.xml, tile-wide.png и tile.png.


urls.py
--------
```
urlpatterns = [

    url(r'^$', views.home, name='main'),
    url(r'^admin/', admin.site.urls),
]
```

home/views.py
-------------
```
 
def home(request):
    return render(request, "home/index.html", {})
```
templates/home
---------------
```
mkdir templates/home
touch templates/home/index.html

```

base.html
----------
```
<title>{% block title %}{% endblock %}</title>

```
home/index.html
---------------
```
{% extends "base.html" %}
{% block title %}My Cool Django Site{% endblock %}
```
./manage.py test home.test
---------------------------
```
----------------------------------------------------------------------
Ran 2 tests in 0.033s

OK
```

static/css/main.css
-------------------

        .jumbotron h1 {
            color: rgba(0, 0, 1, 1);
        }

base.html:
----------

        {% load staticfiles %}
        <!DOCTIPE html> 


static files
------------
Заменить
```
    <link rel="stylesheet" href="css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="css/main.css">
```
на
```
    <link rel="stylesheet" href="{% static 'css/bootstrap-theme.min.css' %}">
    <link rel="stylesheet" href="{% static 'css/main.css' %}">
```
Заменить
```
    <script src="js/vendor/modernizr-2.8.3-respond-1.4.2.min.js"></script>
```
на
```
    <script src="{% static 'js/vendor/modernizr-2.8.3-respond-1.4.2.min.js' %}">
```
Заменить
```
    <script src="js/main.js"></script>
    <script src="js/plugins.js"></script>
```
на
```
    <script src="{% static 'js/main.js' %}">
    <script src="{% static 'js/plugins.js' %}">
```
Заменить
```
    <script src="js/vendor/bootstrap.min.js"></script>
```
на
```
    <script src="{% static 'js/vendor/bootstrap.min.js' %}">
```
Но
--
```
document.write('<script src="js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```
заменить на
```
document.write('<script src="static/js/vendor/jquery-1.11.0.min.js"><\/script>')</script>
```
functional_tests.test_all_users --liveserver=localhost:8082
-----------------------------------------------------------
    Ran 2 tests in 12.785s

    OK

settings.py
-----------

        os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8082'


Selenium: http://docs.seleniumhq.org/
Selenium WebDriver: http://selenium-python.readthedocs.org/en/latest/api.html
WebDriver for Chrome: https://sites.google.com/a/chromium.org/chromedriver/getting-started
urlpatterns: https://docs.djangoproject.com/en/1.8/topics/http/urls/
Static files: https://docs.djangoproject.com/en/1.9/howto/static-files/
HTML5 Boilerplate: http://www.initializr.com/
liveserver: https://docs.djangoproject.com/ja/1.9/topics/testing/tools/