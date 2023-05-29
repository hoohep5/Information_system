# import os
import time
import typing

#
# welcome = """╭────────────────────────────╮
#  │                            │
#  │          Welcome!          │
#  │                            │
#  ╰────────────────────────────╯"""
# sign_in_up = """╭──────────────────────────────╮
#  │  ┌──────────┐  ┌──────────┐  │
#  │  │Sign in(1)│  │Sign up(2)│  │
#  │  └──────────┘  └──────────┘  │
#  ╰──────────────────────────────╯"""
# sign_in = """╭──────────────────────────────────╮
#  │                          ┌────┐  │
#  │  Sign in                 │Back│  │
#  │                          └────┘  │
#  │  Login:"""
# sign_up = """╭──────────────────────────────────╮
#  │                          ┌────┐  │
#  │  Sign up                 │Back│  │
#  │                          └────┘  │
#  │  Login:"""
#
# os.system('cls')
# print(welcome)
# time.sleep(3)
# os.system('cls')
# print(sign_in_up)
# while True:
#     if keyboard.is_pressed('1'):
#         os.system('cls')
#         print(sign_in)
#         time.sleep(2)
#     elif keyboard.is_pressed('2'):
#         os.system('cls')
#         print(sign_up)
#         time.sleep(2)
procedures = ["massage", "piling", "footmassage", "mashotstone"]
salons = ["svenlanskaya", "aleutskaya", "komsomolcskaya"]
session = {"login": "", "password": "", "screen": 1}


# def manager(user_session: dict):
#     global user_input
#     match user_session["screen"]:
#         case 1:  # was welcom
#             user_session["screen"] = 2
#             return Window.print_welcome(20,3)
#         case 2:
#             user_session["screen"] = 3
#             return Window.print_sign_in(20,3)
#         case 3:
#             user_session["screen"] = 4
#             return Window.print_basic_window(length=40, width=20, back=True, title="Выберите процедуру", received_list=procedures, inp_data=True)
class Window:
    # def __init__(self, frames, object1, object2, object3):
    #     self.frames = frames
    #     self.object1 = object1
    #     self.object2 = object2
    #     self.object3 = object3

    # Основное окно
    @staticmethod
    def print_basic_window(*, length: int, width: int, back: bool, title: str, received_list: list, inp_data: bool):
        global user_input
        print("╭", "─" * (length - 2), "╮", sep="")
        is_titled = False  # Наличие заголовка
        if back:  # Проверка на наличие кнопки back
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 6),
                      "┌────┐", "│", sep="")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 7),
                      "┌────┐", "│", sep="")
            print("│", " " * (length - 8), "│Back│", "│", sep="")
            print("│", " " * (length - 8), "└────┘", "│", sep="")
            width -= 3
            is_titled = True
        if is_titled:
            # for i in range(width - 1, 1, -1):
            #     print("│", " " * (length - 2), "│", sep = "")
            for j in received_list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
        else:
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2), "│",
                      sep="")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 1),
                      "│", sep="")
            for j in received_list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
            # for i in range(width - 2, 1, -1):
            #     print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Окно регистрации
    @staticmethod
    def print_sign_in(length, width):
        global session
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2) - 1, 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 14) // 2), "Введите логин", " " * ((length - 14) // 2 - 1), "│", sep="")
            print("│", " " * ((length - 9) // 2), "и пароль", " " * ((length - 9) // 2), "│", sep="")
        else:
            print("│", " " * ((length - 14) // 2), "Введите логин", " " * ((length - 14) // 2), "│", sep="")
            print("│", " " * ((length - 9) // 2), "и пароль", " " * ((length - 9) // 2 - 1), "│", sep="")
        for i in range((width // 2) - 1, 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")
        session["login"] = input()
        session["password"] = input()

    # Приветственное окно
    @staticmethod
    def print_welcome(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 18) // 2), "Добро пожаловать!", " " * ((length - 18) // 2 - 1), "│", sep="")
        else:
            print("│", " " * ((length - 18) // 2), "Добро пожаловать!", " " * ((length - 18) // 2), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Окно успешной регистрации
    @staticmethod
    def print_registrated(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 22) // 2), "Вы зарегистрировались", " " * ((length - 22) // 2 - 1), "│", sep="")
        else:
            print("│", " " * ((length - 22) // 2), "Вы зарегистрировались", " " * ((length - 22) // 2), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: неверный пароль
    @staticmethod
    def print_password_incorrect(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 17) // 2), "Пароль неверный!", " " * ((length - 17) // 2), "│", sep="")
        else:
            print("│", " " * ((length - 17) // 2), "Пароль неверный!", " " * ((length - 17) // 2 - 1), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: слишком длинный логин
    @staticmethod
    def print_login_too_long(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 23) // 2), "Логин слишком длинный!", " " * ((length - 23) // 2), "│", sep="")
        else:
            print("│", " " * ((length - 23) // 2), "Логин слишком длинный!", " " * ((length - 23) // 2 - 1), "│",
                  sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: слишком длинный пароль
    @staticmethod
    def print_password_too_long(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 24) // 2), "Пароль слишком длинный!", " " * ((length - 24) // 2 - 1), "│",
                  sep="")
        else:
            print("│", " " * ((length - 24) // 2), "Пароль слишком длинный!", " " * ((length - 24) // 2), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: время занято
    @staticmethod
    def print_time_is_busy(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 22) // 2), "Это время уже занято!", " " * ((length - 22) // 2 - 1), "│", sep="")
        else:
            print("│", " " * ((length - 22) // 2), "Это время уже занято!", " " * ((length - 22) // 2), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: введено неверное слово
    @staticmethod
    def print_input_error(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 13) // 2), "Ошибка ввода", " " * ((length - 13) // 2), "│", sep="")
        else:
            print("│", " " * ((length - 13) // 2), "Ошибка ввода", " " * ((length - 13) // 2 - 1), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")


# while True:
#     foo = manager(session)
#     if session["screen"] == 0:
#         exit(0)
#     user_input = input()


# определяем список экранов
screens = [1, 2, 3]

# определяем переменную для хранения текущего индекса экрана
current_screen = 0

while True:
    # выводим текущий экран
    print(screens[current_screen])

    # запрашиваем ввод пользователя
    user_input = input(" ")

    if user_input == "back":
        # если пользователь ввел "back", то уменьшаем индекс экрана на 1
        current_screen -= 1
    else:
        # если пользователь ввел что-то другое или ничего не ввел, то увеличиваем индекс экрана на 1
        current_screen += 1

    # проверяем, чтобы индекс экрана не выходил за границы списка
    if current_screen < 0:
        current_screen = 0
    elif current_screen >= len(screens):
        # если достигли конца списка, то завершаем программу
        print("Program finished.")
        break

# Window.print_welcome(20, 3)
# time.sleep(1)
# Window.print_sign_in(30, 6)
# Window.print_basic_window(length=40, width=20, back=True, title="Выберите процедуру", received_list=procedures, inp_data=True)
