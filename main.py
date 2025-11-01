from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import Response, JSONResponse
import uvicorn
import datetime
from typing import List, Optional
import json

from src.core.response_format import response_format
from src.logic.factory_entities import factory_entities
from src.reposity import reposity
from src.start_service import start_service
from src.models.settings_model import settings_model
from src.logic.factory_converters import factory_converters
from src.core.validator import validator
from src.core.abstract_dto import object_to_dto

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

@app.get("/api/ocb/{storage_id}/{start_date}/{end_date}")
async def ocb(start_date: str,end_date: str,storage_id: str):
    start_date, end_date = validator.validate_period(start_date, end_date)
    validator.validate_id(storage_id, [value for value in service.data[reposity.storage_key()]])
    
    result = []
    income_all_transactions = list(filter(lambda transaction: transaction.storage.unique_code == storage_id, service.data[reposity.income_transaction_key()]))
    outcome_all_transactions = list(filter(lambda transaction: transaction.storage.unique_code == storage_id, service.data[reposity.outcome_transaction_key()]))
    for nomenclature in service.data[reposity.nomenclature_key()]:
        init_value = 0
        income = 0
        outcome = 0
        income_transactions = sorted([transaction for transaction in income_all_transactions if transaction.nomenclature == nomenclature and transaction.date <= end_date], key=lambda x: x.date)
        outcome_transactions = sorted([transaction for transaction in outcome_all_transactions if transaction.nomenclature == nomenclature and transaction.date <= end_date], key=lambda x: x.date)
        
        measure = nomenclature.measure.get_base_unit()
        
        # предполагается, что транзакции могут быть в любой единице измерения, но все они сводятся к 1 базовой - measure
        for transaction in income_transactions:
            if transaction.date < start_date:
                init_value += transaction.measure.to_base_unit_value(transaction.value)
            else:
                income += transaction.measure.to_base_unit_value(transaction.value)
                
        for transaction in outcome_transactions:
            if transaction.date < start_date:
                init_value -= transaction.measure.to_base_unit_value(transaction.value)
            else:
                outcome += transaction.measure.to_base_unit_value(transaction.value)
                
        end_value = init_value + income - outcome
        item = {
            "start_value": init_value,
            "nomenclature": nomenclature,
            "measure": measure,
            "income": income,
            "outcome": outcome,
            "end_value": end_value
        }
        result.append(item)
        
    if result:
        converted_result = factory_converter.convert(result)
        return JSONResponse(content=object_to_dto(converted_result), media_type="application/json; charset=utf-8")
    else:
        raise HTTPException(status_code=404, detail="No data found")

@app.post("/api/save")
async def save_data():
    result = factory_converter.convert(service.data)
    filename = "saved_data.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(object_to_dto(result), file, ensure_ascii=False, indent=2)
    return {"status": "SUCCESS"}

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
