from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, JSONResponse
import uvicorn
from src.core.requests import ocb_request, filter_request, block_date_request
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

# Инициализация сервиса
settings_file = "./settings.json"
service = start_service()
settings = settings_model()
settings.response_format = response_format.json_format()
factory_entity = factory_entities(settings)
factory_converter = factory_converters()

app = FastAPI(title="REST API Service")

content_types = {
    response_format.json_format(): 'application/json; charset=utf-8',
    response_format.xml_format(): 'application/json; charset=utf-8',
    response_format.csv_format(): 'text/csv; charset=utf-8',
    response_format.markdown_format(): 'text/markdown; charset=utf-8'
}

@app.get("/api/status")
async def status():
    return {"status": "success"}

@app.get("/api/responses/models")
async def get_response_models():
    return [key for key in reposity.keys()]

@app.get("/api/responses/formats")
async def get_response_formats():
    return [format for format in response_format.keys()]

@app.get("/api/block_date/current")
async def get_current_block_date():
    result = {"block_date": datetime.strftime(service.block_date, "%Y-%m-%d")}
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")

@app.get("/api/block_date/rests/{date_str}")
async def get_rests_at_date(date_str: str):
    date = validator.validate_datetime_from_str(date_str)
    result = rests().show_rests(date)
    return JSONResponse(content=object_to_dto(result), media_type="application/json; charset=utf-8")

@app.post("/api/block_date/update")
async def update_block_date(request: block_date_request):
    try:
        rests().update_block_date(request.new_block_date)
        result = {"status": "success", "new_block_date": datetime.strftime(request.new_block_date, "%Y-%m-%d")}
        return JSONResponse(content=result, media_type="application/json; charset=utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ocb")
async def ocb_(request: ocb_request):
    filters = filter_sorting_dto(request.filters["filters"], request.filters["sorting"])
    result = ocb(service).create(request.start_date, request.end_date, request.storage_id, filters)
        
    if result:
        converted_result = factory_converter.convert(result)
        return JSONResponse(content=object_to_dto(converted_result), media_type="application/json; charset=utf-8")
    else:
        raise HTTPException(status_code=404)
    
@app.post("/api/data")
async def filter_data(request: filter_request):
    if request.model not in reposity.keys():
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



@app.post("/api/save/")
async def save_data(path:str= Query(..., description="Путь для сохранения файла")):
    try:
        service.save_reposity(file_path = path)
        return {"status": "SUCCESS", "saved_to": os.path.abspath(path)}
    except Exception as e:
        return {"status": "ERROR", "error": e}

@app.get("/api/responses/build")
async def build_response(
    format: str = Query(..., description="Формат ответа"),
    model_type: str = Query(..., description="Тип модели")
):
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
    recipes = service.data[reposity.recipe_key()]
    result = factory_converter.convert(recipes)
    return JSONResponse(content=result, media_type="application/json; charset=utf-8")

@app.get("/api/recipes/get_recipe/{id}")
async def get_recipe(id: str):
    recipe = next(filter(lambda r: r.unique_code == id, service.data[reposity.recipe_key()]), None)
    if recipe:
        result = factory_converter.convert(recipe)
        return JSONResponse(content=result, media_type="application/json; charset=utf-8")
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")

if __name__ == '__main__':
    service.start(settings_file)
    uvicorn.run(app, host="127.0.0.1", port=8080)
