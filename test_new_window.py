import curses

menu = ['О нас', 'Услуги', 'Сертификаты', 'Мастера', 'Контакты', 'Выход']


def print_menu(stdscr, selected_row_idx):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	for idx, row in enumerate(menu):
		x = w//2 - len(row)//2
		y = h//2 - len(menu)//2 + idx
		if idx == selected_row_idx:
			stdscr.attron(curses.color_pair(1))
			stdscr.addstr(y, x, row)
			stdscr.attroff(curses.color_pair(1))
		else:
			stdscr.addstr(y, x, row)
	stdscr.refresh()


def print_center(stdscr, text):
	stdscr.clear()
	h, w = stdscr.getmaxyx()
	x = w//2 - len(text)//2
	y = h//2
	stdscr.addstr(y, x, text)
	stdscr.refresh()


def main(stdscr):
	# Выключение мигания курсора
	curses.curs_set(0)

	# Цвет текста и обводки
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

	# Выбор строки отображения при запуске
	current_row = 0

	# Вывод меню
	print_menu(stdscr, current_row)

	while 1:
		key = stdscr.getch()

		if key == curses.KEY_UP and current_row > 0:
			current_row -= 1
		elif key == curses.KEY_DOWN and current_row < len(menu)-1:
			current_row += 1
		elif key == curses.KEY_ENTER or key in [10, 13]:
			print_center(stdscr, "Вы выбрали '{}'".format(menu[current_row]))
			stdscr.getch()
			# При выборе последней строки выйти из программы
			if current_row == len(menu)-1:
				break

		print_menu(stdscr, current_row)


curses.wrapper(main)