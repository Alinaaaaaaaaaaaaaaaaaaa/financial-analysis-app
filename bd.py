import datetime
import sqlite3
import matplotlib.pyplot as plt
import random as random

def grafic_return():
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        paymetsCursor = db.cursor()
        querty = """SELECT expense_id, SUM(amount) as amount from payments GROUP BY expense_id"""
        paymetsCursor.execute(querty)
        all_data = paymetsCursor
        if paymetsCursor.rowcount == 0:
            return "НЕТ ДАННЫХ"
        amount = {}
        for i in all_data:
            amount[i["expense_id"]] = i["amount"]
        cursor = db.cursor()
        querry = """SELECT id, name from expenses"""
        cursor.execute(querry)
        result = {}
        for item in cursor:
            if item["id"] in amount.keys():
                result[item["name"]] = amount[item["id"]]
            else:
                result[item["name"]] = 0
    r = random.random()
    g = random.random()
    b = random.random()
    col = (r, g, b)
    plt.bar(result.keys(), result.values(), color=(col))
    plt.xlabel('Cферы')
    plt.ylabel('Расходы')
    plt.show()

def get_timestamp(y, m, d):
    return datetime.datetime.timestamp(datetime.datetime(y, m, d)) # хранение типа данных date, (тип отсутвует в бд)

def get_date(tmstmp):
    return datetime.datetime.fromtimestamp(tmstmp).date() # вывод типа данных дата

def get_timestamp_sting(s):
    t = s.split('-')
    return get_timestamp(int(t[2]), int(t[1]), int(t[0]))

def get_statistic_data():
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """SELECT * from payments JOIN expenses ON expenses.id = payments.expense_id"""
        cursor.execute(querty)
        all_data = cursor
    return all_data

def get_statistic_data1():
    all_data1 = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """SELECT * from payments"""
        cursor.execute(querty)
        all_data1 = cursor
    return all_data1

def get_statistic_data2():
    all_data2 = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """SELECT * from expenses"""
        cursor.execute(querty)
        all_data2 = cursor
    return all_data2

def date_proverka(d, a):
    flag = False
    all_data = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        params = (d, a)
        querty = """SELECT * from payments WHERE payment_date BETWEEN %d AND %a""" %params
        cursor.execute(querty)
        all_data = cursor
        flag = True
    return all_data

def srednii(d, a):
    count = 0
    cat = 0
    all_data = date_proverka(d, a)
    for payments in all_data:
        if payments['amount']:
            cat += 1
            count += payments["amount"]
    if cat != 0:
        count = count // cat
    return count

def get_most_expens_item(): #самая затратная сфера
    data = get_statistic_data()
    return max(list(data), key=lambda x:x['amount'])['name']

def alina(): #сумма расходов по этой сфере
    data = get_statistic_data2()
    allina = get_most_expens_item()
    p = 2
    count = 0
    data1 = get_statistic_data1()
    for expenses in data:
        if expenses['name'] == allina:
            p = expenses['id']
    for payments in data1:
        if payments['expense_id'] == p:
            count += payments["amount"]
    return count

def get_most_common_item():
    data = get_statistic_data()
    quantily = {}
    for payments in data:
        if payments['expense_id'] in quantily:
            quantily[payments['expense_id']]['qty'] += 1
        else:
            quantily[payments['expense_id']] = {'qty': 1, "name": payments['name']}
    return max(quantily.values(), key=lambda x: ['qty'])['name']


qw = 0
def get_most_expens_day():
    global qw
    data = get_statistic_data()
    week_days = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
    days = {}
    for payments in data:
        if get_date(payments['payment_date']).weekday() in days:
            days[get_date(payments['payment_date']).weekday()] += payments['amount']
        else:
            days[get_date(payments['payment_date']).weekday()] = payments['amount']
    qw = payments['payment_date']
    return week_days[max(days, key=days.get)]

def get_most_expens_day_summ():
    get_most_expens_day()
    global qw
    date1 = get_statistic_data1()
    count = 0
    for payments in date1:
        if payments['payment_date'] == qw:
            count += payments['amount']
    return count

def get_most_exp_month():
    data = get_statistic_data()
    month_list = ('0', "Январь", "Ферваль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    days = {}
    for payments in data:
        if get_date(payments['payment_date']).month in days:
            days[get_date(payments['payment_date']).month] += payments['amount']
        else:
            days[get_date(payments['payment_date']).month] = payments['amount']
        return month_list[max(days, key=days.get)]

def form_plus():
    all_data = {'ac':{}, 'names':[]}
    result = {}
    querty = get_statistic_data2()
    result = dict(querty)
    all_data['ac'] = {result[k]: k for k in result}
    all_data['names'] = [v for v in result.values()]
    return all_data

def insert_payments(insert_payments):
    success = False
    with sqlite3.connect('database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """ INSERT INTO payments(amount, payment_date, expense_id) VALUES (?, ?, ?)"""
        cursor.execute(querty, insert_payments)
        db.commit()
        success = True
    return success

def form_del_sfere(amount):
    flag = False
    a = 0
    count = 0
    data = get_statistic_data2()
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
            flag = True
    return flag

def form_del():
    flag = False
    data = get_statistic_data1()
    a = 0
    for payments in data:
        if payments['id']:
            a += 1
    if a > 1:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""DELETE FROM payments WHERE id = (SELECT max(id) From payments)""")
            flag = True
    else:
        flag =False
    return flag

def new_sfere(a):
    flag = False
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """INSERT INTO expenses (name) VALUES (%a)""" %a
        cursor.execute(querty)
        flag = True
    return flag


