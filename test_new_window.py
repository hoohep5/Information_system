import curses


class MenuDisplay:

    def __init__(self, menu):
        self.menu = menu
        curses.wrapper(self.mainloop)

    def mainloop(self, stdscr):
        # Выключение мигание курсора
        curses.curs_set(0)

        # Цвета выделения
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.stdscr = stdscr

        # Высота и ширина текста
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()

        # Выбранная строка при запуске
        current_row = 0

        self.print_menu(current_row)

        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.print_center("Вы выбрали '{}'".format(self.menu[current_row]))
                self.stdscr.getch()
                # При выборе последней строки переход на подтверждение выхода
                if current_row == len(self.menu) - 1:
                    if self.confirm("Вы уверены что хотите выйти?"):
                        break

            self.print_menu(current_row)

    def print_menu(self, selected_row_idx):
        self.stdscr.clear()
        for idx, row in enumerate(self.menu):
            x = self.screen_width // 2 - len(row) // 2
            y = self.screen_height // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                self.color_print(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def color_print(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    def print_confirm(self, selected="Да"):
        curses.setsyx(self.screen_height // 2 + 1, 0)
        self.stdscr.clrtoeol()

        y = self.screen_height // 2 + 1
        options_width = 10

        # Вывод да
        option = "Да"
        x = self.screen_width // 2 - options_width // 2 + len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        # Вывод нет
        option = "Нет"
        x = self.screen_width // 2 + options_width // 2 - len(option)
        if selected == option:
            self.color_print(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        self.stdscr.refresh()

    def confirm(self, confirmation_text):
        self.print_center(confirmation_text)

        current_option = "Нет"
        self.print_confirm(current_option)

        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_RIGHT and current_option == "Да":
                current_option = "Нет"
            elif key == curses.KEY_LEFT and current_option == "Нет":
                current_option = "Да"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return True if current_option == "Да" else False

            self.print_confirm(current_option)

    def print_center(self, text):
        self.stdscr.clear()
        x = self.screen_width // 2 - len(text) // 2
        y = self.screen_height // 2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()


if __name__ == "__main__":
    menu = ['О нас', 'Услуги', 'Сертификаты', 'Мастера', 'Контакты', 'Выход']
    MenuDisplay(menu)