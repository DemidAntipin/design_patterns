import pathlib
import unittest
from src.reposity import reposity
from src.start_service import start_service
import json
from src.dtos.measure_dto import measure_dto
from src.dtos.category_dto import category_dto
from src.dtos.nomenclature_dto import nomenclature_dto
from src.dtos.recipe_dto import recipe_dto
from src.dtos.storage_dto import storage_dto
from src.dtos.transaction_dto import transaction_dto
from src.models.ingredient_model import ingredient_model
from src.models.measure_model import measure_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomeclature_model
from src.models.recipe_model import recipe_model
from src.models.storage_model import storage_model
from src.models.transaction_model import transaction_model
from src.models.rest_model import rest_model
from src.dtos.rest_dto import rest_dto
from src.logic.rests import rests
from datetime import datetime

class test_saving_reposity(unittest.TestCase):
    # Путь до файла с тестовыми настройками
    __settings_name: str = "tests/data/settings_models.json"

    # Путь до файла с сохраненными моделями
    __saved_reposity: str = "tests/data/saved_data.json"

    # Объект сервиса
    __start_service: start_service = start_service()

    __cache = {}

    __repo = {}

    __match={
        "measure_model": (measure_dto, measure_model),
        "nomenclature_group_model": (category_dto, nomenclature_group_model),
        "nomenclature_model": (nomenclature_dto, nomeclature_model),
        "storage_model":(storage_dto, storage_model),
        "transaction_model": (transaction_dto, transaction_model),
        "recipe_model": (recipe_dto, recipe_model),
        "rest_model": (rest_dto, rest_model)
    }

    # Метод загрузки объектов определенной модели по dto из файла
    def preload(self, data:dict, model:str):
        data = data[model]
        for item in data:
            dto = self.__match[model][0]().create(item)
            mod = self.__match[model][1].from_dto(dto, self.__cache)
            mod.unique_code = dto.id
            self.__cache.setdefault(dto.id, mod)
            if mod not in self.__repo[model]:
                self.__repo[model].append(mod)

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        for key in self.__match.keys():
            self.__repo[key] = []
        self.__start_service.start(self.__settings_name)
        rests().update_block_date(self.__start_service.block_date)

    # Проверка единиц измерения
    def test_save_measures(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        
        # Действие
        
        # Проверки
        assert "measure_model" in data
        for measure in data["measure_model"]:
            dto = measure_dto().create(measure)
            model = measure_model.from_dto(dto, self.__cache)
            assert isinstance(model, measure_model)
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.measure_key()]
    
    # Проверка групп номенклатур
    def test_save_nomenclature_groups(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        
        # Действие
        
        # Проверки
        assert "nomenclature_group_model" in data
        for group in data["nomenclature_group_model"]:
            dto = category_dto().create(group)
            model = nomenclature_group_model.from_dto(dto, self.__cache)
            assert isinstance(model, nomenclature_group_model)
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.nomenclature_group_key()]

    # Проверка номенклатур
    def test_save_nomenclature(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.preload(data, "nomenclature_group_model")
        self.preload(data, "measure_model")

        # Действие

        # Проверки
        assert "nomenclature_model" in data
        for nomenclature in data["nomenclature_model"]:
            dto = nomenclature_dto().create(nomenclature)
            model = nomeclature_model.from_dto(dto, self.__cache)
            assert isinstance(model, nomeclature_model)
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.nomenclature_key()]

    # Проверка складов
    def test_save_storages(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        
        # Действие
        
        # Проверки
        assert "storage_model" in data
        for storage in data["storage_model"]:
            dto = storage_dto().create(storage)
            model = storage_model.from_dto(dto, self.__cache)
            assert isinstance(model, storage_model)
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.storage_key()]

    # Проверка рецептов
    def test_save_recipe(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.preload(data, "nomenclature_group_model")
        self.preload(data, "measure_model")
        self.preload(data, "nomenclature_model")

        # Действие

        # Проверки
        assert "recipe_model" in data
        for recipe in data["recipe_model"]:
            dto = recipe_dto().create(recipe)
            model = recipe_model.from_dto(dto, self.__cache)
            assert isinstance(model, recipe_model)
            assert isinstance(model.ingredients, list)
            for ingredient in model.ingredients:
                assert isinstance(ingredient, ingredient_model)
            for i, step in enumerate(model.description):
                assert isinstance(step, str)
                assert step == self.__start_service.data[reposity.recipe_key()][0].description[i]
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.recipe_key()]

    # Проверка транзакций
    def test_save_transactions(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.preload(data, "nomenclature_group_model")
        self.preload(data, "measure_model")
        self.preload(data, "nomenclature_model")
        self.preload(data, "storage_model")
        
        # Действие
        
        # Проверки
        assert "transaction_model" in data
        for transaction in data["transaction_model"]:
            dto = transaction_dto().create(transaction)
            model = transaction_model.from_dto(dto, self.__cache)
            assert isinstance(model, transaction_model)
            model.unique_code = dto.id
            assert model in self.__start_service.data[reposity.transaction_key()]

    # Проверка остатков
    def test_save_rests(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.preload(data, "nomenclature_group_model")
        self.preload(data, "measure_model")
        self.preload(data, "nomenclature_model")
        self.preload(data, "storage_model")
        self.preload(data, "transaction_model")

        # Действие

        # Проверки
        assert "rest_model" in data
        for rest in data["rest_model"]:
            dto = rest_dto().create(rest)
            model = rest_model.from_dto(dto, self.__cache)
            assert isinstance(model, rest_model)
            model.unique_code = dto.id
            rest_from_service = self.__start_service.data[reposity.rest_key()][model.nomenclature.unique_code]
            assert model.nomenclature == rest_from_service.nomenclature
            assert model.measure == rest_from_service.measure
            assert model.value == rest_from_service.value

    # Проверка всего репозитория
    def test_save_reposity(self):
        # Подготовка
        with open(self.__saved_reposity, 'r', encoding="utf-8") as file:
            data = json.load(file)
        self.preload(data, "nomenclature_group_model")
        self.preload(data, "measure_model")
        self.preload(data, "nomenclature_model")
        self.preload(data, "storage_model")
        self.preload(data, "transaction_model")
        self.preload(data, "recipe_model")
        self.preload(data, "rest_model")

        # Действие

        # Проверки
        self.__repo == self.__start_service.data

if __name__ == '__main__':
    unittest.main() 