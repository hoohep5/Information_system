import curses

def main_menu(stdscr):

    # Очистить экран и скрыть курсор
    curses.curs_set(0)
    stdscr.clear()

    # Получить размер экрана
    height, width = stdscr.getmaxyx()

    # Создать новое окно
    menu_win = curses.newwin(height, width, 0, 0)

    # Вывести приветственное сообщение в окне
    menu_win.addstr(0, 0, "Добро пожаловать!")
    menu_win.addstr(2, 0, "Выберите действие:")

    # Создать список опций
    options = ["1. Регистрация", "2. Вход"]

    # Вывести опции в окне
    for i in range(len(options)):
        menu_win.addstr(i+4, 0, options[i])

    # Получить выбор пользователя
    choice = None
    while choice not in ["1", "2"]:
        choice = stdscr.getkey()

    # Очистить экран и вернуть выбор пользователя
    stdscr.clear()
    return choice

# Инициализировать curses и запустить главное меню
curses.wrapper(main_menu)
