from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, JSONResponse
import uvicorn
from src.core.requests import ocb_request, filter_request, block_date_request, reference_get, reference
from src.core.prototype import prototype
import json
import os
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.core.response_format import response_format
from src.logic.factory_entities import factory_entities
from src.reposity import reposity
from src.start_service import start_service
from src.models.settings_model import settings_model
from src.logic.factory_converters import factory_converters
from src.core.validator import validator
from src.core.abstract_dto import object_to_dto
from src.logic.ocb import ocb
from src.logic.rests import rests
from datetime import datetime
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.logic.reference_service import reference_service
from src.logic.logger_service import logger_service
from src.dtos.logger_dto import logger_dto

# Инициализация сервиса
settings_file = "./settings.json"
service = start_service()
settings = settings_model()
settings.response_format = response_format.json_format()
factory_entity = factory_entities(settings)
factory_converter = factory_converters()
logger = logger_service()

app = FastAPI(title="REST API Service")

content_types = {
    response_format.json_format(): 'application/json; charset=utf-8',
    response_format.xml_format(): 'application/json; charset=utf-8',
    response_format.csv_format(): 'text/csv; charset=utf-8',
    response_format.markdown_format(): 'text/markdown; charset=utf-8'
}

@app.get("/api/status")
async def status():
    # Логгирование
    log_message = f"GET /api/status - проверка доступности API"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    return {"status": "success"}

@app.get("/api/responses/models")
async def get_response_models():
    # Логгирование
    log_message = f"GET /api/responses/models - получение списка доступных моделей"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    return [key for key in reposity.keys()]

@app.get("/api/responses/formats")
async def get_response_formats():
    # Логгирование
    log_message = f"GET /api/responses/formats - получение списка доступных форматов"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    return [format for format in response_format.keys()]

@app.get("/api/block_date/current")
async def get_current_block_date():
    block_date = service.block_date.strftime("%Y-%m-%d")
    result = {"block_date": block_date}
    # Логгирование
    log_message = f"GET /api/block_date/current - запрос текущей даты блокировки {block_date}"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")

@app.get("/api/block_date/rests/{date_str}")
async def get_rests_at_date(date_str: str):
    date = validator.validate_datetime_from_str(date_str)
    result = rests().show_rests(date)
    # Логгирование
    log_message = f"GET /api/block_date/rests/{date_str} - запрос остатков на дату блокировки {date_str}"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    return JSONResponse(content=object_to_dto(result), media_type="application/json; charset=utf-8")

@app.post("/api/block_date/update")
async def update_block_date(request: block_date_request):
    log_message = f"POST /api/block_date/update - запрос на обновление даты блокировки"
    log_dto = logger_dto().create_debug("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    try:
        observe_service.create_event(event_type.change_block_period(), {"new_block_date": request.new_block_date})
        result = {"status": "success", "new_block_date": datetime.strftime(request.new_block_date, "%Y-%m-%d")}
        return JSONResponse(content=result, media_type="application/json; charset=utf-8")
    except Exception as e:
        log_message = f"Обновнение даты блокировки завершилось с ошибкой {e}"
        log_dto = logger_dto().create_error("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ocb")
async def ocb_(request: ocb_request):
    filters = filter_sorting_dto(request.filters["filters"], request.filters["sorting"])
    result = ocb(service).create(request.start_date, request.end_date, request.storage_id, filters)

    log_message = f"POST /api/ocb - построить сальдовую ведомость на период с {request.start_date.strftime("%Y-%m-%d")} по {request.end_date.strftime("%Y-%m-%d")}"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)

    if result:
        converted_result = factory_converter.convert(result)
        return JSONResponse(content=object_to_dto(converted_result), media_type="application/json; charset=utf-8")
    else:
        raise HTTPException(status_code=404)
    
@app.post("/api/data")
async def filter_data(request: filter_request):
    log_message = f"POST /api/data - отфильтровать модели"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    if request.model not in reposity.keys():
        log_message = f"POST /api/data - модель {request.model} не найдена в репозитории"
        log_dto = logger_dto().create_error("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        raise HTTPException(
            status_code=400,
            detail=f"Model '{request.model}' not found. Available: {list(reposity.keys())}"
        )
    models = service.data[request.model]
    filters = filter_sorting_dto(request.filters["filters"], request.filters["sorting"])
    proto = prototype(models)
    proto = prototype.filter(proto, filters)
    factory = factory_converters()
    result = factory.convert(proto.data)
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")



@app.post("/api/save")
async def save_data(path:str= Query(..., description="Путь для сохранения файла")):
    log_message = f"POST /api/save - запрос на сохранение репозитория в файл {path}"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    try:
        service.save_reposity(file_path = path)
        log_message = f"Сохранение успешно завершено в файл {path}"
        log_dto = logger_dto().create_debug("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        return {"status": "SUCCESS", "saved_to": os.path.abspath(path)}
    except Exception as e:
        log_message = f"Запрос завершен с ошибкой {e}"
        log_dto = logger_dto().create_error("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        return {"status": "ERROR", "error": e}

@app.get("/api/reference/{id}")
async def get_reference(id:str):
    model = service.repo.get_by_unique_code(id)
    log_message = f"GET /api/reference/{id} - поиск объекта по уникальному коду"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    if model:
        log_message = f"Объект с кодом {id} найден"
        log_dto = logger_dto().create_debug("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        return JSONResponse(content=factory_converter.convert(model), media_type="application/json; charset=utf-8")
    else:
        log_message = f"Объект с кодом {id} не найден"
        log_dto = logger_dto().create_error("API", log_message)
        observe_service.create_event(event_type.log(), log_dto)
        raise HTTPException(status_code=400, detail=f"Объект с кодом {id} не найден.")

@app.put("/api/reference")
async def put_reference(request: reference):
    log_message = f"PUT /api/reference - запрос на добавление нового объекта в репозиторий"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    try:
        reference_service.add(request.type, request.properties)
        return {"status":"SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.patch("/api/reference")
async def patch_reference(request: reference):
    log_message = f"PATCH /api/reference - запрос на изменение объекта в репозитории"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    if not "unique_code" in request.properties.keys():
        raise HTTPException(status_code=400, detail=f"Отсутствует необходимое поле unique_code")
    try:
        reference_service.change(request.type, request.properties)
        return {"status":"SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.delete("/api/reference")
async def remove_reference(request: reference):
    log_message = f"DELETE /api/reference - запрос на удаление объекта из репозитория"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    if not "unique_code" in request.properties.keys():
        raise HTTPException(status_code=400, detail=f"Отсутствует необходимое поле unique_code")
    try:
        reference_service.remove(request.type, request.properties)
        return {"status":"SUCCESS"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e)

@app.get("/api/responses/build")
async def build_response(
    format: str = Query(..., description="Формат ответа"),
    model_type: str = Query(..., description="Тип модели")
):
    log_message = f"GET /api/response/build - запрос на получение моделей {model_type} в формате {format}"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    format = format.lower()
    if format not in response_format.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Format '{format}' not supported. Available: {list(response_format.keys())}"
        )
    
    if model_type not in reposity.keys():
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_type}' not found. Available: {list(reposity.keys())}"
        )

    models = service.data[model_type]
    result = factory_entity.create(format)().create(models)
    content_type = content_types.get(format, 'application/json; charset=utf-8')

    return Response(content=result, media_type=content_type)

@app.get("/api/recipes/get_recipes")
async def get_recipes():
    log_message = f"GET /api/recipes/get_recipes - запрос на получение рецептов"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    recipes = service.data[reposity.recipe_key()]
    result = factory_converter.convert(recipes)
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")

@app.get("/api/recipes/get_recipe/{id}")
async def get_recipe(id: str):
    log_message = f"GET /api/recipes/get_recipe/{id} - запрос на получение рецепта по уникальному коду {id}"
    log_dto = logger_dto().create_info("API", log_message)
    observe_service.create_event(event_type.log(), log_dto)
    recipe = next(filter(lambda r: r.unique_code == id, service.data[reposity.recipe_key()]), None)
    if recipe:
        result = factory_converter.convert(recipe)
        return JSONResponse(content=result, media_type="application/json; charset=utf-8")
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")

if __name__ == '__main__':
    service.start(settings_file)
    uvicorn.run(app, host="127.0.0.1", port=8080)
