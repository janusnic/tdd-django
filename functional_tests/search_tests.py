# -*- coding: utf-8 -*-

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