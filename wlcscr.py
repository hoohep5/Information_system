import urwid


def handle_key(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()


# Создание виджетов
text = urwid.Text("Добро пожаловать!")
register_button = urwid.Button("Регистрация")
login_button = urwid.Button("Вход")

# Обработчики событий
urwid.connect_signal(register_button, 'click', handle_key)
urwid.connect_signal(login_button, 'click', handle_key)

# Создание виджета для компоновки
buttons = urwid.Pile([register_button, login_button])
top = urwid.Filler(urwid.Pile([text, ('pack', buttons)]), valign='middle')

# Создание главного окна
loop = urwid.MainLoop(top, unhandled_input=handle_key)
loop.run()
