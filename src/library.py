import sqlite3

class Library:
    """
    Класс, представляющий библиотеку книг.
    """
    def __init__(self):
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
        # Запрос для создания таблицы жанров, если она не существует
        create_genres_table_query = 'SELECT COUNT(*) FROM genres'
        # Запрос для добавления стандартных жанров, если они отсутствуют
        add_default_genres_query = 'INSERT INTO genres (name) VALUES (?)'

        # Проверяем, существует ли таблица жанров
        self.cursor.execute(create_genres_table_query)
        count = self.cursor.fetchone()[0]
        # Если таблица не существует, добавляем стандартные жанры
        if count == 0:
            self.cursor.executemany(add_default_genres_query, [
                ('Фантастика',), ('Детектив',), ('Роман',), ('Приключения',), ('Драма',)])
            self.conn.commit()

    def get_book_details(self, book_id: int):
        """
        Получение подробной информации о книге по её ID.
        :param book_id: ID книги.
        :return: Словарь с информацией о книге.
        """
        # Запрос для получения информации о книге по её ID
        get_book_details_query = 'SELECT books.id, books.title, books.author, books.description, genres.name FROM books JOIN genres ON books.genre_id = genres.id WHERE books.id = ?'
        # Получаем подробную информацию о книге по её ID
        self.cursor.execute(get_book_details_query, (book_id,))
        book = self.cursor.fetchone()
        return book

    def get_genres(self) -> list:
        """
        Получение списка всех жанров книг в библиотеке.
        :return: Список жанров книг в библиотеке.
        """
        # Запрос для получения списка всех жанров книг
        get_genres_query = 'SELECT name FROM genres'
        # Получаем список всех жанров книг в библиотеке
        self.cursor.execute(get_genres_query)
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
        # Получаем название, автора и описание книги из консоли
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
        # Проверяем, что жанр книги есть в базе данных
        if genre not in genres:
            self.cursor.execute(self.add_default_genres_query, (genre,))
            self.conn.commit()
        # Добавляем книгу в библиотеку
        self.cursor.execute(self.add_book_query, (title, author, description, genre)) 
        self.conn.commit()
        print(f"Книга {title} успешно добавлена в библиотеку.")
        self.wait_for_enter()

    def display_books(self): 
        """
        Отображение списка всех книг в библиотеке.
        """
        # Проверяем наличие данных о книгах в библиотеке
        if (self.has_book_data() == False): # Проверяем наличие данных о книгах в библиотеке
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        # Выводим список всех книг в библиотеке
        self.cursor.execute(self.books_query)
        books = self.cursor.fetchall()
        # Выводим информацию о книгах
        for book in books:
            print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}")
            
        # Получаем ID книги для просмотра подробной информации или завершаем работу
        book_id = input("Введите ID книги для просмотра подробной информации (или нажмите Enter для продолжения): ") 
        if not book_id:
            return
        # Проверяем, что введен ID книги
        if book_id:
            # Получаем подробную информацию о книге
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
        # Проверяем наличие данных о книгах в библиотеке
        if (self.has_book_data() == False):
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        # Вводим жанр для просмотра книг
        genre = input("Введите жанр для просмотра книг: ")
        # Проверяем, что жанр не пустой
        if not genre:
            print("Ошибка: Книг без жанров не существует.")
            self.wait_for_enter()
            return
        # Выполняем поиск книг по жанру
        self.cursor.execute(self.display_books_by_genre_query, (genre,))
        books = self.cursor.fetchall()
        # Выводим результаты поиска
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
        # Проверяем наличие данных о книгах в библиотеке
        if (self.has_book_data() == False):
            print("Библиотека пуста, добавьте книги.")
            self.wait_for_enter()
            return
        # Вводим ключевое слово для поиска
        keyword = input("Введите ключевое слово для поиска: ")
        # Проверяем, что ключевое слово не пустое
        if not keyword:
            print("Ошибка: Ключевое слово не может быть пустым.")
            self.wait_for_enter()
            return
        # Выполняем поиск книг по ключевому слову
        self.cursor.execute(self.search_books_query, ('%' + keyword + '%', '%' + keyword + '%'))
        books = self.cursor.fetchall()
        # Выводим результаты поиска
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
        # Проверяем, что название книги не пустое
        if not title:
            print("Ошибка: Вы не указали название книги.")
            self.wait_for_enter()
            return    
        # Получаем ID книги по названию
        book_id = self.get_book_id_by_title(title)
        # Если книга найдена, удаляем ее
        if book_id:
            self.cursor.execute(self.delete_book_query, (book_id,))
            self.conn.commit()
            print(f"Книга '{title}' успешно удалена.")
        else:
            print(f"Книга с названием '{title}' не найдена.")
        self.wait_for_enter()
        
    # Функция для ожидания нажатия Enter
    def wait_for_enter(self):
        input("Для продолжения нажмите Enter...")   