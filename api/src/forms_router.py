from json import dumps

from fastapi import APIRouter
from fastapi import Request, Depends
from fastapi.responses import Response

from db_cntx import get_db
from model import Form
from utils import get_field_type

router = APIRouter()


@router.post("/upload_form")
async def upload_form(request: Request, db=Depends(get_db)):
    """
    Ручка для добавления шаблона формы.
    Пример:
    example.com/upload_form?name=qwerty&user_phone=phone&test=text
    создаст новую запись в бд с именем qwerty и вернёт её в ответе.
    """
    params = dict(request.query_params)
    name = params.pop("name")
    for item in params.values():
        if item not in ['email', 'phone', 'date', 'text']:
            return 'Wrong type ' + str(item)
    form = Form(name=name, **params)
    created_form_id = await db.forms.insert_one(form.dict())
    created_form = Form.parse_obj(
        await db.forms.find_one({"_id": created_form_id.inserted_id})
    )
    return Response(created_form.json(), status_code=201, media_type="application/json")


@router.post("/get_form")
async def get_form(request: Request, db=Depends(get_db)):
    """
    Ручка для получения подходящего шаблона для заполненной формы.
    Пример:
    example.com/get_form?user_phone=8 (456) 789-56-43&test=tttexttt&zxc=123
    будет искать подходящий шаблон по имени полей и их типу, если не найдёт -
    выведет поля и их типы из заполненной формы
    """
    params = dict(request.query_params)
    for param in params:
        params[param] = get_field_type(params[param])
    query = {"$and": []}
    for param in params:
        query["$and"].append({"$or": [
            {param: params[param]},
            {param: {"$exists": False}}
        ]})
    result = await db.forms.find_one(query)
    if result is None:
        return Response(dumps(params), status_code=404, media_type="application/json")
    form = Form(**result)
    return Response(form.json(), status_code=200, media_type="application/json")
