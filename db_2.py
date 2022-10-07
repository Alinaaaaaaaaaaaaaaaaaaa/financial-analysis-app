import datetime
import sqlite3
import matplotlib.pyplot as plt
import random as random
import codecs

v = ""
def login(login, password, signal):
    global v
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    a = login
    v = login
    obrabotka()
    querty = """SELECT * FROM autho WHERE login = (%a)"""%a
    cur.execute(querty)
    value = cur.fetchall()
    if value !=[] and value[0][2] == password:
        signal.emit('Успешно')
    else:
        signal.emit('Проверьте данные или зарегестрируйтесь')
    cur.close()
    con.close()

def register(login, password, signal):
    con = sqlite3.connect('database.db')
    global v
    cur = con.cursor()
    a = login
    querty = """SELECT * FROM autho WHERE login =(%a)"""%a
    cur.execute(querty)
    value = cur.fetchall()
    if value != []:
        signal.emit('Такой ник уже используется!')
    else:
        p = (login, password)
        querty = """INSERT INTO autho (login, password) VALUES (?, ?)"""
        cur.execute(querty, p)
        signal.emit('Вы успешно зарегистрированы!')
        v = login
        con.commit()
        obrabotka()
    cur.close()
    con.close()

def obrabotka():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    a = v
    querty = """SELECT id FROM autho WHERE login = (%a)""" %a
    cur.execute(querty)
    value = cur.fetchall()
    con.close()
    print(value[0][0])
    return value[0][0]

def grafic_return(d, a):
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        paymetsCursor = db.cursor()
        k = str(obrabotka())
        querty = """SELECT expense_id, SUM(amount) as amount from payments WHERE payments.users_id = (?) AND (?)<= payment_date AND payment_date <= (?) GROUP BY expense_id """
        paymetsCursor.execute(querty, (k, d, a))
        all_data = paymetsCursor
        if paymetsCursor.rowcount == 0:
            return "НЕТ ДАННЫХ"
        else:
            amount = {}
            for i in all_data:
                amount[i["expense_id"]] = i["amount"]
            if list(amount.values()) == [0.0] or list(amount.values()) == []:
                return "НЕТ ДАННЫХ"
            else:
                con = sqlite3.connect('database.db')
                cur = con.cursor()
                cursor = db.cursor()
                querry = """SELECT id, name from expenses where expenses.id_users = (?)"""
                q = obrabotka()
                k = (q,)
                cursor.execute(querry, k)
                cur.execute(querry, k)
                value = cur.fetchall()
                if value == [] or list(amount.values()) == []:
                    return "НЕТ ДАННЫХ"
                else:
                    result = {}
                    for item in cursor:
                        if item["id"] in amount.keys():
                            k = item["name"]
                            #p = codecs.decode(k, 'unicode-escape')
                            result[k] = amount[item["id"]]
                        else:
                            result[item["name"]] = 0
                    r, g, b = random.random(), random.random(), random.random()
                    col = (r, g, b)
                    plt.bar(result.keys(), result.values(), color=(col))
                    plt.xlabel('Cферы')
                    plt.ylabel('Расходы')
                    plt.title("Сумма расходов по сферам за заданный период")
                    plt.show()

def get_timestamp(y, m, d):
    return datetime.datetime.timestamp(datetime.datetime(y, m, d)) # хранение типа данных date, (тип отсутвует в бд)

def get_date(tmstmp):
    return datetime.datetime.fromtimestamp(tmstmp).date() # вывод типа данных дата

def get_timestamp_sting(s):
    t = s.split('.')
    return get_timestamp(int(t[2]), int(t[1]), int(t[0]))

def get_statistic_data(d, a):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    querty = """SELECT * from payments JOIN expenses ON expenses.id = payments.expense_id WHERE payments.users_id = (?) AND (?)<= payment_date AND payment_date <= (?)"""
    q = obrabotka()
    k = (q, d, a)
    cur.execute(querty, k)
    value = cur.fetchall()
    if value == []:
        return False
    else:
        all_data = []
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            q = obrabotka()
            querty = """SELECT * from payments JOIN expenses ON expenses.id = payments.expense_id WHERE payments.users_id = (?) AND (?)<= payment_date AND payment_date <= (?)"""
            cursor.execute(querty, (q, d, a))
            all_data = cursor
        return all_data

def get_statistic_data1():
    all_data1 = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        q = obrabotka()
        k = (q,)
        querty = """SELECT id, amount, payment_date, expense_id from payments where users_id = (?)"""
        cursor.execute(querty, k)
        all_data1 = cursor
    return all_data1

def get_statistic_data2(): # получение массива данных по СФЕРАМ
    all_data2 = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        q = obrabotka()
        k = (q,)
        querry = """SELECT id, name from expenses where id_users == (?)"""
        cursor.execute(querry, k)
        all_data2 = cursor
    return all_data2

def date_proverka(d, a): #проверка наличия данных в диапазоне выбранных дат и получение массива данных по ПЛАТЕЖАМ
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        paymetsCursor = db.cursor()
        k = str(obrabotka())
        querty = """SELECT * from payments WHERE payments.users_id = (?) AND (?) <= payment_date AND payment_date <= (?)"""
        paymetsCursor.execute(querty, (k, d, a))
        all_data = paymetsCursor
    return all_data

def srednii(d, a): #средняя сумма расходов
    count = 0
    cat = 0
    flag = "данные отсутствуют"
    all_data = date_proverka(d, a)
    for payments in all_data:
        cat += 1
        count += int(payments['amount'])
    if count == 0.0:
        return flag
    else:
        count = count / cat
        return count
ccc = 0
def get_most_expens_item(d, a): #самая затратная сфера
    if get_statistic_data(d, a) == False:
        return "данные отсутствуют"
    else:
        data = get_statistic_data(d, a)
        qwerty = max(list(data), key=lambda x:x['amount'])['name']
        if qwerty == "":
            return "данные отсутствуют"
        p = 0
        count = 0
        data1 = get_statistic_data2()
        for expenses in data1:
            if expenses['name'] == qwerty:
                p = expenses['id']
        data = get_statistic_data(d, a)
        for payments in data:
            if payments['expense_id'] == p:
                count += payments["amount"]
        global ccc
        ccc = count
        if count == 0 or qwerty == "":
            return "данные отсутствуют"
        elif qwerty[1] == "u":
            a = codecs.decode(qwerty, 'unicode-escape')
            return a
        else:
            return qwerty

def alina(): #сумма расходов по этой сфере
    '''data = get_statistic_data2()
    if get_most_expens_item(d, a) == "данные отсутствуют":
        return "данные отсутствуют"
    else:
        allina = get_most_expens_item(d, a)
        k = allina.encode('unicode-escape').decode('utf-8')
        p = 0
        count = 0
        data1 = get_statistic_data1()
        for expenses in data:
            if expenses['name'] == k:
                p = expenses['id']
        for payments in data1:
            if payments['expense_id'] == p:
                count += payments["amount"]'''
    return ccc

qw = 0
def get_most_expens_day(d, a): # самый затратный день
    global qw
    if get_most_expens_item(d, a) == "данные отсутствуют":
        return "данные отсутствуют"
    else:
        data = get_statistic_data(d, a)
        week_days = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
        days = {}
        for payments in data:
            if get_date(payments['payment_date']).weekday() in days:
                days[get_date(payments['payment_date']).weekday()] += payments['amount']
            else:
                if int(payments['amount']) == 0:
                    return "данные отсутствуют"
                else:
                    days[get_date(payments['payment_date']).weekday()] = payments['amount']
        qw = payments['payment_date']
        return week_days[max(days, key=days.get)]

def get_most_expens_day_summ(d, a): #сумма по самому дорогому дню
    if get_most_expens_item(d, a) == "данные отсутствуют":
        return "данные отсутствуют"
    else:
        get_most_expens_day(d, a)
        global qw
        date1 = get_statistic_data1()
        count = 0
        if get_most_expens_day(d, a) == "данные отсутствуют":
            return "данные отсутствуют"
        else:
            for payments in date1:
                if payments['payment_date'] == qw:
                    count += payments['amount']
            return count

def month():
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        q = obrabotka()
        querty = """SELECT * from payments JOIN expenses ON expenses.id = payments.expense_id WHERE payments.users_id = (?)"""
        cursor.execute(querty, (q,))
        all_data = cursor
    return all_data

def get_most_exp_month(): # самый затратный месяц ЗА ВЕСЬ период
    data = month()
    month_list = ('0', "Январь", "Ферваль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    days = {}
    for payments in data:
        if payments["amount"] == 0.0:
            return "внесите платеж"
        else:
            if get_date(payments['payment_date']).month in days:
                days[get_date(payments['payment_date']).month] += payments['amount']
            else:
                days[get_date(payments['payment_date']).month] = payments['amount']
    if days == {}:
        return "внесите платеж"
    else:
        return month_list[max(days, key=days.get)]

def form_plus():
    all_data = {'ac':{}, 'names':[]}
    result = {}
    querty = get_statistic_data2()
    result = dict(querty)
    all_data['ac'] = {result[k]: k for k in result}
    all_data['names'] = [v for v in result.values()]
    for i in range(len(all_data['names'])):
        a = all_data['names'][i]
        if a[1] == "u" and a[0] == "/":
            all_data['names'][i] = codecs.decode(a, 'unicode-escape')
    return all_data

def form_del():
    data = get_statistic_data1()
    a = 0
    for payments in data:
        if payments['id']:
            a += 1
    if a > 1:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            q = obrabotka()
            k = (q,)
            querty = """DELETE FROM payments WHERE id = (SELECT max(id) From payments) AND users_id = (?)"""
            cursor.execute(querty, k)
            flag = True
            db.commit()
    else:
        flag =False
    return flag

def insert_payments(insert_payments):
    success = False
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    q = obrabotka()
    k = (q,)
    querty = """SELECT amount FROM payments WHERE users_id = (?)"""
    cur.execute(querty, k)
    value = cur.fetchall()
    if value == []:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            querty = """DELETE FROM payments WHERE users_id == (?) AND amount == 0.0;"""
            cursor.execute(querty, k)
            db.commit()
    with sqlite3.connect('database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """ INSERT INTO payments(amount, payment_date, expense_id, users_id) VALUES (?, ?, ?, ?)"""
        cursor.execute(querty, insert_payments)
        success = True
    db.commit()
    return success

def form_del_sfere(amount): #удаление сферы расходов
    flag = False
    a = 0
    count = 0
    data = get_statistic_data2()
    #amount = amount.encode('unicode-escape').decode('utf-8')
    for expenses in data:
        if expenses['name'] == amount:
            a = expenses['id']
        else:
            count += 1
    if count > 0:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            querty = """DELETE FROM "expenses" WHERE id=%a""" %a
            cursor.execute(querty)
            querty = """DELETE FROM "payments" WHERE expense_id = %a""" %a
            cursor.execute(querty)
            flag = True
            db.commit()
    return flag

def new_sfere(a):
    flag = False
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        q = obrabotka()
        k = (q, a)
        querty = """SELECT id, name FROM expenses WHERE id_users = (?) AND name =(?) """
        cursor.execute(querty, k)
        value = cursor.fetchall()
        if value != []:
            flag = False
        else:
            querty = """INSERT INTO expenses (name, id_users) VALUES (?,?)"""
            cursor.execute(querty, (a, q))
            flag = True
    db.commit()
    return flag

def krug(flag):
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        q = obrabotka()
        k = (q,)
        asa = 0
        querty = """SELECT expense_id, SUM(amount) as amount from payments WHERE users_id = (?) GROUP BY expense_id"""
        cursor.execute(querty, k)
        all_data = cursor
    amount = {}
    for payments in all_data:
        if payments['amount'] != 0:
            amount[payments["expense_id"]] = payments['amount']
            asa = payments['amount']
    if asa == 0.0:
        return "НЕТ ДАННЫХ"
    else:
        #print(list(amount.values()))
        #print(amount.keys())
        if list(amount.values()) == [0.0]:
            return "НЕТ ДАННЫХ"
        else:
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cursor = db.cursor()
            q = obrabotka()
            rrr = (q,)
            querry = """SELECT id, name from expenses where id_users == (?)"""
            cursor.execute(querry, rrr)
            cur.execute(querry, rrr)
            lll = cur.fetchall()
            if lll == []:
                return "НЕТ ДАННЫХ"
            else:
                result = {}
                for item in cursor:#id сферы и названия
                    if item["id"] in amount.keys(): #id сферы
                        k = item["name"]
                        #p = codecs.decode(k, 'unicode-escape')
                        result[k] = amount[item["id"]]
                    '''else:
                        result[item["name"]] = 0'''
                if flag == 0:
                    #print(result.keys())
                    #print(result.values())
                    fig1, ax1 = plt.subplots()  # вывод круговой диаграммы
                    wedges, texts, autotexts = ax1.pie(result.values(), labels=result.keys(), autopct='%1.2f%%')  # вывод значений в процентах
                    ax1.pie(result.values(), labels=result.keys())  # значения для диаграммы
                    ax1.legend(result.keys(), loc='upper left', bbox_to_anchor=(1.0, 1.1))  # легенда - какие данные и их расположение
                    plt.title("Расходы за весь период")
                    plt.show()