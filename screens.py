import os
import time
import keyboard

welcome = """╭────────────────────────────╮
 │                            │
 │          Welcome!          │
 │                            │
 ╰────────────────────────────╯"""
sign_in_up = """╭──────────────────────────────╮
 │  ┌──────────┐  ┌──────────┐  │
 │  │Sign in(1)│  │Sign up(2)│  │
 │  └──────────┘  └──────────┘  │
 ╰──────────────────────────────╯"""
sign_in = """╭──────────────────────────────────╮
 │                          ┌────┐  │
 │  Sign in                 │Back│  │
 │                          └────┘  │
 │  Login:"""
sign_up = """╭──────────────────────────────────╮
 │                          ┌────┐  │
 │  Sign up                 │Back│  │
 │                          └────┘  │
 │  Login:"""

os.system('cls')
print(welcome)
time.sleep(3)
os.system('cls')
print(sign_in_up)
while True:
    if keyboard.is_pressed('1'):
        os.system('cls')
        print(sign_in)
        time.sleep(2)
    elif keyboard.is_pressed('2'):
        os.system('cls')
        print(sign_up)
        time.sleep(2)
