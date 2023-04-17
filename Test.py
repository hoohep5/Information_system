#4 сущности user, procedure, master, salone. Каждая сущность поддерживает все следующие операции CRUD Create, read, update, delete.
# на каждый класс Dao
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
print(signin_1)
signin_2 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Sign in                 │Back│  │
│                          └────┘  │
│  Login: login678901234567890     │
│  Pass:
"""
print(signin_2)
regist_1 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Registration            │Back│  │
│                          └────┘  │
│  Login:
"""
print(regist_1)
regist_2 = """
╭──────────────────────────────────╮
│                          ┌────┐  │
│  Registration            │Back│  │
│                          └────┘  │
│  Login: login678901234567890     │
│  Pass:
"""
print(regist_2)