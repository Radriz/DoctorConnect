import datetime
import os
import subprocess
import time
import uuid
from typing import Optional, List

import fitz
from docx2pdf import convert
import pypandoc
from fastapi import FastAPI, Form, Depends, HTTPException, Request, UploadFile, File, Body, Query
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from itsdangerous import URLSafeSerializer, BadSignature

from Database import autorization, registration, find_techniks, get_user, create_order, get_orders_doctor, \
    get_orders_technik, get_order_by_id, update_order_done, delete_order_by_id, update_order_by_id, procedure_type, \
    name_procedure, get_subtype_by_type, get_template_procedure, create_template_procedure, \
    delete_template_procedure_by_id, add_procedure_to_template, edit_user_procedure, delete_user_procedure, \
    update_amount_procedure_template, update_template_name, update_sticker_name, create_plan_db, create_service_db, \
    get_all_patient, get_patient_data_plan_by_id, get_stages_plan_id, add_photo_to_order, get_photos_by_order_id, \
    delete_photo_from_order, add_technik_service, update_technik_service, delete_technik_service, \
    get_all_technik_services, set_new_order_price, delete_file_from_technik_files, add_file_to_technik_files, \
    get_technik_files_by_order_id, set_new_order_technik_comment, get_all_technik_invoices, delete_technik_invoice, \
    get_not_paid_not_invoice_orders_technik, add_invoice, add_invoice_order, get_technik_invoice_orders, \
    delete_invoice_order, get_invoice_by_id, get_all_doctor_invoices, pay_doctor_invoice, pay_invoice_order, \
    update_tg_to_user
from add_image import image_to_pdf
from crypto_cipher import URLSafeEncryptor
from document_generate import generate_plan
from email_conformation import send_email_conformation
from parameters import first_row, second_row, types, color_letter, color_number, tooth_priority
from dotenv import dotenv_values
config = dotenv_values() # {'LOGIN' : 123}
encryptor = URLSafeEncryptor(password=config['CRYPTO_TELEGRAM_BOT'])
app = FastAPI()


app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/images", StaticFiles(directory="templates/images"), name="images")
app.mount("/plans", StaticFiles(directory="treatment_plans"), name="treatment_plan")
app.mount("/order/photo/show", StaticFiles(directory="orders_photo"), name="orders_photo")
app.mount("/order/technik/file/show", StaticFiles(directory="technik_files"), name="technik_files")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account")

SECRET_KEY = config["SECRET_KEY"]
serializer = URLSafeSerializer(SECRET_KEY)

# Зарегистрируем кастомный фильтр для Jinja2
def filter_tooth(tooth_string, quarter):
    teeth = [num.strip() for num in tooth_string.split(',')]
    multiplier = {
        1: -1,
        2: 1,
        3: -1,
        4: 1,
    }
    quarters = {
        1: range(11, 19),  # Верхняя правая
        2: range(21, 29),  # Верхняя левая
        3: range(41, 49),  # Нижняя левая
        4: range(31, 39)   # Нижняя правая
    }
    quarter_teeth = [tooth if tooth[0] != "0" else "0" for tooth in sorted(teeth, key=lambda x: multiplier[quarter]*int(x)) if int(tooth) in quarters[quarter]]
    return ' '.join(quarter_teeth)

# Добавим кастомный фильтр в Jinja2
templates.env.filters["filter_tooth"] = filter_tooth


class CreateInvoice(BaseModel):
    doctor_id: int
    orders: List[int]

class UserAuthorization(BaseModel):
    email: str
    password: str


class Order(BaseModel):
    patient: str
    formula: str
    type: str
    price: str
    comment: str
    fitting: str
    deadline: str
    technik: str
    color_letter: str
    color_number: str



class TemplateProcedure(BaseModel):
    template_name: str
    tooth_depend: bool

class TemplateSticker(BaseModel):
    template_id: int
    sticker: str


class Procedure(BaseModel):
    name: str
    type: str
    price: int
    template_id: int
    amount: int
    is_active: bool

class User_tg(BaseModel):
    cipher_id: str
    tg_id: int



def create_session(user_id):
    return serializer.dumps({"user_id": user_id})


def read_session(session_cookie: str):
    try:
        data = serializer.loads(session_cookie)
        return data.get("user_id")
    except BadSignature:
        return None

@app.post("/send/email/code")
async def send_email(request: Request, email: str = Query(...)):
    code = send_email_conformation(email)
    return {"code": code}


@app.get("/authorization", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("authorization.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def initial(request: Request):
    return RedirectResponse(url="/account")


@app.get("/registration", response_class=HTMLResponse)
async def regist(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.route("/account", methods=['GET', 'POST'])
async def account(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is not None:
        user = get_user(user_id)
        if user[5] == "doctor":
            selected_techniks = []
            orders = get_orders_doctor(user[0])
            for i in range(len(orders)):
                orders[i] = list(orders[i])
                if orders[i][5]:
                    data = orders[i][5].split("-")
                    orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                technik = get_user(orders[i][7])
                orders[i][7] = {"id" : technik[0], "name" : technik[1]}
                if {"id" : technik[0], "name" : technik[1]} not in selected_techniks:
                    selected_techniks.append({"id": technik[0], "name":technik[1]})

        else:
            selected_doctors = []
            orders = get_orders_technik(user[0])
            for i in range(len(orders)):
                orders[i] = list(orders[i])
                if orders[i][5]:
                    data = orders[i][5].split("-")
                    orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                doctor = get_user(orders[i][6])

                if doctor[6] is not None:
                    doctor_name = f"{doctor[1]} ({doctor[6]})"
                else:
                    doctor_name = f"{doctor[1]}"
                orders[i][6] = {"id": doctor[0], "name": doctor_name}
                if {"id" : doctor[0], "name" : doctor_name} not in selected_doctors:
                    selected_doctors.append({"id": doctor[0], "name": doctor_name})

        done = [order for order in orders if order[9] == 1]
        fitting_done = [order for order in orders if order[9] == 0 and order[12] == 1]
        not_done = [order for order in orders if order[9] == 0 and order[12] == 0]

        if user[5] == "doctor":
            return templates.TemplateResponse("doctor_personal_account.html",
                  {
                      "request": request,
                      'fio': user[1],
                      "done": done,
                      "fitting_done": fitting_done,
                      "not_done": not_done,
                      "techniks": selected_techniks,
                      "cipher_id": encryptor.encrypt(str(user[0]))
                  })
        else:
            return templates.TemplateResponse(
                "technik_personal_account.html",
                {
                    "request": request,
                    'fio': user[1],
                    "done": done,
                    "fitting_done": fitting_done,
                    "not_done": not_done,
                    "doctors": selected_doctors,
                    "cipher_id": encryptor.encrypt(str(user[0]))

                })

    return RedirectResponse(url="/authorization")


@app.post("/account/enter", response_class=HTMLResponse)
async def check_login_password(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password
    res = autorization(email, password)
    if res:
        session = create_session(res[0])
        response = RedirectResponse(url="/account")
        response.set_cookie(key="session", value=session)
        return response
    return templates.TemplateResponse("authorization.html", {"request": request, "wrong_password": True})


@app.post("/registration", response_class=HTMLResponse)
async def regist(request: Request, fio: str = Form(...),
                 email: str = Form(...), password: str = Form(...), speciality: str = Form(...),
                 repeat_password: str = Form(...), clinic: Optional[str] = Form(None),):
    res, comment = registration(fio, email, password, speciality, repeat_password,clinic)
    if not res:
        return templates.TemplateResponse("registration.html", {"request": request,"comment": comment})
    else:
        return templates.TemplateResponse("authorization.html", {"request": request})
@app.get("/forgot", response_class=HTMLResponse)
async def forgot(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/user/tg")
async def add_tg_to_user(request: Request, user_tg: User_tg):
    cipher_id = user_tg.cipher_id
    tg_id = user_tg.tg_id
    user_id = encryptor.decrypt(cipher_id)
    user= get_user(user_id)
    if user is None:
        return {"status": "error", "message": "Пользователь не найден"}
    update_tg_to_user(user_id, tg_id)
    return {"status":"success", "fio": user[1]}

@app.get("/order/create", response_class=HTMLResponse)
async def create_order_form(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    techniks = find_techniks()
    patients = get_all_patient()
    selected_tooth = []
    return templates.TemplateResponse("create_order.html", {
        "request": request,
        "techniks": techniks,
        "first_row": first_row,
        "second_row": second_row,
        "selected_tooth": selected_tooth,
        "job_types": types,
        "color_letter": color_letter,
        "color_number": color_number,
        "patients" : patients
    })


@app.get("/order/plan", response_class=HTMLResponse)
async def plan(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    types = procedure_type()
    patients = get_all_patient()
    return templates.TemplateResponse("plan.html", {
        "request": request,
        "first_row": first_row,
        "second_row": second_row,
        "job_types": types,
        "patients": patients
    })

@app.get("/clients")
async def plan(request: Request):
    patients = get_all_patient()
    return {"clients": [{"id" : client[0],"fio" :client[1],"birthday": client[2]} for client in patients]}

@app.get("/procedure/get/{type}/{subtype}")
async def get_name_procedure_by_type(request: Request, type: str, subtype: str):
    names = name_procedure(type, subtype)
    procedures = {"procedure": []}
    for name in names:
        procedure = {}
        procedure["id"] = name[0]
        procedure["name"] = name[2]
        procedure["price"] = name[3]
        procedures["procedure"].append(procedure)
    return procedures


@app.post("/order/create")
async def add_order(request: Request, order: Order):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    doctor = get_user(user_id)

    id = create_order(
        order.patient,
        order.formula,
        order.type,
        order.comment,
        order.fitting,
        order.deadline,
        int(order.technik),
        doctor[0],
        order.color_letter,
        order.color_number,
        int(order.price) * len(order.formula.split(", ")),
    )
    return {"order_id" : id}

@app.put("/order/price/{order_id}")
async def update_order_price(request: Request, order_id: int, price: int = Query(...), comment: str = Query(...)):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return RedirectResponse(url="/authorization")
    set_new_order_price(order_id, price)
    if comment:
        set_new_order_technik_comment(order_id, comment)
    return {"updated_price" : price}


@app.delete("/order/photo/delete/{photo_name}")
async def delete_photo(request: Request, photo_name: str):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return RedirectResponse(url="/authorization")
    delete_photo_from_order(photo_name)
    os.remove(os.path.join("orders_photo", photo_name))
    return {"deleted_photo" : photo_name}



@app.post("/order/photo/upload/{order_id}")
async def upload_photos(request: Request, order_id: int, photos: List[UploadFile] = File(...)):
    uploaded_files = []

    for photo in photos:
        extension = os.path.splitext(photo.filename)[1]
        unique_filename = f"{uuid.uuid4()}{extension}"
        file_path = os.path.join("orders_photo", unique_filename)
        with open(file_path, "wb") as file:
            content = await photo.read()
            file.write(content)
        uploaded_files.append(photo.filename)
        add_photo_to_order(order_id,unique_filename)

    return {"uploaded_files": uploaded_files}

@app.delete("/order/technik/file/delete/{file_name}")
async def delete_photo(request: Request, file_name: str):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return RedirectResponse(url="/authorization")
    delete_file_from_technik_files(file_name)
    os.remove(os.path.join("technik_files", file_name))
    return {"deleted_file" : file_name}

@app.post("/order/technik/file/upload/{order_id}")
async def upload_photos(request: Request, order_id: int, files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{extension}"
        file_path = os.path.join("technik_files", unique_filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded_files.append(file.filename)
        add_file_to_technik_files(order_id,unique_filename)

    return {"uploaded_files": uploaded_files}
@app.post("/order/update/{order_id}", response_class=HTMLResponse)
async def update_order(request: Request, order_id: int, patient: str = Form(...), formula: str = Form(...),
                       type: str = Form(...), comment: str = Form(""), fitting: str = Form(...),
                       deadline: str = Form(...), technik: str = Form(...), color: str = Form(...)):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    doctor = get_user(user_id)
    techniks = find_techniks()

    update_order_by_id(patient, formula, type, comment, fitting, deadline, int(technik), doctor[0],
                       color[0], color[1:], order_id)
    order = get_order_by_id(order_id)
    selected_tooth = order[2].split(", ")
    photos = get_photos_by_order_id(order_id)
    return templates.TemplateResponse("edit_order.html", {
        "request": request,
        "success": True,
        "first_row": first_row,
        "second_row": second_row,
        "selected_tooth": selected_tooth,
        "job_types": types,
        "color_letter": color_letter,
        "color_number": color_number,
        "techniks": techniks,
        "order": order,
        "photos": photos
    })


@app.get("/order/get/{order_id}", response_class=HTMLResponse)
async def get_order(request: Request, order_id: int):
    order = get_order_by_id(order_id)
    selected_tooth = order[2].split(", ")

    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    user = get_user(user_id)
    photos = get_photos_by_order_id(order_id)
    files = get_technik_files_by_order_id(order_id)


    if user[5] == "doctor" and order[9] != 1:
        techniks = find_techniks()
        return templates.TemplateResponse("edit_order.html", {
            "request": request,
            "first_row": first_row,
            "second_row": second_row,
            "selected_tooth": selected_tooth,
            "job_types": types,
            "color_letter": color_letter,
            "color_number": color_number,
            "techniks": techniks,
            "order": order,
            "photos": photos,
            "technik_files": files
        })
    elif  user[5] == "doctor":
        technic = get_user(order[7])
        return templates.TemplateResponse("show_order_doctor.html", {
            "request": request,
            "order": order,
            "technic": technic,
            "first_row": first_row,
            "second_row": second_row,
            "selected_tooth": selected_tooth,
            "photos": photos,
            "technik_files": files
        })
    else:
        doctor = get_user(order[6])
        return templates.TemplateResponse("show_order.html", {
            "request": request,
            "order": order,
            "doctor": doctor,
            "first_row": first_row,
            "second_row": second_row,
            "selected_tooth": selected_tooth,
            "photos": photos,
            "technik_files": files
        })


@app.get("/procedure/subtype/{type}")
async def get_subtype(request: Request, type: str):
    return get_subtype_by_type(type)


@app.get("/procedure/template/get/{type}")
async def get_subtype(request: Request, type: str):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    templates = get_template_procedure(type, user_id)
    templates_dict = {}
    # {1:
    # {"name" : "Лечение прямого кариеса", "price" : 7500, "procedure" :[
    # {""}, {}, {}
    # ]  }
    for template in templates:
        if template[0] not in templates_dict:
            templates_dict[template[0]] = {"name": template[1],"sticker": template[10], "price": 0,"tooth_depend": template[12] == 1, "procedure": []}

        templates_dict[template[0]]["procedure"].append({
            "id": template[2] if template[2] is not None else template[6],
            "type": "template" if template[2] is not None else 'user',
            "name": template[3] if template[3] is not None else template[7],
            "price": template[5] if template[5] is not None else template[8],
            "amount": template[9],
            "is_active": template[11] == 1
        })
        if template[11] == 1:
            templates_dict[template[0]]["price"] += (template[5] if template[5] is not None else template[8]) * template[9]
    return templates_dict


@app.post("/procedure/template/create/")
async def save_template(request: Request, templateProcedure: TemplateProcedure):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    new_template = create_template_procedure(templateProcedure.template_name, templateProcedure.tooth_depend, user_id)
    return {'id': new_template}


@app.post("/procedure/user/")
async def procedure(request: Request, procedure: Procedure):
    add_procedure_to_template(procedure.name, procedure.type, procedure.price, procedure.template_id, procedure.amount,procedure.is_active)
    return {"result": 'Done'}

@app.put("/procedure/user/{id}")
async def procedure(request: Request,id: int, procedure: Procedure):
    edit_user_procedure(id, procedure.name, procedure.type, procedure.price)
    print(id, procedure.template_id,procedure.amount)
    update_amount_procedure_template(id, procedure.template_id,procedure.amount,procedure.is_active)
    return {"result": 'Done'}


@app.put("/procedure/template/{id}")
async def update_template(request: Request,id: int, template: TemplateProcedure):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    update_template_name(id,template.template_name,user_id,template.tooth_depend)
    return {"result": 'Done'}
@app.put("/procedure/sticker/template")
async def update_stickers(request: Request, template: TemplateSticker):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    update_sticker_name(template.template_id,template.sticker,user_id)
    return {"result": 'Done'}

@app.delete("/procedure/user/{id}")
async def procedure(request: Request,id: int):
    delete_user_procedure(id)
    return {"result": 'Done'}


@app.delete("/procedure/template/{template_id}")
async def save_template(request: Request, template_id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    delete_template_procedure_by_id(template_id, user_id)
    print(template_id, user_id)
    return {"result": 'Done'}


@app.post("/order/done/{order_id}")
async def save_done_order(request: Request, order_id: int, done: str = Form('off')):
    done = 1 if done == 'on' else 0
    update_order_done(order_id, is_done=done)
    return RedirectResponse(url="/account")



@app.post("/order/done/fitting/{order_id}")
async def save_done_fitting_order(request: Request, order_id: int, fitting_done: str = Form('off')):
    fitting_done = 1 if fitting_done == 'on' else 0
    update_order_done(order_id, fitting_done=fitting_done)
    return RedirectResponse(url="/account")


@app.post("/order/delete/{order_id}")
async def delete_order(request: Request, order_id: int):
    delete_order_by_id(order_id)
    return RedirectResponse(url="/account")

@app.get("/technik/service/show")
async def get_technik_services(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    services = get_all_technik_services(user_id)
    return templates.TemplateResponse("technik_services.html", {
        "request": request,
        "services": services
    })

@app.get("/technik/invoice/show")
async def get_technik_services(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    invoices = get_all_technik_invoices(user_id)
    print(invoices)
    return templates.TemplateResponse("technik_invoices.html", {
        "request": request,
        "invoices": invoices
    })
@app.get("/doctor/invoice/show")
async def get_doctor_services(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    invoices = get_all_doctor_invoices(user_id)
    print(invoices)
    return templates.TemplateResponse("doctor_invoices.html", {
        "request": request,
        "invoices": invoices
    })


class Technik_service(BaseModel):
    id: int
    name: str
    price: int
@app.post("/technik/service/edit")
async def add_service(request: Request, technik_service: Technik_service):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    if str(technik_service.id) == "-1":
        add_technik_service(user_id, technik_service.name, technik_service.price)
    else:
        update_technik_service(technik_service.id, technik_service.name, technik_service.price)
    return {"result": "done"}

@app.delete("/technik/service/delete/{id}")
async def delete_service(request: Request, id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    delete_technik_service(id)
    return {"result": "done"}

@app.delete("/technik/invoice/delete/{id}")
async def delete_service(request: Request, id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    invoice = get_invoice_by_id(id)
    if invoice[4] == "Оплачено":
        return Response(content="Удаление данного счета невозможно!", status_code=400, type="application/text")
    delete_technik_invoice(id)
    delete_invoice_order(id)

    return {"result": "done"}
@app.post("/doctor/invoice/pay/{id}")
async def pay_invoice(request: Request, id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    invoice = get_invoice_by_id(id)
    if invoice[4] == "Оплачено":
        return Response(content="Оплата данного счета невозможна!", status_code=400, type="application/text")
    pay_doctor_invoice(id)
    pay_invoice_order(id)

    return {"result": "done"}

@app.get("/technik/invoice/create")
async def create_invoice_page(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is not None:
        user = get_user(user_id)
        if user[5] == "doctor":
           return RedirectResponse(url="/account")
        selected_doctors = []
        orders = get_not_paid_not_invoice_orders_technik(user[0])
        for i in range(len(orders)):
            orders[i] = list(orders[i])
            if orders[i][5]:
                data = orders[i][5].split("-")
                orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
            doctor = get_user(orders[i][6])

            if doctor[6] is not None:
                doctor_name = f"{doctor[1]} ({doctor[6]})"
            else:
                doctor_name = f"{doctor[1]}"
            orders[i][6] = {"id": doctor[0], "name": doctor_name}
            if {"id": doctor[0], "name": doctor_name} not in selected_doctors:
                selected_doctors.append({"id": doctor[0], "name": doctor_name})
        return templates.TemplateResponse(
            "create_invoice.html",
            {
                "request": request,
                'fio': user[1],
                'orders': orders,
                "doctors": selected_doctors,
            })

    return RedirectResponse(url="/authorization")
@app.post("/technik/invoice/create")
async def create_invoice(request: Request,create_invoice: CreateInvoice):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is not None:
        user = get_user(user_id)
        if user[5] == "doctor":
           return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
        current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        orders = []
        for order_id in create_invoice.orders:
            orders.append(get_order_by_id(order_id))
        total_price = 0
        for order in orders:
            total_price += order[14]
        invoice_id = add_invoice(current_time, create_invoice.doctor_id, user_id,total_price)
        for order in orders:
            add_invoice_order(invoice_id, order[0])
    # return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
@app.get("/technik/service/list")
async def get_services(request: Request):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    services = get_all_technik_services(user_id)
    return {"services": [{"id": service[0], "name" : service[2], "price" : service[3] } for service in services]}

@app.get("/technik/invoice/{id}/orders")
async def get_orders(request: Request,id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    orders = get_technik_invoice_orders(id)
    return {"orders": [{
        "id": order[0],
        "doctor":f"{order[-2]} {f'({order[-1]})' if order[-1] is not None else ''}".strip(),
        "patient": order[2],
        "formula": order[3],
        "type": order[4],
        "price": order[5]
    } for order in orders]}
@app.get("/technik/service/get/{technik_id}")
async def get_services(request: Request,technik_id: int):
    services = get_all_technik_services(technik_id)
    return {"services": [{"id": service[0], "name" : service[2], "price" : service[3] } for service in services]}


@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/authorization")
    response.delete_cookie("session")
    return response
class PlanModel(BaseModel):
    fio: str
    birthday: str
@app.post("/plan/create")
async def create_plan(request: Request, plan: PlanModel):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    plan_id = create_plan_db(plan.fio.title().strip(), datetime.datetime.now(), user_id, plan.birthday)
    return {"plan_id":plan_id}

class ServiceModel(BaseModel):
    stage : str
    template_id: int
    tooths : str
    plan_id: int


@app.post("/plan/service/create")
async def create_service(request: Request, service: ServiceModel):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    service_id = create_service_db(service.stage, service.template_id, service.tooths, service.plan_id)
    return {"service_id": service_id}

@app.get("/plan/document/{plan_id}")
async def get_document(request: Request, plan_id: int):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    if user_id is None:
        return Response(content="Ошибка авторизации!", status_code=401, type="application/text")
    data = get_patient_data_plan_by_id(plan_id,user_id)
    data = {
        "fio": str(data[0]),
        "birthday": str(data[1]),
        "data_day": str(datetime.datetime.now().strftime("%d.%m.%Y"))
    }
    get_stages = get_stages_plan_id(plan_id)
    total_price = 0

    stages = []
    done_stages = []
    for stage in get_stages:
        if (stage[0], stage[1]) in done_stages:
            if int(stage[9]):
                stage_i = done_stages.index((stage[0],stage[1]))
                if stage[2] not in stages[stage_i]['templates']:
                    stages[stage_i]['templates'][stage[2]] = {'name' : stage[3], 'items' : []}
                    stages[stage_i]['sticker'].append(stage[4])
                stages[stage_i]['templates'][stage[2]]["items"].append({
                    "no": len(stages[stage_i]['templates'][stage[2]]["items"]) + 1,
                    "service": stage[5],
                    "price_per_unit": stage[6],
                    "quantity":  stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(",")),
                    "total":  (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6],
                })
                stages[stage_i]['total_price'] +=  (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6]
        else:
            stages.append({
                "number": len([stages for stage in stages if stage["templates"]]) + 1  if int(stage[9]) else -1,
                "stage": stage[0],
                'total_price' : (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6] if int(stage[9]) else 0,
                'tooth' : stage[1],
                'sticker' : [stage[4]],
                "templates": {
                    stage[2]: {'name' : stage[3], 'items' : [
                        {
                            "no": 1,
                            "service": stage[5],
                            "price_per_unit": stage[6],
                            "quantity":  stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(",")),
                            "total": (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6],
                        }
                    ]}
                } if int(stage[9]) else {}
            })
            done_stages.append((stage[0],stage[1]))
        total_price +=  (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6] if int(stage[9]) else 0
    print(stages)
    file_name = f'{data["fio"].replace(" ", "_")}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
    output_path =  os.getcwd() +f'/treatment_plans/{file_name}'
    generate_plan(stages, data,total_price,
                  output_path=output_path + ".docx")
    # -------------WINDOWS--------------------
    # convert(output_path + ".docx", output_path + "no_icons.pdf")
    # ---------------LINUX------------------
    original_directory = os.getcwd()
    os.chdir('treatment_plans')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', output_path + ".docx"], check=True)
    os.chdir(original_directory)
    default_pdf_name = os.path.splitext(output_path + ".docx")[0] + ".pdf"
    os.rename(default_pdf_name, output_path + "no_icons.pdf")
    # ---------------------------------------
    file_handle = fitz.open(output_path + "no_icons.pdf")
    page = file_handle[0]
    tooth_images = {} # {17: ['gutta', '']}
    for stage in stages:
        images = stage["sticker"]
        tooths = stage["tooth"].split(",")
        for image in images:
            if image == "tooth":
                continue
            for tooth in tooths:
                tooth = int(tooth)
                if tooth not in tooth_images:
                    tooth_images[tooth] = []
                tooth_images[tooth].append(image)
    for tooth, images in tooth_images.items():
        images.sort(key=lambda image: tooth_priority.index(image))
        for image in images:
            image_to_pdf(image, int(tooth), page)
    file_handle.save(output_path + ".pdf")
    file_handle.close()
    os.remove(output_path + "no_icons.pdf")

    return {"document_word":file_name + ".docx","document_pdf":file_name + ".pdf"}

if __name__ == "__main__":
    if os.path.exists("/etc/letsencrypt/live/drlink.ru/privkey.pem"):
        app.add_middleware(HTTPSRedirectMiddleware)
        uvicorn.run("main:app",
                    host="0.0.0.0",
                    port=443,
                    reload=True,
                    ssl_keyfile="/etc/letsencrypt/live/drlink.ru/privkey.pem",
                    ssl_certfile="/etc/letsencrypt/live/drlink.ru/fullchain.pem")
    else:
        uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
