import connexion
from flask import request, Response

from src.core.response_format import response_format
from src.logic.factory_entities import factory_entities
from src.reposity import reposity
from src.start_service import start_service
from src.models.settings_model import settings_model
from src.logic.factory_converters import factory_converters

import json

settings_file = "./settings.json"
service = start_service()
settings = settings_model()
settings.response_format = response_format.json_format()
factory_entity = factory_entities(settings)
factory_converter = factory_converters()

app = connexion.FlaskApp(__name__)

content_types = {
    response_format.json_format(): 'application/json; charset=utf-8',
    response_format.xml_format(): 'application/json; charset=utf-8',
    response_format.csv_format(): 'text/csv; charset=utf-8',
    response_format.markdown_format(): 'text/markdown; charset=utf-8'
}

"""Проверить доступность REST API"""
@app.route("/api/status", methods=['GET'])
def status():
    return {"status": "success"}

"""Типы моделей, доступные для формирования ответов"""
@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    return [key for key in reposity.keys()]

"""Доступные форматы ответов"""
@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    return [format for format in response_format.keys()]

"""Сформировать ответ для моделей (model) в переданном формате (format)"""
@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format = request.args.get('format')
    if format is None:
        return {"error": "param 'format' must be transmitted"}
    format = format.lower()
    if format not in get_response_formats():
        return {
            "error": f"not such format '{format}'. Available: "
                    f"{get_response_formats()}"
        }
    content_type = content_types.get(format)
    model_type = request.args.get('model')
    if model_type is None:
        return {"error": "param 'model' must be transmitted"}
    if model_type not in get_response_models():
        return {
            "error": f"not such model '{model_type}'. "
                    f"Available: {get_response_models()}"
        }

    models = service.data[model_type]
    result = factory_entity.create(format)().create(format, models)

    return Response(result, content_type=content_type)

"""Получить представление всего списка рецептов в Json формате"""
@app.route("/api/recipes/get_recipes", methods=['GET'])
def get_recipes():
    recipes = service.data[reposity.recipe_key()]
    result = factory_converter.create(recipes).convert(recipes)
    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")

"""Получить представление конкретного рецепта по его id в Json формате"""
@app.route("/api/recipes/get_recipe/<id>", methods=['GET'])
def get_recipe(id: str):
    recipe = next(filter(lambda r: r.unique_code == id, service.data[reposity.recipe_key()]), None)
    result = factory_converter.create(recipe).convert(recipe)
    if result:
        return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")
    else:
        return Response(status=404)
    
if __name__ == '__main__':
    service.start(settings_file)
    app.run(host="127.0.0.1", port = 8080)