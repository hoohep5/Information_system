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


class Window:
    # def __init__(self, frames, object1, object2, object3):
    #     self.frames = frames
    #     self.object1 = object1
    #     self.object2 = object2
    #     self.object3 = object3
    @staticmethod
    def printframes(length, width, back):
        print("╭", "─"*(length-2), "╮", sep = "")
        if back:
            print("│", " " * (length - 8), "┌────┐", "│", sep = "")
            print("│", " " * (length - 8), "│Back│", "│", sep = "")
            print("│", " " * (length - 8), "└────┘", "│", sep = "")
            width -= 3
        for i in range(width-1, 1, -1):
            print("│", " " * (length - 2), "│", sep = "")
        print("╰", "─" * (length - 2), "╯", sep = "")


Window.printframes(25, 10, False)
