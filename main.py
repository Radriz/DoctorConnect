import datetime
import os
import subprocess
import time
import uuid
from typing import Optional, List

import fitz
from docx2pdf import convert
import pypandoc
from fastapi import FastAPI, Form, Depends, HTTPException, Request, UploadFile, File
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
    get_all_patient, get_patient_data_plan_by_id, get_stages_plan_id, add_photo_to_order
from add_image import image_to_pdf
from document_generate import generate_plan
from parameters import first_row, second_row, types, color_letter, color_number

app = FastAPI()


app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/images", StaticFiles(directory="templates/images"), name="images")
app.mount("/plans", StaticFiles(directory="treatment_plans"), name="treatment_plan")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account")

SECRET_KEY = "your-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)


class UserAuthorization(BaseModel):
    email: str
    password: str


class Order(BaseModel):
    patient: str
    formula: str
    type: str
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



def create_session(user_id):
    return serializer.dumps({"user_id": user_id})


def read_session(session_cookie: str):
    try:
        data = serializer.loads(session_cookie)
        return data.get("user_id")
    except BadSignature:
        return None


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
            orders = get_orders_doctor(user[0])
            for i in range(len(orders)):
                orders[i] = list(orders[i])
                if orders[i][5]:
                    data = orders[i][5].split("-")
                    orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                technik = get_user(orders[i][7])
                orders[i][7] = technik[1]

        else:
            selected_doctors = []
            orders = get_orders_technik(user[0])
            for i in range(len(orders)):
                orders[i] = list(orders[i])
                if orders[i][5]:
                    data = orders[i][5].split("-")
                    orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                doctor = get_user(orders[i][6])
                selected_doctors.append({"id" : doctor[0], "name" : ""})
                if doctor[6] is not None:
                    selected_doctors[-1]["name"] = f"{doctor[1]} ({doctor[6]})"
                else:
                    selected_doctors[-1]["name"] = f"{doctor[1]}"
                orders[i][6] =  selected_doctors[-1]

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
                                                  "not_done": not_done
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
        order.color_number
    )
    return {"order_id" : id}

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
@app.post("/order/update/{order_id}", response_class=HTMLResponse)
async def update_order(request: Request, order_id: int, patient: str = Form(...), formula: str = Form(...),
                       type: str = Form(...), comment: str = Form(""), fitting: str = Form(...),
                       deadline: str = Form(...), technik: str = Form(...), color_letter: str = Form(...),
                       color_number: str = Form(...)):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    doctor = get_user(user_id)
    techniks = find_techniks()

    update_order_by_id(patient, formula, type, comment, fitting, deadline, int(technik), doctor[0],
                       color_letter, color_number, order_id)
    order = get_order_by_id(order_id)
    selected_tooth = list(map(int, order[2].split(", ")))
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
        "order": order
    })


@app.get("/order/get/{order_id}", response_class=HTMLResponse)
async def get_order(request: Request, order_id: int):
    order = get_order_by_id(order_id)
    selected_tooth = list(map(int, order[2].split(", ")))

    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie) if session_cookie else None
    if user_id is None:
        return RedirectResponse(url="/authorization")
    user = get_user(user_id)

    if user[5] == "doctor":
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
            "order": order
        })
    else:
        doctor = get_user(order[6])
        return templates.TemplateResponse("show_order.html", {
            "request": request,
            "order": order,
            "doctor": doctor,
            "first_row": first_row,
            "second_row": second_row,
            "selected_tooth": selected_tooth
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
                "number": len(done_stages) + 1,
                "stage": stage[0],
                'total_price' : (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6],
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
                }
            })
            done_stages.append((stage[0],stage[1]))
        total_price +=  (stage[7] if stage[8] == 0 else stage[7] * len(stage[1].split(","))) * stage[6]
    print(stages)
    file_name = f'{data["fio"].replace(" ", "_")}_{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}'
    output_path =  os.getcwd() +f'/treatment_plans/{file_name}'
    generate_plan(stages, data,total_price,
                  output_path=output_path + ".docx")
    # convert(output_path + ".docx", output_path + "no_icons.pdf")
    original_directory = os.getcwd()
    os.chdir('treatment_plans')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf:writer_pdf_Export', output_path + ".docx"], check=True)
    os.chdir(original_directory)
    default_pdf_name = os.path.splitext(output_path + ".docx")[0] + ".pdf"
    os.rename(default_pdf_name, output_path + "no_icons.pdf")
    file_handle = fitz.open(output_path + "no_icons.pdf")
    page = file_handle[0]
    for stage in stages:
        images = stage["sticker"]
        tooths = stage["tooth"].split(",")
        for image in images:
            if image == "tooth":
                continue
            for tooth in tooths:
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
