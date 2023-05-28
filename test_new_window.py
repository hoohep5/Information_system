# import os
# import time
# import keyboard
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
procedures = ["massageyrtyrty", "z", "pilling", "massageyrtyrty", "z", "pilling"]
salons = ["svenlanskaya", "aleutskaya", "komsomolcskaya"]

class Window:
    # def __init__(self, frames, object1, object2, object3):
    #     self.frames = frames
    #     self.object1 = object1
    #     self.object2 = object2
    #     self.object3 = object3

    # Основное окно
    @staticmethod
    def printBasicWindow(length, width, back, title, list):
        print("╭", "─"*(length - 2), "╮", sep = "")
        isTitled = False # Наличие загаловка
        if back: # Проверка на наличие кнопки back
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 6), "┌────┐", "│", sep = "")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 7), "┌────┐", "│", sep = "")
            print("│", " " * (length - 8), "│Back│", "│", sep = "")
            print("│", " " * (length - 8), "└────┘", "│", sep = "")
            width -= 3
            isTitled = True
        if isTitled:
            # for i in range(width - 1, 1, -1):
            #     print("│", " " * (length - 2), "│", sep = "")
            for j in list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
        else:
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2), "│", sep = "")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 1), "│", sep = "")
            for j in list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
            # for i in range(width - 2, 1, -1):
            #     print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")

    # Окно регистрации
    def printSignIn(length, width):
        print("╭", "─" * (length - 2), "╮", sep = "")
        for i in range((width // 2) - 1, 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        if length % 2 == 0:
            print("│", " " * ((length - 14) // 2), "Введите логин", " " * ((length - 14) // 2 - 1), "│", sep = "")
            print("│", " " * ((length - 9) // 2), "и пароль", " " * ((length - 9)//2), "│", sep = "")
        else:
            print("│", " " * ((length - 14) // 2), "Введите логин", " " * ((length - 14) // 2), "│", sep = "")
            print("│", " " * ((length - 9) // 2), "и пароль", " " * ((length - 9) // 2 - 1), "│", sep = "")
        for i in range((width // 2) - 1, 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")
        login = input()
        password = input()

    # Приветственное окно
    def printWelcome(length, width):
        print("╭", "─" * (length - 2), "╮", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        if length % 2 == 0:
            print("│", " " * ((length - 18) // 2), "Добро пожаловать!", " " * ((length - 18) // 2 - 1), "│", sep = "")
        else:
            print("│", " " * ((length - 18) // 2), "Добро пожаловать!", " " * ((length - 18) // 2), "│", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")

    # Окно успешной регистрации
    def printRegistrated(length, width):
        print("╭", "─" * (length - 2), "╮", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        if length % 2 == 0:
            print("│", " " * ((length - 22) // 2), "Вы зарегистрировались", " " * ((length - 22) // 2 - 1), "│", sep = "")
        else:
            print("│", " " * ((length - 22) // 2), "Вы зарегистрировались", " " * ((length - 22) // 2), "│", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")

    # Ошибка: неверный пароль
    def printPasswordIncorrect(length, width):
        print("╭", "─" * (length - 2), "╮", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        if length % 2 == 0:
            print("│", " " * ((length - 17) // 2), "Пароль неверный!", " " * ((length - 17) // 2), "│", sep = "")
        else:
            print("│", " " * ((length - 17) // 2), "Пароль неверный!", " " * ((length - 17) // 2 - 1), "│", sep = "")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")

    # Ошибка: слишком длинный логин
    def printLoginTooLong(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 23) // 2), "Логин слишком длинный!", " " * ((length - 23) // 2), "│", sep="")
        else:
            print("│", " " * ((length - 23) // 2), "Логин слишком длинный!", " " * ((length - 23) // 2 - 1), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")

    # Ошибка: слишком длинный пароль
    def printPasswordTooLong(length, width):
        print("╭", "─" * (length - 2), "╮", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        if length % 2 == 0:
            print("│", " " * ((length - 24) // 2), "Пароль слишком длинный!", " " * ((length - 24) // 2 - 1), "│", sep="")
        else:
            print("│", " " * ((length - 24) // 2), "Пароль слишком длинный!", " " * ((length - 24) // 2), "│", sep="")
        for i in range((width // 2), 1, -1):
            print("│", " " * (length - 2), "│", sep="")
        print("╰", "─" * (length - 2), "╯", sep="")


Window.printWelcome(21, 3)
Window.printRegistrated(30, 3)
Window.printPasswordIncorrect(20, 3)
Window.printLoginTooLong(30, 3)
Window.printPasswordTooLong(30, 3)