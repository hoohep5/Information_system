#4 сущности user, procedure, master, salone. Каждая сущность поддерживает все следующие операции CRUD Create, read, update, delete.
# на каждый класс Dao
import keyboard
start = """
╭────────────────────────────╮
│  ┌───────┐ ┌────────────┐  │
│  │Sign in│ │Registration│  │
│  └───────┘ └────────────┘  │
╰────────────────────────────╯
"""
print(start)
signin_1 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Sign in                 │Back│  │
│                          └────┘  │
│  Login:
"""

signin_2 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Sign in                 │Back│  │
│                          └────┘  │
│  Login: login678901234567890     │
│  Pass:
"""

regist_1 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Registration            │Back│  │
│                          └────┘  │
│  Login:
"""

regist_2 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Registration            │Back│  │
│                          └────┘  │
│  Login: login678901234567890     │
│  Pass:
"""
while True:
    try:
        if keyboard.is_pressed('enter'):  # if key 'q' is pressed
            print(signin_1)
            break
    except:
        break