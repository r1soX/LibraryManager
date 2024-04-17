import sqlite3
import os
class Library:
    """
    Класс, представляющий библиотеку книг.
    """
    def __init__(self): 
        """
        Инициализация библиотеки.
        """
        
        # Запрос для создания таблицы жанров, если она не существует
        self.create_genres_table_query = 'SELECT COUNT(*) FROM genres'

        # Запрос для добавления стандартных жанров, если они отсутствуют
        self.add_default_genres_query = 'INSERT INTO genres (name) VALUES (?)'

        # Запрос для получения информации о книге по её ID
        self.get_book_details_query = 'SELECT books.id, books.title, books.author, books.description, genres.name FROM books JOIN genres ON books.genre_id = genres.id WHERE books.id = ?'

        # Запрос для получения списка всех жанров книг
        self.get_genres_query = 'SELECT name FROM genres'

        # Запрос для получения ID книги по её названию
        self.get_book_id_by_title_query = 'SELECT id FROM books WHERE title = ?'

        # Запрос для добавления новой книги в библиотеку
        self.add_book_query = 'INSERT INTO books (title, author, description, genre_id) VALUES (?, ?, ?, (SELECT id FROM genres WHERE name = ?))'

        # Запрос для отображения списка всех книг в библиотеке
        self.books_query = 'SELECT books.id, books.title, books.author, genres.name FROM books JOIN genres ON books.genre_id = genres.id'

        # Запрос для отображения списка книг определенного жанра
        self.display_books_by_genre_query = 'SELECT id, title, author FROM books WHERE genre_id = (SELECT id FROM genres WHERE name = ?)'

        # Запрос для поиска книг по ключевому слову
        self.search_books_query = 'SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?'
        
        self.delete_book_query = 'DELETE FROM books WHERE id = ?'

        # Устанавливаем соединение с базой данных
        self.conn = sqlite3.connect('database/library.db')
        # Создаем курсор для выполнения запросов
        self.cursor = self.conn.cursor()
        # Создаем таблицу книг, если она не существует
        with open('database/migrations/migrations.sql', 'r') as file:
            migration_sql = file.read()
            self.cursor.executescript(migration_sql)
            
        # Сохраняем изменения
        self.conn.commit()
        # Создаем таблицу жанров, если она не существует
        self.create_genres_table()

        
    def create_genres_table(self):
        """
        Создание таблицы жанров книг, если она не существует.
        Добавление жанров, если их нет в базе данных.
        """

        self.cursor.execute(self.create_genres_table_query)
        count = self.cursor.fetchone()[0]
        if count == 0:
            self.cursor.executemany(self.add_default_genres_query, [
                ('Фантастика',), ('Детектив',),('Роман',),('Приключения',),('Драма',)])
            self.conn.commit()
    def get_book_details(self, book_id: int): 
        """
        Получение подробной информации о книге по её ID.

        :param book_id: ID книги.
        :return: Словарь с информацией о книге.
        """
        self.cursor.execute(self.get_book_details_query, (book_id,))
        book = self.cursor.fetchone()
        return book
    def get_genres(self) -> list: 
        """
        Получение списка всех жанров книг в библиотеке.
        :return: Список жанров книг в библиотеке.
        """
        # Получаем список всех жанров книг в библиотеке
        self.cursor.execute(self.get_genres_query)
        genres = self.cursor.fetchall()
        # Формируем список жанров книг
        return [genre[0] for genre in genres]

    def get_book_id_by_title(self, title) -> int:
        """
        Получение ID книги по её названию.
        :param title: Название книги.
        :return: ID книги или None, если книги с таким названием не существует.
        """
        # Получаем ID книги по её названию
        self.cursor.execute(self.get_book_id_by_title_query, (title,))
        book_id = self.cursor.fetchone()
        # Возвращаем ID книги или None, если книги с таким названием не существует
        return book_id[0] if book_id else None
    def add_book(self): 
        """
        Добавление новой книги в библиотеку.
        """
        title = input("Введите название книги: ")
        author = input("Укажите автора книги: ")
        description = input("Введите описание книги: ")
        
        # Проверяем, что название, автор и описание не пусты
        if not title or not author or not description:
            print("Ошибка: Название, автор и описание книги не могут быть пустыми.")
            self.wait_for_enter()
            return
        
        # Получаем список всех жанров книг
        genres = self.get_genres()
        print("Доступные жанры:")
        # Выводим список жанров книг
        for idx, genre in enumerate(genres, start=1):
            print(f"{idx}. {genre}")
        
        choice = input("Выберите номер жанра из списка или введите новый жанр: ")
        # Проверяем, что выбран жанр из списка
        if choice.isdigit() and 1 <= int(choice) <= len(genres):
            genre = genres[int(choice) - 1]
        else:
            genre = input("Введите новый жанр: ")
            if not genre:
                print("Ошибка: Жанр книги не может быть пустым.")
                self.wait_for_enter()
                return
        
        if genre not in genres:
            self.cursor.execute(self.add_default_genres_query, (genre,))
            self.conn.commit()
        
        self.cursor.execute(self.add_book_query, (title, author, description, genre))
        self.conn.commit()
        print(f"Книга {title} успешно добавлена в библиотеку.")
        self.wait_for_enter()

    def display_books(self): 
        """
        Отображение списка всех книг в библиотеке.
        """

        if (self.has_book_data() == False): # Проверяем наличие данных о книгах в библиотеке
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return

        self.cursor.execute(self.books_query)
        books = self.cursor.fetchall()
        for book in books:
            print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
        book_id = input("Введите ID книги для просмотра подробной информации (или нажмите Enter для продолжения): ")
        if not book_id:
            return
        
        if book_id:
            book_details = self.get_book_details(int(book_id))
            if book_details:
                print("Подробная информация о книге:")
                print(f"Название: {book_details[1]}")
                print(f"Автор: {book_details[2]}")
                print(f"Описание: {book_details[3]}")
                print(f"Жанр: {book_details[4]}")
            else:
                print(f'По данному ID книга не найдена.')
        self.wait_for_enter()    
    def has_book_data(self) -> bool:
        """
        Проверка наличия данных о книгах в библиотеке.
        :return: True, если данные о книгах есть, False иначе.
        """
        self.cursor.execute('SELECT COUNT(*) FROM books')
        count = self.cursor.fetchone()[0]
        
        return count > 0 # Если количество книг больше 0, то данные о книгах есть
        
    def display_books_by_genre(self): 
        """
        Отображение списка книг определенного жанра.
        """
        
        if (self.has_book_data() == False):
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        genre = input("Введите жанр для просмотра книг: ")
        if not genre:
            print("Ошибка: Книг без жанров не существует.")
            self.wait_for_enter()
            return
        self.cursor.execute(self.display_books_by_genre_query, (genre,))
        books = self.cursor.fetchall()
        if books:
            print(f"Книги в жанре '{genre}':")
            for book in books:
                print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
        else:
            print(f"Нет книг в жанре '{genre}'.")
        self.wait_for_enter()
            
    def search_books(self): 
        """
        Поиск книг по ключевому слову.
        """
        if (self.has_book_data() == False):
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        keyword = input("Введите ключевое слово для поиска: ")
        if not keyword:
            print("Ошибка: Ключевое слово не может быть пустым.")
            self.wait_for_enter()
            return
        self.cursor.execute(self.search_books_query, ('%' + keyword + '%', '%' + keyword + '%'))
        books = self.cursor.fetchall()
        if books:
            print(f"Результаты поиска для '{keyword}':")
            for book in books:
                print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
        else:
            print(f"По запросу '{keyword}' ничего не найдено.")
        self.wait_for_enter()    
    def remove_book(self): 
        """
        Удаление книги из библиотеки по названию.
        """
        # Проверяем наличие данных о книгах в библиотеке
        if (self.has_book_data() == False):
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        # Выводим список книг для удаления
        self.cursor.execute(self.books_query)
        books = self.cursor.fetchall()
        
        print("Список книг:")
        for book in books:
            print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
        title = input("Введите название книги для удаления: ")
        if not title:
            print("Ошибка: Вы не указали название книги.")
            self.wait_for_enter()
            return    
        book_id = self.get_book_id_by_title(title)
        if book_id:
            self.cursor.execute(self.delete_book_query, (book_id,))
            self.conn.commit()
            print(f"Книга '{title}' успешно удалена.")
        else:
            print(f"Книга с названием '{title}' не найдена.")
        self.wait_for_enter()
        
    def wait_for_enter(self):
        input("Для продолжения нажмите Enter...")   