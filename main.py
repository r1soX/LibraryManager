import os
from src.actions import actions

def main():
    """
    Основная функция управления библиотекой книг.
    """
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана
        print("Добро пожаловать в библиотеку!")
        for key, value in actions.items():  # Вывод доступных действий
            print(value["message"]) 
        choice = input("Выберите действие: ")

        action = actions.get(choice)  # Получение действия по ключу
        if action:
            action["action"]()  # Выполнение действия
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()