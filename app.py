import tkinter as tk
from tkinter import ttk
import sqlite3
from tkcalendar import DateEntry
import bd as ex
import tkinter.messagebox as mb

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Финансист')
        self.style = ttk.Style()
        self.style.configure('alina', font=('Helvetica', 13, 'bold'), padding=(0, 10, 0, 10))
        self['background'] = '#E6E6FA'
        self.conf = {'padx':10, 'pady':10}
        self.bold_font = 'Helvetica 13 bolt'
        self.put_frames()

    def put_frames(self):
        self.frame_instruction = Instruction(self).grid(row=0, column=0, sticky="nswe")
        self.frame_setting = Setting(self).grid(row=0, column=1, sticky="nswe")
        self.frame_grafic = Plus(self).grid(row=1, column=0, sticky="nswe")
        self.frame_plus = Grafic(self).grid(row=1, column=1, sticky="nswe")

    def refresh(self):
        all_frames = [f for f in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_frames()

class Instruction(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.put_widgets()

    def put_widgets(self):
        self.label_name = tk.Label(self, text="Инструкция")
        self.lx = tk.Label(self, text="Данное финанасовое приложение создано для внесения")
        self.lx1 = tk.Label(self, text="ваших ежедневных трат. Поле 'Настройки' позволяет")
        self.lx2 = tk.Label(self, text="удалить ненужную сферу или удалить последний ввод")
        self.lx3 = tk.Label(self, text="суммы за какую-то определеннную дату. А делается")
        self.lx4 = tk.Label(self, text="это через специальное поле. Внесение расходов-")
        self.lx5 = tk.Label(self, text="вы вносите свои расходы, выбирая соответсвующие")
        self.lx6 = tk.Label(self, text="поля с датой, суммой и сферой расходов.")
        self.lx7 = tk.Label(self, text='В поле "Отчет" необходимо поставить дату, за которую')
        self.lx8 = tk.Label(self, text='Вам нужна статистика. А после нажать на кнопку обнов-')
        self.lx9 = tk.Label(self, text='ления результатов. Данные обновятся на текущие.')
        self.lx10 = tk.Label(self, text='Не забудьте, что дата начала периода должна быть мень-')
        self.lx11 = tk.Label(self, text='ше даты конца. А также нажатием на специальную кнопку')
        self.lx12 = tk.Label(self, text='вы можете получить график по заданному периоду. Удачи!')
        self.lx13 = tk.Label(self, text='❤❤❤')

        self.label_name.grid(row=0, columnspan=2, sticky="n")
        self.lx.grid(row=1, column=0, sticky="w", padx=10)
        self.lx1.grid(row=2, column=0, sticky="w", padx=10)
        self.lx2.grid(row=3, column=0, sticky="w", padx=10)
        self.lx3.grid(row=4, column=0, sticky="w", padx=10)
        self.lx4.grid(row=5, column=0, sticky="w", padx=10)
        self.lx5.grid(row=6, column=0, sticky="w", padx=10)
        self.lx6.grid(row=7, column=0, sticky="w", padx=10)
        self.lx7.grid(row=9, column=0, sticky="w",padx=10)
        self.lx8.grid(row=10, column=0, sticky="w",padx=10)
        self.lx9.grid(row=11, column=0, sticky="w", padx=10)
        self.lx10.grid(row=12, column=0, sticky="w", padx=10)
        self.lx11.grid(row=13, column=0, sticky="w", padx=10)
        self.lx12.grid(row=14, column=0, sticky="w", padx=10)
        self.lx13.grid(row=15, column=0, sticky="n", padx=10)

class Setting(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = self.master['background']
        self.items = ex.form_plus()
        self.put_widgets()

    def put_widgets(self):
        self.lab = tk.Label(self, text="Настройки")
        self.lab3 = ttk.Label(self, text="Выберите сферу удаления: ")
        self.lab4 = ttk.Combobox(self, values=self.items['names'])
        self.lab5 = ttk.Label(self, text="Удалить последний ввод во вкладке Внесение расходов:")
        self.batt_del = ttk.Button(self, text="Удалить сферу расходов", command=self.form_del_sfere)
        self.batt2 = ttk.Button(self, text="Удалить данные", command=self.form_del)
        self.labaa = ttk.Label(self, text="Внести новую сферу:")
        self.text = tk.Entry(self, textvariable=tk.StringVar())
        self.batt = ttk.Button(self, text="Внести новую сферу", command=self.new_sfere)

        self.lab.grid(row=0, column=0, columnspan=2, sticky="n")
        self.lab3.grid(row=3, column=0, sticky="e", padx=10, pady=10)
        self.lab4.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        self.batt_del.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.lab5.grid(row=5, column=0, columnspan=2, sticky="nswe", padx=10, pady=10)
        self.batt2.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.labaa.grid(row=7, column=0, sticky="e", padx=10, pady=10)
        self.text.grid(row=7, column=1, sticky="w", padx=10, pady=10)
        self.batt.grid(row=8, column=0, columnspan=2, padx=10, pady=10)


    def new_sfere(self):
        flag = True
        if str(self.text.get()) != "":
            try:
                int(self.text.get())
            except ValueError:
                a = str(self.text.get())
                if ex.new_sfere(a):
                    self.master.refresh()
                    return flag
            self.bell()
            self.show_error3()
        else:
            self.bell()
            self.show_error3()


    def show_error(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Необходимо внести новые сферы для возможности удаления."
        mb.showerror("Ошибка", msg)
    def show_error1(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Необходимо выбрать сферу в поле для удаления."
        mb.showerror("Ошибка", msg)
    def show_error2(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Вы удалили данные допустимое число раз, введите новые для продолжения удаления"
        mb.showerror("Ошибка", msg)
    def show_error3(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Проверьте поле ввода сферы. Вы явно допустили ошибку."
        mb.showerror("Ошибка", msg)

    def form_del(self):
        if ex.form_del():
            self.master.refresh()
        else:
            self.bell()
            self.show_error2()

    def form_del_sfere(self):
        amount = str(self.lab4.get())
        if amount == "":
            self.bell()
            self.show_error1()
        elif ex.form_del_sfere(amount):
            self.master.refresh()
        else:
            self.bell()
            self.show_error()

class Plus(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#F08080'
        self.items = ex.form_plus()
        self.put_widgets()

    def put_widgets(self):
        self.choose0 = ttk.Label(self, text="Внесение расходов")
        self.choose = ttk.Label(self, text="Выбери сферу расходов:")
        self.choose1 = ttk.Combobox(self, values=self.items['names'])
        self.choose2 = ttk.Label(self, text="Внесите сумму платежа:")
        self.choose3 = ttk.Entry(self, justify=tk.RIGHT, validate="key", validatecommand=(self.register(self.validation_am), '%P'))
        self.choose4 = ttk.Label(self, text="Выберите дату платежа:")
        self.choose5 = DateEntry(self, date_pattern='dd-mm-YYYY')
        self.btn = ttk.Button(self, text="Сохранить", command=self.form_submit)
        self.grafic = ttk.Button(self, text="Показать график", command=self.grafic)


        self.choose0.grid(row=0, columnspan=2, sticky="n")
        self.choose.grid(row=1, column=0, sticky="w", cnf=self.master.conf)
        self.choose1.grid(row=1, column=1, sticky="e", cnf=self.master.conf)
        self.choose2.grid(row=2, column=0, sticky="w", cnf=self.master.conf)
        self.choose3.grid(row=2, column=1, sticky="e", cnf=self.master.conf)
        self.choose4.grid(row=3, column=0, sticky="w", cnf=self.master.conf)
        self.choose5.grid(row=3, column=1, sticky="e", cnf=self.master.conf)
        self.btn.grid(row=4, column=0, columnspan=2, cnf=self.master.conf)
        self.grafic.grid(row=9, column=0, columnspan=2, sticky="nswe", padx=10, pady=40)

    def grafic(self):
        if ex.grafic_return == False:
            self.bell()
        else:
            ex.grafic_return()

    def show_error(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Заполните все поля для ввода данных корректными данными."
        mb.showerror("Ошибка", msg)

    def show_error1(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Данной сферы нет в списке. Сначала внесите ее в поле ввода новой сферы."
        mb.showerror("Ошибка", msg)

    def validation_am(self, input):
        try:
            x = float(input)
            return True
        except ValueError:
            self.show_error()
            self.bell()
            return False

    def form_submit(self):
        flag = True
        print(self.choose5.get())
        payment_date = ex.get_timestamp_sting(self.choose5.get())
        try:
            expense_id = self.items['ac'][self.choose1.get()]
            amount = float(self.choose3.get())
        except KeyError or UnboundLocalError:
            if self.choose1.get() != '':
                pass
            else:
                flag = False
                self.bell()
                self.show_error()
        except ValueError:
            flag = False
            self.bell()
            self.show_error1()
        try:
            print(payment_date)
            insert_payments = (amount, payment_date, expense_id)
        except UnboundLocalError:
            flag = False
            self.bell()
            self.show_error1()
        if flag:
            insert_payments = (amount, payment_date, expense_id)
            if ex.insert_payments(insert_payments):
                self.master.refresh()
        else:
            flag = False

class Grafic(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self['background'] = '#40E0D0'
        self.put_widgets()

    def put_widgets(self):
        self.label_name = tk.Label(self, text="Отчет")
        self.label1_text = tk.Label(self, text="Самая затратная сфера:")

        self.label1_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.label1_value.grid(row=1, column=1, sticky="e", padx=10, pady=10)
        self.label3_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.label3_text = tk.Label(self, text="Самый затратный день:")
        self.label2_text = tk.Label(self, text="Сумма расходов по этой сфере:")
        self.label2_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.label4_text = tk.Label(self, text="Самый затратный месяц за весь период:")
        self.label4_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.label5_text = tk.Label(self, text="В этот день потрачено:")
        self.label5_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.label6_text = tk.Label(self, text="Самая часто встречающаяся сфера:")
        self.label6_value = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.filter1 = DateEntry(self, date_pattern='dd-mm-YYYY')
        self.filter2 = DateEntry(self, date_pattern='dd-mm-YYYY')
        self.bitbit1 = tk.Label(self, text="Средняя сумма расходов")
        self.bitbit2 = tk.Label(self, text="Нажми на кнопку", font="Calibri 12 bold")
        self.botton_chop = ttk.Button(self, text="Фильтровать данные", command=self.date_proverka)


        self.label_name.grid(row=0, columnspan=2, sticky="n")
        self.filter1.grid(row=7, column=0, sticky="w", padx=10, pady=10)
        self.filter2.grid(row=7, column=1, sticky="e", padx=10, pady=10)
        self.label1_text.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.label2_text.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.label2_value.grid(row=2, column=1, sticky="e", padx=10, pady=10)
        self.label3_text.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.label3_value.grid(row=3, column=1, sticky="e", padx=10, pady=10)
        self.label5_text.grid(row=4, column=0, sticky="w", padx=10, pady=10)
        self.label5_value.grid(row=4, column=1, sticky="e", padx=10, pady=10)
        self.label4_text.grid(row=5, column=0, sticky="w", padx=10, pady=10)
        self.label4_value.grid(row=5, column=1, sticky="e", padx=10, pady=10)
        self.label6_text.grid(row=6, column=0, sticky="w", padx=10, pady=10)
        self.label6_value.grid(row=6, column=1, sticky="e", padx=10, pady=10)
        self.bitbit1.grid(row=8, column=0, sticky="w", padx=10, pady=10)
        self.bitbit2.grid(row=8, column=1, sticky="e", padx=10, pady=10)
        self.botton_chop.grid(row=9, columnspan=2, cnf=self.master.conf)

    def show_error(self):
        btn_error = tk.Button(self, text="Окно с ошибкой", command=self.show_error)
        msg = "Данных по данным датам не существует. Проверьте, чтобы дата начала периода была меньше даты конца периода."
        mb.showerror("Ошибка", msg)

    def date_proverka(self):
        d = ex.get_timestamp_sting(self.filter1.get())
        a = ex.get_timestamp_sting(self.filter2.get())
        if d <= a:
            ex.date_proverka(ex.get_timestamp_sting(self.filter1.get()), ex.get_timestamp_sting(self.filter2.get()))
            count = ex.srednii(d, a)
            self.bitbit2.destroy()
            self.bitbit2 = tk.Label(self, text=f"{count}", font="Calibri 12 bold")
            self.bitbit2.grid(row=8, column=1, sticky="e", padx=10, pady=10)
            self.label6_value.destroy()
            self.label6_value = tk.Label(self, text=ex.get_most_common_item(), font="Calibri 12 bold")
            self.label6_value.grid(row=6, column=1, sticky="e", padx=10, pady=10)
            self.label2_value.destroy()
            self.label2_value = tk.Label(self, text=ex.alina(), font="Calibri 12 bold")
            self.label2_value.grid(row=2, column=1, sticky="e", padx=10, pady=10)
            self.label3_value.destroy()
            self.label3_value = tk.Label(self, text=ex.get_most_expens_day(), font="Calibri 12 bold")
            self.label3_value.grid(row=3, column=1, sticky="e", padx=10, pady=10)
            self.label1_value.destroy()
            self.label1_value = tk.Label(self, text=ex.get_most_expens_item(), font="Calibri 12 bold")
            self.label1_value.grid(row=1, column=1, sticky="e", padx=10, pady=10)
            self.label4_value.destroy()
            self.label4_value = tk.Label(self, text=ex.get_most_exp_month(), font="Calibri 12 bold")
            self.label4_value.grid(row=5, column=1, sticky="e", padx=10, pady=10)
            self.label5_value.destroy()
            self.label5_value = tk.Label(self, text=ex.get_most_expens_day_summ(), font="Calibri 12 bold")
            self.label5_value.grid(row=4, column=1, sticky="e", padx=10, pady=10)
        else:
            self.show_error()
            self.bell()

app = App()
app.resizable(width=False, height=False)
app.mainloop()

