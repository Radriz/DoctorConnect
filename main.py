from typing import Optional

from fastapi import FastAPI, Form, Depends, HTTPException, Request
from fastapi.openapi.models import Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
import uvicorn
from itsdangerous import URLSafeSerializer, BadSignature

from Database import autorization, registration, find_techniks, get_user, create_order, get_orders_doctor, \
    get_orders_technik, get_order_by_id, update_order_done, delete_order_by_id, update_order_by_id, procedure_type, \
    name_procedure, get_subtype_by_type, get_template_procedure, create_template_procedure, \
    delete_template_procedure_by_id, add_procedure_to_template, edit_user_procedure, delete_user_procedure, \
    update_amount_procedure_template, update_template_name
from parameters import first_row, second_row, types, color_letter, color_number

app = FastAPI()
app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/images", StaticFiles(directory="templates/images"), name="images")

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



class Procedure(BaseModel):
    name: str
    type: str
    price: int
    template_id: int
    amount: int


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
                data = orders[i][5].split("-")
                orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                technik = get_user(orders[i][7])
                orders[i][7] = technik[1]

        else:
            orders = get_orders_technik(user[0])
            for i in range(len(orders)):
                orders[i] = list(orders[i])
                data = orders[i][5].split("-")
                orders[i][5] = f"{data[2]}.{data[1]}.{data[0]}"
                doctor = get_user(orders[i][6])
                if doctor[6] is not None:
                    orders[i][6] = f"{doctor[1]} ({doctor[6]})"
                else:
                    orders[i][6] = f"{doctor[1]}"

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
                    "not_done": not_done
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
                 repeat_password: str = Form(...)):
    res = registration(fio, email, password, speciality, repeat_password)
    if not res:
        return templates.TemplateResponse("registration.html", {"request": request})
    else:
        return templates.TemplateResponse("authorization.html", {"request": request})


@app.get("/order/create", response_class=HTMLResponse)
async def create_order_form(request: Request):
    techniks = find_techniks()
    selected_tooth = []
    return templates.TemplateResponse("create_order.html", {
        "request": request,
        "techniks": techniks,
        "first_row": first_row,
        "second_row": second_row,
        "selected_tooth": selected_tooth,
        "job_types": types,
        "color_letter": color_letter,
        "color_number": color_number
    })


@app.get("/order/plan", response_class=HTMLResponse)
async def plan(request: Request):
    types = procedure_type()
    return templates.TemplateResponse("plan.html", {
        "request": request,
        "first_row": first_row,
        "second_row": second_row,
        "job_types": types
    })


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


@app.post("/order/create", response_class=HTMLResponse)
async def add_order(request: Request, order: Order):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    doctor = get_user(user_id)

    create_order(
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
    return Response(content="Успешно!", status_code=200, type="application/text")


@app.post("/order/update/{order_id}", response_class=HTMLResponse)
async def update_order(request: Request, order_id: int, patient: str = Form(...), formula: str = Form(...),
                       type: str = Form(...), comment: str = Form(""), fitting: str = Form(...),
                       deadline: str = Form(...), technik: str = Form(...), color_letter: str = Form(...),
                       color_number: str = Form(...)):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
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
    user_id = read_session(session_cookie)
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
            templates_dict[template[0]] = {"name": template[1],"sticker": template[10], "price": 0, "procedure": []}

        templates_dict[template[0]]["procedure"].append({
            "id": template[2] if template[2] is not None else template[6],
            "type": "template" if template[2] is not None else 'user',
            "name": template[3] if template[3] is not None else template[7],
            "price": template[5] if template[5] is not None else template[8],
            "amount": template[9]
        })
        templates_dict[template[0]]["price"] += (template[5] if template[5] is not None else template[8]) * template[9]
    return templates_dict


@app.post("/procedure/template/create/")
async def save_template(request: Request, templateProcedure: TemplateProcedure):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    new_template = create_template_procedure(templateProcedure.template_name, user_id)
    return {'id': new_template}


@app.post("/procedure/user/")
async def procedure(request: Request, procedure: Procedure):
    add_procedure_to_template(procedure.name, procedure.type, procedure.price, procedure.template_id, procedure.amount)
    return {"result": 'Done'}

@app.put("/procedure/user/{id}")
async def procedure(request: Request,id: int, procedure: Procedure):
    edit_user_procedure(id, procedure.name, procedure.type, procedure.price)
    print(id, procedure.template_id,procedure.amount)
    update_amount_procedure_template(id, procedure.template_id,procedure.amount)
    return {"result": 'Done'}


@app.put("/procedure/template/{id}")
async def update_template(request: Request,id: int, template: TemplateProcedure):
    session_cookie = request.cookies.get("session")
    user_id = read_session(session_cookie)
    update_template_name(id,template.template_name,user_id)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("main:app",
    #             host="0.0.0.0",
    #             port=443,
    #             reload=True,
    #             ssl_keyfile="/etc/letsencrypt/live/drlink.ru/privkey.pem",
    #             ssl_certfile="/etc/letsencrypt/live/drlink.ru/fullchain.pem")
