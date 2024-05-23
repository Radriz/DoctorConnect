import sqlite3

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


def registration(fio, username, email, password, speciality, repeat_password):
    if password.lower() == repeat_password.lower():
        cursor.execute(
            f"insert into User(fio,username,email, password,speciality) Values('{fio}','{username}','{email}','{password}','{speciality}')")
        connection.commit()
        print('Пользователь зарегистрирован!')
        return True
    elif password.lower() != repeat_password.lower():
        print('Повторить пароль')
        return False


def autorization(email, password):
    check = cursor.execute(
        f"select * from user where email='{email}' and password= '{password}'").fetchall()  # [(id, fio...),]
    if check:
        print("Успешно авторизирован")
        return check
    else:
        print("Неверный логин или пароль")
        return False


class Technik:
    def __init__(self, id, name):
        self.id = id
        self.name = name


def find_techniks():
    techniks = cursor.execute(
        f"select * from user where speciality = 'technik'").fetchall()
    technik_objects = []
    for technik in techniks:
        t = Technik(technik[0], technik[1])
        technik_objects.append(t)
    return technik_objects


def create_order(patient, formula, type, comment, fitting, deadline, technik, doctor, color_letter,color_number):
    cursor.execute(
        f"""insert into "order"(patient, formula, type, comment, fitting, deadline, to_user, from_user,color_letter,color_number) 
        Values('{patient}','{formula}','{type}','{comment}','{fitting}','{deadline}',{technik},{doctor},'{color_letter}','{color_number}')""")
    connection.commit()


def get_user(id):
    user = cursor.execute(
        f"select * from user where id = {id}"
    ).fetchone()
    return user


def get_orders_technik(id):
    order = cursor.execute(
        f"""select * from "order" where to_user = {id}""").fetchall()
    return order


def get_orders_doctor(id):
    order = cursor.execute(
        f"""select * from "order" where from_user = {id}""").fetchall()
    order.reverse()
    return order


def get_order_by_id(id):
    order = cursor.execute(
        f"""select * from "order" where id = {id}"""
    ).fetchone()
    return order


def get_order_technik_done(id, is_done, fitting_done):
    if is_done == 0:
        order = cursor.execute(
            f"""select * from "order" where to_user = {id} and is_done = {is_done} and fitting_done = {fitting_done}""").fetchall()
    else:
        order = cursor.execute(
            f"""select * from "order" where to_user = {id} and is_done = {is_done}""").fetchall()
    return order


def get_order_doctor_done(id, is_done, fitting_done):
    if is_done == 0:
        order = cursor.execute(
            f"""select * from "order" where from_user = {id} and is_done = {is_done} and fitting_done = {fitting_done}""").fetchall()
    else:
        order = cursor.execute(
            f"""select * from "order" where from_user = {id} and is_done = {is_done}""").fetchall()
    return order

def update_order_done(order_id, is_done= None, fitting_done = None):
    if fitting_done is not None:
        cursor.execute(
            f"""update "order" set fitting_done = {fitting_done} where id = {order_id}""")
    elif is_done is not None:
        cursor.execute(
            f"""update "order" set is_done = {is_done} where id = {order_id}""")
    connection.commit()

def delete_order_by_id(id):
    cursor.execute(
        f"""delete from "order" where id = {id}""")
    connection.commit()

def update_order_by_id(patient, formula, type, comment, fitting, deadline, technik, doctor, color_letter,color_number,order_id):
    cursor.execute(
        f"""update "order" set patient = '{patient}',
        formula = '{formula}',
        type = '{type}',
        comment = '{comment}',
        fitting = '{fitting}',
        deadline = '{deadline}',
        to_user = '{technik}',
        from_user = '{doctor}',
        color_letter = '{color_letter}',
        color_number = '{color_number}'
        where id = {order_id}""")
    connection.commit()


