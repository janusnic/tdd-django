# -*- coding: utf-8 -*-

from selenium import webdriver
import unittest

# Класс теста унаследован от unittest.TestCase. Наследование класса TestCase является способом сообщения модулю unittest, что это тест:

class NewVisitorTest(unittest.TestCase):  

    # setUp — это часть инициализации, этот метод будет вызываться перед каждым методом теста, который вы собираетесь написать внутри класса теста. Здесь мы создаем элемент класса Firefox WebDriver.

    def setUp(self):  
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3) # Implicit waits - Неявные ожидания

    # Метод tearDown будет вызван после каждого метода теста. Это метод для действий чистки. В текущем методе реализовано закрытие окна браузера. Вы можете также вызывать метод quit вместо close. Метод quit закроет браузер полностью, в то время как close закроет одну вкладку. Однако, в случае, когда открыта только одна вкладка, по умолчанию большинство браузеров закрывается полностью.:

    def test_it_worked(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Welcome to Django', self.browser.title)
        
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