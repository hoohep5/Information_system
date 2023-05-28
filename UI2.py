import curses

HOST = "127.0.0.1"
PORT = 65432

class ConsoleUI:
    def __init__(self):
        self.options = ["Запись на процедуру", "Option 2", "Option 3"]
        self.selected_option = 0

    def run(self):
        curses.wrapper(self._run_curses)

    def send_reqest(self, client_socket, reqest):
        pass

    def _run_curses(self, stdscr):
    # Настройка библиотеки
        # не отображаются вводимые символы
        curses.noecho()
        # данные напрямую идут в консоль после каждого нажатия
        curses.cbreak()
        stdscr.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Main loop
        while True:
            # Меню отрисовки
            stdscr.clear()
            for i, option in enumerate(self.options):
                if i == self.selected_option:
                    stdscr.attron(curses.color_pair(1))
                else:
                    stdscr.attron(curses.color_pair(2))
                stdscr.addstr(i + 1, 1, option)
            stdscr.refresh()

            # Обработка того, что ввел пользователь
            key = stdscr.getch()
            if key == ord("w"):
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif key == ord("s"):
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                selected = self.options[self.selected_option]
                # Тут кнопки будут иметь какие то функции
                break

        # Заканчиваем работу
        curses.curs_set(1)
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


ui = ConsoleUI()
ui.run()
