import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime


class SpaAppointmentApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Запись на процедуру")
        self.window.geometry("400x250")

        # Frame для выбора даты
        self.date_frame = ttk.Frame(self.window, padding=10)
        self.date_frame.pack(fill='x')

        ttk.Label(self.date_frame, text="Дата:").pack(side='left')
        self.date_picker = ttk.Combobox(self.date_frame, width=10)
        self.date_picker.pack(side='left')
        self.date_picker['values'] = self.get_dates()
        self.date_picker.current(0)

        # Frame для выбора времени
        self.time_frame = ttk.Frame(self.window, padding=10)
        self.time_frame.pack(fill='x')

        ttk.Label(self.time_frame, text="Время:").pack(side='left')
        self.time_picker = ttk.Combobox(self.time_frame, width=10)
        self.time_picker.pack(side='left')
        self.time_picker['values'] = self.get_times()
        self.time_picker.current(0)

        # Frame для выбора процедуры
        self.service_frame = ttk.Frame(self.window, padding=10)
        self.service_frame.pack(fill='x')

        ttk.Label(self.service_frame, text="Процедура:").pack(side='left')
        self.service_picker = ttk.Combobox(self.service_frame, width=20)
        self.service_picker.pack(side='left')
        self.service_picker['values'] = ['Массаж', 'Пилинг', 'Маска']
        self.service_picker.current(0)

        # Кнопка для отправки запроса на сервер
        self.submit_button = ttk.Button(self.window, text="Записаться", command=self.submit_appointment)
        self.submit_button.pack(pady=10)

    def get_dates(self):
        # Возвращает список дат на неделю вперед от сегодняшнего дня
        dates = []
        today = datetime.date.today()
        for i in range(7):
            date = today + datetime.timedelta(days=i)
            dates.append(date.strftime('%d.%m.%Y'))
        return dates

    def get_times(self):
        # Возвращает список временных интервалов
        return ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

    def submit_appointment(self):
        # Функция для отправки запроса на сервер
        date = self.date_picker.get()
        time = self.time_picker.get()
        service = self.service_picker.get()

        # Отправка запроса на сервер
        # ...

        messagebox.showinfo("Успех", "Вы успешно записались на процедуру.")
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = SpaAppointmentApp()
    app.run()
