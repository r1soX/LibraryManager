# Библиотека книг

Привет! Это простая консольная программа для управления библиотекой книг. С помощью этой программы вы можете добавлять книги, просматривать список книг, искать книги по ключевым словам, удалять книги и многое другое.

## Инструкция по запуску программы

1. Убедитесь, что у вас установлен Python версии 3.x. Если Python не установлен, вы можете скачать его с официального сайта [python.org](https://www.python.org/).
2. Склонируйте репозиторий на свой компьютер.
```shell
git clone https://github.com/r1soX/LibraryManager.git
```
3. Запустите программу, выполнив команду:
```shell
python main.py
```
   
## Использование программы

1. При запуске программы вы увидите меню с доступными действиями.
2. Выберите номер действия, введя соответствующую цифру.
3. Следуйте инструкциям на экране для выполнения выбранного действия.
4. Наслаждайтесь управлением вашей библиотекой книг!

## Дополнительная информация

- Программа использует SQLite базу данных для хранения информации о книгах и жанрах.
- В файле `migrations.sql` содержатся SQL запросы для создания таблиц в базе данных.
- Файл `actions.py` содержит доступные действия для управления библиотекой.
- Файл `library.py` содержит класс `Library` для работы с книгами в библиотеке.