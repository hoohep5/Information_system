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
    @staticmethod
    def printTextWindow(text):
        print("╭", "─"*(len(text)+2), "╮", sep = "")
        print("│", text, "│")
        print("╰", "─" * (len(text)+2), "╯", sep = "")
    def printBasicWindow(length, width, back, title, list):
        print("╭", "─"*(length - 2), "╮", sep = "")
        isTitled = False
        if back:
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 6), "┌────┐", "│", sep = "")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 7), "┌────┐", "│", sep = "")
            print("│", " " * (length - 8), "│Back│", "│", sep = "")
            print("│", " " * (length - 8), "└────┘", "│", sep = "")
            width -= 3
            isTitled = True
        if isTitled:
            for j in list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
        else:
            if (length % 2 == 0 and len(title) % 2 == 0) or (length % 2 != 0 and len(title) % 2 != 0):
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2), "│", sep = "")
            else:
                print("│", " " * ((length - len(title) - 1) // 2), title, " " * ((length - len(title) - 1) // 2 - 1), "│", sep = "")
            for j in list:
                print("│", j, " " * ((length - 5) - len(j)), "│")
        print("╰", "─" * (length - 2), "╯", sep = "")

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
        return login, password


#Window.printBasicWindow(35, 3, False, "Добро пожаловать!", salons)
#Window.printTextWindow("Hello!")
#Window.printSignIn(35, 3)

