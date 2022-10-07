import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QLineEdit
from ui1 import *
import db_2 as db
from check_db import *
from instruction import Ui_FINANCIER
from glavn import Ui_main
import codecs
from setting import Ui_setting
from payments import Ui_Payments
from otchet import Ui_Otchet

class Authorization(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_authorization()
        self.ui.setupUi(self)

        self.editor = self.ui.lineEdit
        self.editor.setEchoMode(QLineEdit.Password)
        self.ui.pushButton.clicked.connect(self.auth)
        self.ui.pushButton_2.clicked.connect(self.reg)
        self.base_line_edit = [self.ui.lineEdit_2, self.ui.lineEdit]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_f)


    def check_input(funct):
        def wrapper(self):
            for line_edit_2 in self.base_line_edit:
                if len(line_edit_2.text()) == 0:
                    return
            funct(self)
        return wrapper

    def signal_f(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)
        if value == "Успешно" or value == "Вы успешно зарегистрированы!":
            self.ui.lineEdit_2.clear()
            self.ui.lineEdit.clear()
            open1()

    @check_input
    def auth(self):
        name = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()
        self.check_db.thr_login(name, password)

    @check_input
    def reg(self):
        name = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()
        self.check_db.thr_register(name, password)


def open1():
    mywin.close()
    global Window
    Window = QtWidgets.QWidget()
    ui = Ui_main()
    ui.setupUi(Window)
    Window.show()

    def back():
        Window.close()
        mywin.show()

    ui.pushButton_2.clicked.connect(payments)
    ui.pushButton.clicked.connect(setting)
    ui.pushButton_4.clicked.connect(instruction)
    ui.pushButton_3.clicked.connect(otchet)
    ui.pushButton_5.clicked.connect(back)

'''def closeEvent(event):
        reply = QMessageBox.question(Authorization(), 'Вопрос', 'Вы уверены, что хотите выйти?',
                QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
                event.accept()
        else:
            event.ignore()'''

def instruction():
    global exampleApp
    exampleApp = QtWidgets.QWidget()
    ui = Ui_FINANCIER()
    ui.setupUi(exampleApp)
    Window.close()
    exampleApp.show()

    def new():
        exampleApp.close()
        Window.show()

    ui.pushButton_2.clicked.connect(new)

def otchet():
    global otc
    otc = QtWidgets.QWidget()
    ui = Ui_Otchet()
    ui.setupUi(otc)
    Window.close()
    otc.show()

    def main_open():
        otc.close()
        Window.show()

    def show_error():
        QtWidgets.QMessageBox.about(Authorization(), 'Оповещение',
        "Данных по данным датам не существует. Проверьте, чтобы дата начала периода была меньше даты конца периода.")

    def date_proverka():
        d = db.get_timestamp_sting(ui.dateEdit.text())
        a = db.get_timestamp_sting(ui.dateEdit_2.text())
        if d <= a:
            ui.lineEdit_13.setText(str(db.srednii(d, a))) #средняя сумма расходов
            ui.lineEdit_8.setText(str(db.get_most_expens_item(d, a)))  #самая затратная сфера
            ui.lineEdit_5.setText(str(db.alina())) #сумма расходов по сфере
            ui.lineEdit_9.setText(str(db.get_most_expens_day_summ(d, a))) #сумма расходов по самому затратному дню
            ui.lineEdit_10.setText(str(db.get_most_expens_day(d, a)))  # самый затратный день
        else:
            show_error()

    def grafic():
        if db.krug(1) != "НЕТ ДАННЫХ":
            db.krug(0)
        else:
            QtWidgets.QMessageBox.about(Authorization(), 'Оповещение',
                                            'Данные отсутствуют - внесите первый платеж.')

    def grafic_1():
        d = db.get_timestamp_sting(ui.dateEdit.text())
        a = db.get_timestamp_sting(ui.dateEdit_2.text())
        if d <= a:
            if db.grafic_return(d, a) != "НЕТ ДАННЫХ":
                    db.grafic_return(d, a)
            else:
                QtWidgets.QMessageBox.about(Authorization(), 'Оповещение',
                                            'Данные отсутствуют')
        else:
            show_error()


    ui.lineEdit_12.setText(str(db.get_most_exp_month()))  # самый затратный месяц
    ui.pushButton_3.clicked.connect(main_open) #открытие меню
    ui.pushButton_4.clicked.connect(date_proverka) #фильтрация
    ui.pushButton_5.clicked.connect(grafic) #график за весь период
    ui.pushButton_6.clicked.connect(grafic_1) #график за пользоват. период

def payments():
    global alina
    alina = QtWidgets.QWidget()
    ui = Ui_Payments()
    ui.setupUi(alina)
    Window.close()
    alina.show()

    def close_pay():
        alina.close()
        Window.show()

    def validation_am():
        x = ui.lineEdit.text()
        try:
            float(x)
            form_submit()
            payment_date = ui.dateEdit.text()
        except ValueError:
            ui.lineEdit.clear()
            show_error()

    def form_submit():
        flag = True
        items = db.form_plus()
        payment_date = db.get_timestamp_sting(ui.dateEdit.text())
        appa = ui.comboBox.currentText()
        #print(appa)
        #utf = appa.encode('unicode-escape').decode('utf-8')
        #print(utf)
        try:
            expense_id = items['ac'][appa]
            amount = float(ui.lineEdit.text())
            if amount <= 0:
                show_error9()
                ui.lineEdit.clear()
                flag = False
        except KeyError or UnboundLocalError:
            if ui.comboBox.currentText() != '':
                pass
            else:
                flag = False
                show_error()
        except ValueError:
            flag = False
            show_error1()
        try:
            l = db.obrabotka()
            insert_payments = (amount, payment_date, expense_id, l)
        except UnboundLocalError:
            flag = False
            show_error1()
        if flag:
            l = db.obrabotka()
            insert_payments = (amount, payment_date, expense_id, l)
            if db.insert_payments(insert_payments):
                QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Платеж сохранен")
                ui.lineEdit.clear()
                #master.refresh()
        else:
            flag = False

    def show_error():
        QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Заполните все поля для ввода данных корректными данными.")

    def show_error1():
        QtWidgets.QMessageBox.about(Authorization(), 'Оповещение',
                                    "Данной сферы нет в списке. Сначала внесите ее в поле ввода новой сферы.")

    comp = db.form_plus()
    ui.comboBox.addItems(comp['names'])
    ui.pushButton_2.clicked.connect(validation_am)
    ui.pushButton_3.clicked.connect(close_pay)

def setting():
    global set
    set = QtWidgets.QWidget()
    ui = Ui_setting()
    ui.setupUi(set)
    Window.close()
    set.show()

    def close():
        set.close()
        Window.show()

    def inp():
        flag = True
        text = ui.lineEdit.text()
        if str(text) != "":
            try:
                int(text)
            except ValueError:
                a = str(text)
                if db.new_sfere(a):
                    ui.comboBox.clear()
                    items = db.form_plus()
                    ui.comboBox.addItems(items['names'])
                    print(items['names'])
                    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Сфера сохранена.")
                    ui.lineEdit.clear()
                    return flag
                else:
                    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Такая сфера уже есть.")
                    return flag
            show_error3()
        else:
            #bell()
            show_error3()

    def form_del_sfere():
        amount = str(ui.comboBox.currentText())
        if amount == "":
            show_error1()
        elif db.form_del_sfere(amount):
            ui.comboBox.clear()
            items = db.form_plus()
            ui.comboBox.addItems(items['names'])
            QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Сфера успешно удалена.")
        else:
            show_error()
            #bell()

    items = db.form_plus()
    ui.comboBox.addItems(items['names'])
    ui.pushButton_3.clicked.connect(form_del)
    ui.pushButton_2.clicked.connect(close)
    ui.pushButton_6.clicked.connect(form_del_sfere)
    ui.pushButton_7.clicked.connect(inp)

def form_del():
    if db.form_del():
        QtWidgets.QMessageBox.about(Authorization(),'Оповещение', "Платеж удален.")
    else:
        show_error2()

def show_error3():
    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Проверьте поле ввода сферы. Вы явно допустили ошибку.")

def show_error():
    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Необходимо внести новые сферы для возможности удаления.")

def show_error1():
    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Необходимо выбрать сферу в поле для удаления.")

def show_error9():
    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Внесите платеж больше 0")

def show_error2():
    QtWidgets.QMessageBox.about(Authorization(), 'Оповещение', "Вы удалили данные допустимое число раз, введите новые для продолжения удаления")

app = QtWidgets.QApplication(sys.argv)
mywin = Authorization()
mywin.show()
sys.exit(app.exec_())


