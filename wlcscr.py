import urwid


class RegistrationWindow(urwid.WidgetWrap):
    def __init__(self):
        registration_text = urwid.Text("Форма регистрации")
        registration_button = urwid.Button("Зарегистрироваться")
        back_button = urwid.Button("Назад")

        urwid.connect_signal(registration_button, 'click', self.handle_registration_submit)
        urwid.connect_signal(back_button, 'click', self.handle_back_to_main)

        registration_widgets = urwid.Pile([registration_text, registration_button, back_button])
        registration_top = urwid.Filler(registration_widgets, valign='middle')

        super().__init__(registration_top)

    def handle_registration_submit(self, button):

        pass
        # Логика обработки данных регистрации
        # ...

    def handle_back_to_main(self, button):
        loop.widget = main_window


class MainWindow(urwid.WidgetWrap):
    def __init__(self):
        text = urwid.Text("Добро пожаловать!")
        register_button = urwid.Button("Регистрация")
        login_button = urwid.Button("Вход")

        urwid.connect_signal(register_button, 'click', self.handle_registration)
        # Добавьте обработчики событий для кнопок входа

        buttons = urwid.Pile([register_button, login_button])
        top = urwid.Filler(urwid.Pile([text, ('pack', buttons)]), valign='middle')

        super().__init__(top)

    @staticmethod
    def handle_registration(button):
        loop.widget = RegistrationWindow()


# Создание главного окна
main_window = MainWindow()

# Создание главного цикла
loop = urwid.MainLoop(main_window)
loop.run()

main_window.handle_registration(None)
