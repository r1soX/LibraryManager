from src.library import Library
library = Library()  # Создаем объект класса Library
actions = { 
        "1": {
            "action": library.add_book, # Добавляем книгу в библиотеку
            "message": "1. Добавить книгу" 
        },
        "2": {
            "action": library.display_books, # Показать список книг
            "message": "2. Показать список книг"
        },
        "3": {
            "action": library.display_books_by_genre, # Показать список книг по жанру
            "message": "3. Просмотр книг по жанру"
        },
        "4": {
            "action": library.search_books, # Поиск книги
            "message": "4. Поиск книги"
        },
        "5": {
            "action": library.remove_book, # Удалить книгу
            "message": "5. Удалить книгу"
        },
        "6": {
            "action": lambda: exit(), # Выход
            "message": "6. Выход"
        },
    }