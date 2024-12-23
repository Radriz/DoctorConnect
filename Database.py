import sqlite3
import hashlib

connection = sqlite3.connect("Database.db")
cursor = connection.cursor()


def hash_password(password):
    h = hashlib.md5(password.encode())
    p = h.hexdigest()
    return p


def registration(fio, email, password, speciality, repeat_password, clinic):
    if not clinic:
        clinic = None
    if password.lower() == repeat_password.lower():
        password = hash_password(password)
        try:
            cursor.execute(
                f"insert into User(fio,email, password,speciality,clinic) Values('{fio}','{email}','{password}','{speciality}','{clinic}')")
            connection.commit()
        except:
            return False, 'Пользователь с таким e-mail существует'
        return True, 'Пользователь зарегистрирован!'
    elif password.lower() != repeat_password.lower():
        return False, 'Пароли не совпадают попробуйте еще раз'


def autorization(email, password):
    h2 = hashlib.md5(password.encode())
    checks = cursor.execute(
        f"select * from user where LOWER(email)='{email.lower()}'").fetchall()  # [(id, fio...),]
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


def create_order(patient, formula, type, comment, fitting, deadline, technik, doctor, color_letter, color_number,price):
    id = cursor.execute(
        f"""insert into "order"(patient, formula, type, comment, fitting, deadline, to_user, from_user,color_letter,color_number,price) 
        Values('{patient}','{formula}','{type}','{comment}','{fitting}','{deadline}',{technik},{doctor},'{color_letter}','{color_number}','{price}') returning id""").fetchone()
    connection.commit()
    return id[0]

def set_new_order_price(order_id, price):
    cursor.execute(
        f"""update "order" set price = {price} where id = {order_id}""")
    connection.commit()
def set_new_order_technik_comment(order_id, comment):
    cursor.execute(
        f"""update "order" set technik_comment = '{comment}' where id = {order_id}""")
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
        user_procedure.price,template_procedure.amount,template.stick,template_procedure.is_active,template.tooth_depend from template
        left join template_procedure on template_procedure.template_id = template.id 
        left join procedure on template_procedure.procedure_id = procedure.id
        left join user_procedure on template_procedure.user_procedure_id = user_procedure.id
        where (procedure.type = '{type}' or user_procedure.type = '{type}')
        and (template.user_id = {user_id} or template.user_id is null) order by template_procedure.id"""
    ).fetchall()
    return templates


def create_template_procedure(template_name,tooth_depend,user_id):
    id = cursor.execute(
        f"""insert into template(name,user_id,tooth_depend) 
            Values('{template_name}',{user_id},{1 if tooth_depend else 0}) returning id""").fetchone()
    connection.commit()
    return id[0]


def delete_template_procedure_by_id(id, user_id):
    cursor.execute(
        f"""delete from template where id = {id} and user_id={user_id}""")
    connection.commit()


def add_procedure_to_template(name, type, price, template_id, amount,is_active):
    user_procedure_id = cursor.execute(
        f"""insert into user_procedure(name,type,price) 
              Values('{name}','{type}',{price}) returning id""").fetchone()
    connection.commit()
    print(template_id, user_procedure_id, amount)
    cursor.execute(
        f"""insert into template_procedure(template_id, user_procedure_id, amount,is_active) 
                  Values({template_id},{user_procedure_id[0]},{amount},{1 if is_active else 0} )""")
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


def update_amount_procedure_template(procedure_id, template_id, amount,is_active):
    cursor.execute(
        f"""update template_procedure set amount = {amount}, is_active = {1 if is_active else 0}
                where user_procedure_id = {procedure_id} and 
                template_id = {template_id} """)
    connection.commit()


def update_template_name(template_id, template_name, user_id, tooth_depend):
    cursor.execute(
        f"""update template set name = '{template_name}', tooth_depend = {1 if tooth_depend else 0}
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


def create_service_db(stage, template_id, tooth, plan_id):
    cursor.execute(
        f"""insert into plan_template(stage, plan_id, tooth, template_id) 
            Values('{stage}',{plan_id}, '{tooth}', {template_id}) returning id""").fetchone()
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
        f"""SELECT stage, tooth, template.id, template.name, template.stick, 
        user_procedure.name, user_procedure.price, template_procedure.amount,template.tooth_depend, template_procedure.is_active
        FROM plan_template
        join treatment_plan on plan_template.plan_id = treatment_plan.id
        join template on plan_template.template_id = template.id
        join template_procedure on template.id = template_procedure.template_id
        join user_procedure on template_procedure.user_procedure_id = user_procedure.id
        where treatment_plan.id = {id} order by plan_template.id""").fetchall()
    return stages

def add_photo_to_order(order, photo):
    cursor.execute(
        f"""INSERT INTO Order_photos(order_id, photo) VALUES({order}, '{photo}')"""
    )
    connection.commit()

def add_file_to_technik_files(order, file):
    cursor.execute(
        f"""INSERT INTO technik_files(order_id, file) VALUES({order}, '{file}')"""
    )
    connection.commit()
def get_photos_by_order_id(order_id):
    get_photo = cursor.execute(
        f""" SELECT * FROM Order_photos WHERE order_id = {order_id}"""
    ).fetchall()
    return get_photo

def get_technik_files_by_order_id(order_id):
    get_file = cursor.execute(
        f""" SELECT * FROM technik_files WHERE order_id = {order_id}"""
    ).fetchall()
    return get_file

def delete_photo_from_order(photo_name):
    cursor.execute(
        f""" DELETE FROM Order_photos WHERE photo = '{photo_name}'"""
    )
    connection.commit()
def delete_file_from_technik_files(file_name):
    cursor.execute(
        f""" DELETE FROM technik_files WHERE file = '{file_name}'"""
    )
    connection.commit()

def add_technik_service(technik_id,name,price):
    cursor.execute(
        f"""INSERT INTO technik_services(technik_id, name, price) VALUES({technik_id}, '{name}', {price})"""
    )
    connection.commit()

def update_technik_service(id,name,price):
    cursor.execute(
        f"""UPDATE technik_services SET name = '{name}', price = {price} WHERE id = {id}"""
    )
    connection.commit()

def delete_technik_service(id):
    cursor.execute(
        f"""DELETE FROM technik_services WHERE id = {id}"""
    )
    connection.commit()

def get_all_technik_services(technik_id):
    get_services = cursor.execute(
        f""" SELECT * FROM technik_services WHERE technik_id = {technik_id}"""
    ).fetchall()
    return get_services

def get_all_technik_invoices(technik_id):
    get_invoices = cursor.execute(
        f""" SELECT Invoice.id,Invoice.creation_date,user.fio,technik_id,paid,total_price FROM Invoice inner join user on Invoice.doctor_id = user.id WHERE technik_id = {technik_id}"""
    ).fetchall()
    return get_invoices

def delete_technik_invoice(id):
    cursor.execute(
        f""" DELETE FROM Invoice WHERE id = {id}"""
    )
    connection.commit()

def get_not_paid_not_invoice_orders_technik(id):
    order = cursor.execute(
        f"""select * from "order" where to_user = {id} and paid = 0 and invoice is NULL""").fetchall()
    return order