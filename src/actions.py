from src.library import Library
library = Library()  # Создаем объект класса Library
actions = { 
        "1": {
            "action": library.add_book,
            "message": "1. Добавить книгу" 
        },
        "2": {
            "action": library.display_books,
            "message": "2. Показать список книг"
        },
        "3": {
            "action": library.display_books_by_genre,
            "message": "3. Просмотр книг по жанру"
        },
        "4": {
            "action": library.search_books,
            "message": "4. Поиск книги"
        },
        "5": {
            "action": library.remove_book,
            "message": "5. Удалить книгу"
        },
        "6": {
            "action": lambda: exit(),
            "message": "6. Выход"
        },
    }