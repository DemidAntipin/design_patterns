from src.reposity import reposity
from src.models.measure_model import measure_model
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomeclature_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.ingredient_model import ingredient_model
from src.dtos.nomenclature_dto import nomenclature_dto
from src.dtos.ingredient_dto import ingredient_dto
from src.dtos.measure_dto import measure_dto
from src.dtos.category_dto import category_dto
from src.core.validator import validator, argument_exception, operation_exception
from src.models.storage_model import storage_model
from src.models.transaction_model import transaction_model
from src.dtos.transaction_dto import transaction_dto
from src.dtos.recipe_dto import recipe_dto
from src.dtos.storage_dto import storage_dto
from src.logic.factory_converters import factory_converters
from src.core.abstract_dto import object_to_dto
from src.models.settings_model import settings_model
from src.settings_manager import settings_manager
from datetime import datetime
from src.core.observe_service import observe_service
from src.core.abstract_subscriber import abstract_subscriber
from src.core.event_type import event_type
from src.core.common import common
import os
import json
from src.dtos.reference_dto import reference_dto
from src.dtos.update_dependencies_dto import update_dependencies_dto
from src.dtos.check_dependencies_dto import check_dependencies_dto

class start_service(abstract_subscriber):
    __repo:reposity = reposity()

    # Первый запуск
    __first_start = True

    # Словарь который содержит загруженные и инициализованные инстансы нужных объектов
    # Ключ - id записи, значение - abstract_model
    __cache = {}

    __match = {
        reposity.nomenclature_key() : (nomenclature_dto, nomeclature_model),
        reposity.measure_key() : (measure_dto, measure_model),
        reposity.nomenclature_group_key() : (category_dto, nomenclature_group_model),
        reposity.storage_key() : (storage_dto, storage_model)
    }

    __settings: settings_manager = None

    # Наименование файла (полный путь)
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()
        self.__settings = settings_manager()
        observe_service.add(self)


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
        
    @property
    def repo(self) -> reposity:
        return self.__repo

    @repo.setter
    def repo(self, repo:reposity):
        validator.validate(repo, reposity)
        self.__repo = repo
        
    @property
    def first_start(self) -> bool:
        return self.__first_start
    
    @first_start.setter
    def first_start(self, value:bool):
        validator.validate(value, bool)
        self.__first_start = value

    @property
    def block_date(self) -> datetime:
        return self.__settings.settings.block_date
    
    @block_date.setter
    def block_date(self, value:datetime):
        validator.validate(value, datetime)
        self.__settings.settings.block_date = value

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open( self.__full_file_name, 'r', encoding="utf-8") as file_instance:
                settings = json.load(file_instance)

                if "block_date" in settings.keys():
                    self.__settings.settings.block_date = datetime.strptime(settings["block_date"], self.__settings.settings.datetime_format)
                else:
                    return False

                if "first_start" in settings.keys():
                    self.first_start = settings["first_start"]

                if self.first_start:
                    self.first_start = False
                    if "default_recipe" in settings.keys():
                        data = settings["default_recipe"]
                        return self.convert(data)
                    return False
                else:
                    return True
        except Exception as e:
            error_message = str(e)
            raise Exception(error_message)
        
    # Сохранить элемент в репозитории
    def __save_item(self, key:str, dto, item):
        validator.validate(key, str)
        item.unique_code = dto.id
        self.__cache.setdefault(dto.id, item)
        self.__repo.data[ key ].append(item)

    # Удалить элемент из репозитория
    def __pop_item(self, key:str, item):
        validator.validate(key, str)
        item = self.__cache.pop(item.unique_code)
        self.__repo.data[key].remove(item)

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
    

    def __convert_storages(   self, data: dict) -> bool:
        validator.validate(data, dict)      
        storages = data['storages'] if 'storages' in data else []   
        if len(storages) == 0:
            return False
         
        for storage in storages:
            dto = category_dto().create(storage)
            item = storage_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.storage_key(), dto, item )

        return True

    def __convert_transactions(   self, data: dict) -> bool:
        validator.validate(data, dict)      
        transactions = data['transactions'] if 'transactions' in data else []   
        if len(transactions) == 0:
            return False
         
        for transaction in transactions:
            dto = transaction_dto().create(transaction)
            item = transaction_model.from_dto(dto, self.__cache)
            self.__save_item( reposity.transaction_key(), dto, item )

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
        self.__convert_storages(data)   
        self.__convert_transactions(data)  


        # Собираем рецепт
        compositions =  data['composition'] if 'composition' in data else []
        ingredients_list = []
        for composition in compositions:
            dto = ingredient_dto().create(composition)
            item = ingredient_model.from_dto(dto, self.__cache)
            ingredients_list.append(item)
        self.__default_recipe.ingredients = ingredients_list

        self.__default_recipe.unique_code = data["id"]    
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
        
    """
    Сохранить репозиторий в файл
    """
    def save_reposity(self, file_path: str):
        validator.validate(file_path, str)
        abs_path = os.path.abspath(file_path)
        factory_converter = factory_converters()
        save = self.data[reposity.rest_key()]
        self.data[reposity.rest_key()] = list(self.data[reposity.rest_key()].values())
        result = factory_converter.convert(self.data)
        result["block_date"] = datetime.strftime(self.block_date, self.__settings.settings.datetime_format)
        result["first_start"] = self.first_start
        self.data[reposity.rest_key()] = save
        with open(abs_path, 'w', encoding='utf-8') as file:
            json.dump(object_to_dto(result), file, ensure_ascii=False, indent=2)

    """
    Обработка событий
    """
    def handle(self, event:str, params:reference_dto):
        super().handle(event, params)

        if event == event_type.add_reference():
            validator.validate(params, reference_dto)
            model_type = params.name
            if model_type not in self.__match.keys():
                raise argument_exception(f"Получена неизвестная модель {model_type}. Доступны только следующие модели: {self.__match.keys()}")
            dto = self.__match[model_type][0]().create(params.model_dto_dict)
            model = self.__match[model_type][1].from_dto(dto, self.__cache)
            if model not in self.data[model_type]:
                self.__save_item(model_type, dto, model)
        elif event == event_type.change_reference():
            validator.validate(params, reference_dto)
            model_type = params.name
            # Получить объект по коду
            old_model = self.repo.get_by_unique_code(params.id)
            if not old_model:
                raise operation_exception(f"Объект с кодом {params.id} не найден.")
            self.data[reposity.rest_key()]=list(self.data[reposity.rest_key()].values())
            # Получить dto объекта, обновить его и перезаписать объект
            dto_dict = object_to_dto(factory_converters().convert(old_model))
            dto_dict.update(params.model_dto_dict)
            dto = self.__match[model_type][0]().create(dto_dict)
            model=self.__match[model_type][1].from_dto(dto, self.__cache)
            update_dto = update_dependencies_dto().create({"old_model":old_model, "new_model":model})
            # Рассылка всем моделям проверить зависимость от old_model, и обновится, если зависимость обнаружена.
            observe_service.create_event( event_type.update_dependencies(), update_dto)
            self.__pop_item(model_type, old_model)
            self.__save_item(model_type, dto, model)
            self.data[reposity.rest_key()] = {rest.nomenclature.unique_code: rest for rest in self.data[reposity.rest_key()]}
        elif event == event_type.remove_reference():
            validator.validate(params, reference_dto)
            model_type = params.name
            # Получить объект по коду
            model = self.repo.get_by_unique_code(params.id)
            if not model:
                raise operation_exception(f"Объект с кодом {params.id} не найден.")
            check_dto = check_dependencies_dto().create({"model":model})
            # Рассылка всем моделям проверить зависимость от model, и вызвать исключение, если зависимость обнаружна.
            observe_service.create_event(event_type.check_dependencies(), check_dto)
            self.__pop_item(model_type, model)
        elif event == event_type.change_block_period():
            self.save_reposity("appsettings.json")