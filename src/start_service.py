from src.reposity import reposity
from src.models.measure_model import measure_model
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomeclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.ingredient_model import ingredient_model
from src.dtos.nomenclature_dto import nomenclature_dto
from src.dtos.measure_dto import measure_dto
from src.dtos.category_dto import category_dto
from src.core.validator import validator, argument_exception, operation_exception
import os
import json

class start_service():
    __repo:reposity = reposity()

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    # Наименование файла (полный путь)
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

     # Текущий файл
    @property
    def file_name(self) -> str:
        return self.__full_file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)        
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.__full_file_name, 'r', encoding="utf-8") as file_instance:
                settings = json.load(file_instance)

                if "default_recipe" in settings.keys():
                    data = settings["default_recipe"]
                    return self.convert(data)

            return False
        except Exception as e:
            error_message = str(e)
            raise Exception(error_message)
        
    # Сохранить элемент в репозитории
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[ key ].append(item)

    # Загрузить единицы измерений   
    def __convert_measures(self, data: dict) -> bool:
        validator.validate(data, dict)
        measures = data['measures'] if 'measures' in data else []    
        if len(measures) == 0:
            return False
         
        for measure in measures:
            dto = measure_dto().create(measure)
            item = measure_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.measure_key(), dto, item )

        return True

    # Загрузить группы номенклатуры
    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories =  data['categories'] if 'categories' in data else []    
        if len(categories) == 0:
            return False

        for category in  categories:
            dto = category_dto().create(category)    
            item = nomenclature_group_model.from_dto(dto, self.__cache )
            self.__save_item( reposity.nomenclature_group_key(), dto, item )

        return True

    # Загрузить номенклатуру
    def __convert_nomenclatures(   self, data: dict) -> bool:
        validator.validate(data, dict)      
        nomenclatures = data['nomenclatures'] if 'nomenclatures' in data else []   
        if len(nomenclatures) == 0:
            return False
         
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomeclature_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.nomenclature_key(), dto, item )

        return True        


    # Обработать полученный словарь    
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # 1 Созданим рецепт
        name = data['name'] if 'name' in data else "НЕ ИЗВЕСТНО"
        self.__default_recipe = recipe_model.create(name)

        # Загрузим шаги приготовления
        steps =  data['steps'] if 'steps' in data else []
        for step in steps:
            if step.strip() != "":
                validator.validate(step, str)
        self.__default_recipe.description = steps

        self.__convert_measures(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)        


        # Собираем рецепт
        compositions =  data['composition'] if 'composition' in data else []
        ingredients_list = []
        for composition in compositions:
            namnomenclature_id = composition['nomenclature_id'] if 'nomenclature_id' in composition else ""
            value  = composition['value'] if 'value' in composition else ""
            nomenclature = self.__cache[namnomenclature_id] if namnomenclature_id in self.__cache else None
            item = ingredient_model.create(nomenclature, value)
            ingredients_list.append(item)
        self.__default_recipe.ingredients = ingredients_list
            
        # Сохраняем рецепт
        self.__repo.data[ reposity.recipe_key()].append(self.__default_recipe)

        return True

    """
    Стартовый набор данных
    """
    @property
    def data(self):
        return self.__repo.data   

    """
    Основной метод для генерации эталонных данных
    """
    def start(self, file="settings.json"):
        self.file_name = file
        result = self.load()
        if result == False:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")