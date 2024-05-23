from typing import List

from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import uvicorn

from Database import autorization, registration, find_techniks, get_user, create_order, get_orders_doctor, \
    get_orders_technik, get_order_by_id, update_order_done, delete_order_by_id, update_order_by_id
from parameters import first_row, second_row, types, color_letter, color_number

app = FastAPI()
app.mount("/css", StaticFiles(directory="templates/css"), name="css")
app.mount("/js", StaticFiles(directory="templates/js"), name="js")
app.mount("/images", StaticFiles(directory="templates/images"), name="images")
current_user = None

class UserAuthorization(BaseModel):
    email: str
    password: str


templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="account")


def get_current_user(token: str = Depends(oauth2_scheme)):
    print(token)
    user = get_user(token)  # (id, fio, ...)
    if user[0] == token:
        return user
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")


@app.get("/authorization", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("authorization.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def initial(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/registration", response_class=HTMLResponse)
async def regist(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


# @app.post("/check", response_class=HTMLResponse)
# async def check_login_password(user : UserAuthorization):
#     email = user.email
#     password =user.password
#     print(email, password)
#     res = autorization(email, password)
#     if res == True:
#         return templates.TemplateResponse("technik_personal_account.html")
#     else:
#         return templates.TemplateResponse("wrong_authorization.html")



@app.route("/account",methods=['GET', 'POST'])
async def account(request: Request):
    if current_user is not None:
        if current_user[5] == "doctor":
            orders = get_orders_doctor(current_user[0])
            done = []
            fitting_done = []
            not_done = []
            for order in orders:
                if order[9] == 0 and order[12] == 0:
                    not_done.append(order)
                elif order[9] == 0 and order[12] == 1:
                    fitting_done.append(order)
                else:
                    done.append(order)
            return templates.TemplateResponse("doctor_personal_account.html",
                  {
                      "request": request,
                      'fio': current_user[1],
                      "done": done,
                      "fitting_done": fitting_done,
                      "not_done": not_done
                  })
        else:
            orders = get_orders_technik(current_user[0])
            done = []
            fitting_done = []
            not_done = []
            for order in orders:
                if order[9] == 0 and order[12] == 0:
                    not_done.append(order)
                elif order[9] == 0 and order[12] == 1:
                    fitting_done.append(order)
                else:
                    done.append(order)
            return templates.TemplateResponse(
                "technik_personal_account.html",
                  {
                      "request": request,
                      'fio': current_user[1],
                      "done":done,
                      "fitting_done":fitting_done,
                      "not_done":not_done
                  })

    return templates.TemplateResponse("authorization.html", {"request": request})


@app.post("/account/enter", response_class=HTMLResponse)
async def check_login_password(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    global current_user
    email = form_data.username
    password = form_data.password
    print(email, password)
    res = autorization(email, password)
    if res:
        current_user = res[0]


    return RedirectResponse(url="/account")


@app.post("/registration", response_class=HTMLResponse)
async def regist(request: Request, fio: str = Form(...), username: str = Form(...),
                 email: str = Form(...), password: str = Form(...), speciality: str = Form(...),
                 repeat_password: str = Form(...)):
    res = registration(fio, username, email, password, speciality, repeat_password)
    if res == False:
        return templates.TemplateResponse("registration.html", {"request": request})
    else:
        return templates.TemplateResponse("authorization.html", {"request": request})

@app.get("/order/create", response_class=HTMLResponse)
async def regist(request: Request):
    techniks = find_techniks()
    selected_tooth = []
    return templates.TemplateResponse("create_order.html", {
        "request": request,
        "techniks": techniks,
        "first_row":first_row,
        "second_row":second_row,
        "selected_tooth":selected_tooth,
        "job_types": types,
        "color_letter": color_letter,
        "color_number": color_number
    })
@app.get("/order/plan", response_class=HTMLResponse)
async def plan(request: Request):
    return templates.TemplateResponse("plan.html",{"request": request})


@app.post("/order/create", response_class=HTMLResponse)
async def add_order(request: Request, patient: str = Form(...), formula: str = Form(...),
                    type: str = Form(...), comment: str = Form(""), fitting: str = Form(...),
                    deadline: str = Form(...), technik: str = Form(...), color_letter: str = Form(...),
                    color_number: str = Form(...)):
    doctor = get_user(current_user[0])
    techniks = find_techniks()

    selected_tooth = []
    create_order(patient, formula, type, comment, fitting, deadline, int(technik), doctor[0],
                 color_letter,color_number)
    return templates.TemplateResponse("create_order.html", {
        "request": request,
        "success": True,
        "first_row": first_row,
        "second_row": second_row,
        "selected_tooth": selected_tooth,
        "job_types": types,
        "color_letter": color_letter,
        "color_number": color_number,
        "techniks": techniks,
    })
@app.post("/order/update/{order_id}", response_class=HTMLResponse)
async def update_order(request: Request, order_id: int ,patient: str = Form(...), formula: str = Form(...),
                    type: str = Form(...), comment: str = Form(""), fitting: str = Form(...),
                    deadline: str = Form(...), technik: str = Form(...), color_letter: str = Form(...),
                    color_number: str = Form(...)):
    doctor = get_user(current_user[0])
    techniks = find_techniks()

    update_order_by_id(patient, formula, type, comment, fitting, deadline, int(technik), doctor[0],
                 color_letter,color_number,order_id)
    order = get_order_by_id(order_id)
    selected_tooth = list(map(int,order[2].split(", ")))
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
        "order" : order
    })

@app.get("/order/get/{order_id}", response_class=HTMLResponse)
async def get_order(request: Request, order_id: int):
    order = get_order_by_id(order_id)
    selected_tooth = list(map(int,order[2].split(", ")))

    if current_user[5] == "doctor":
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
            "first_row":first_row,
            "second_row":second_row,
            "selected_tooth":selected_tooth
        })
@app.post("/order/done/{order_id}")
async def save_done_order(request: Request,order_id:int,done : str = Form('off')):
    done = 1 if done == 'on' else 0
    update_order_done(order_id, is_done = done)
    return RedirectResponse(url="/account")

@app.post("/order/done/fitting/{order_id}")
async def save_done_order(request: Request,order_id:int,fitting_done : str = Form('off')):
    fitting_done = 1 if fitting_done == 'on' else 0
    update_order_done(order_id, fitting_done=fitting_done)
    return RedirectResponse(url="/account")

@app.post("/order/delete/{order_id}")
async def delete_order(request: Request,order_id:int):
    delete_order_by_id(order_id)
    return RedirectResponse(url="/account")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=80, reload=True)