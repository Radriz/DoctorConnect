import sqlite3
import hashlib

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


def hash_password(password):
    h = hashlib.md5(password.encode())
    p = h.hexdigest()
    return p


def registration(fio, email, password, speciality, repeat_password):
    if password.lower() == repeat_password.lower():
        password = hash_password(password)
        cursor.execute(
            f"insert into User(fio,email, password,speciality) Values('{fio}','{email}','{password}','{speciality}')")
        connection.commit()
        print('Пользователь зарегистрирован!')
        return True
    elif password.lower() != repeat_password.lower():
        print('Повторить пароль')
        return False


def autorization(email, password):
    h2 = hashlib.md5(password.encode())
    checks = cursor.execute(
        f"select * from user where email='{email}'").fetchall()  # [(id, fio...),]
    for check in checks:
        if check[4] == h2.hexdigest():
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


def create_order(patient, formula, type, comment, fitting, deadline, technik, doctor, color_letter, color_number):
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


def update_order_done(order_id, is_done=None, fitting_done=None):
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


def update_order_by_id(patient, formula, type, comment, fitting, deadline, technik, doctor, color_letter, color_number,
                       order_id):
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


def procedure_type():
    type = cursor.execute(
        f"select type from procedure").fetchall()  # [("",), ("",), ]
    type = list(set(type))
    updt_types = [t[0] for t in type]
    return updt_types


def name_procedure(type, subtype):
    x = f"""select * from procedure where type = '{type}' and subtype= '{subtype}'"""
    name = cursor.execute(x).fetchall()
    return name


def get_subtype_by_type(type):
    subtype = cursor.execute(
        f"""select subtype from procedure where type = '{type}'"""
    ).fetchall()
    subtype_list = list(set([sub[0] for sub in subtype]))
    return subtype_list


def get_template_procedure(type, user_id):
    templates = cursor.execute(
        f"""select template.id,template.name, procedure.id,
        procedure.name,procedure.subtype,procedure.price,user_procedure.id,user_procedure.name,
        user_procedure.price,template_procedure.amount,template.stick from template
        left join template_procedure on template_procedure.template_id = template.id 
        left join procedure on template_procedure.procedure_id = procedure.id
        left join user_procedure on template_procedure.user_procedure_id = user_procedure.id
        where (procedure.type = '{type}' or user_procedure.type = '{type}')
        and (template.user_id = {user_id} or template.user_id is null) order by template_procedure.id"""
    ).fetchall()
    return templates


def create_template_procedure(template_name, user_id):
    id = cursor.execute(
        f"""insert into template(name,user_id) 
            Values('{template_name}',{user_id}) returning id""").fetchone()
    connection.commit()
    return id[0]


def delete_template_procedure_by_id(id, user_id):
    cursor.execute(
        f"""delete from template where id = {id} and user_id={user_id}""")
    connection.commit()


def add_procedure_to_template(name, type, price, template_id, amount):
    user_procedure_id = cursor.execute(
        f"""insert into user_procedure(name,type,price) 
              Values('{name}','{type}',{price}) returning id""").fetchone()
    connection.commit()
    print(template_id, user_procedure_id, amount)
    cursor.execute(
        f"""insert into template_procedure(template_id, user_procedure_id, amount) 
                  Values({template_id},{user_procedure_id[0]},{amount})""")
    connection.commit()


def edit_user_procedure(id, name, type, price):
    cursor.execute(
        f"""update user_procedure set name = '{name}',
            type = '{type}',
            price = '{price}'
            where id = {id}""")
    connection.commit()


def update_sticker_name(template_id, sticker, user_id):
    cursor.execute(
        f"""update template set stick = '{sticker}'
                where id = {template_id} and user_id = {user_id}""")
    connection.commit()


def delete_user_procedure(id):
    cursor.execute(
        f"""delete from user_procedure where id = {id}""")
    connection.commit()


def update_amount_procedure_template(procedure_id, template_id, amount):
    cursor.execute(
        f"""update template_procedure set amount = {amount}
                where user_procedure_id = {procedure_id} and 
                template_id = {template_id} """)
    connection.commit()


def update_template_name(template_id, template_name, user_id):
    cursor.execute(
        f"""update template set name = '{template_name}'
                    where id = {template_id} and user_id = {user_id}
                    """)
    connection.commit()


def create_client(fio, birthday):
    cursor.execute(
        f"""insert into client(fio, birth_day) 
            Values('{fio}', '{birthday}') returning id""").fetchone()
    connection.commit()
    return cursor.lastrowid


def get_client_by_fio(fio,birthday):
    client = cursor.execute(
        f"""select id from client where fio = '{fio}' and birth_day = '{birthday}'""").fetchone()
    return client


def create_plan_db(fio, date_time, user_id,birthday):
    client = get_client_by_fio(fio,birthday)
    if not client:
        client_id = create_client(fio, birthday)
    else:
        client_id=client[0]
    cursor.execute(
        f"""insert into treatment_plan(client_id, date_time, user_id) 
            Values({client_id}, '{date_time.strftime('%d.%m.%Y %H:%M:%S')}',{user_id}) returning id""").fetchone()
    connection.commit()
    return cursor.lastrowid


def create_service_db(stage, template_id, tooth, plan_id, amount):
    cursor.execute(
        f"""insert into plan_template(stage, plan_id, tooth, template_id, quantity) 
            Values('{stage}',{plan_id}, '{tooth}', {template_id}, {amount}) returning id""").fetchone()
    connection.commit()
    return cursor.lastrowid

def get_all_patient():
    patient = cursor.execute(
        f"""SELECT * FROM client""").fetchall()
    return patient

def get_patient_data_plan_by_id(id,user_id):
    patient = cursor.execute(
        f"""SELECT client.fio , client.birth_day from client
        join treatment_plan on client.id = treatment_plan.client_id
        where treatment_plan.id = {id} and user_id={user_id}""").fetchone()
    return patient

def get_stages_plan_id(id):
    stages = cursor.execute(
        f"""SELECT stage, quantity, tooth, template.name FROM plan_template
        join treatment_plan on plan_template.plan_id = treatment_plan.id
        join template on plan_template.template_id = template.id
        where treatment_plan.id = {id}""").fetchall()
    return stages