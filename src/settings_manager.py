from src.models.settings_model import settings_model
from src.core.validator import argument_exception
from src.core.validator import operation_exception
from src.core.validator import validator
from src.models.company_model import company_model
from src.core.abstract_subscriber import abstract_subscriber
from src.core.event_type import event_type
from src.core.observe_service import observe_service
from datetime import datetime
import json
import os

####################################################3
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager(abstract_subscriber):
    # Наименование файла (полный путь)
    __file_name:str = ""

    # Настройки
    __settings:settings_model = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.default()
        observe_service.add(self)

    # Текущие настройки
    @property
    def settings(self) -> settings_model:
        return self.__settings
    
    @settings.setter
    def settings(self, value: settings_model):
        if isinstance(value, settings_model):
            self.__settings = value
    
    # Текущий каталог
    @property
    def file_name(self) -> str:
        return self.__file_name

    # Полный путь к файлу настроек
    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        file_name = os.path.abspath(value)        
        if os.path.exists(file_name):
            self.__file_name = file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {file_name}')

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            with open( self.__file_name, 'r', encoding="utf-8") as file_instance:
                settings = json.load(file_instance)
                if "company" in settings.keys():
                    data = settings["company"]
                    return self.convert(data)
            return False
        except:
            return False
        
    # Обработать полученный словарь  
    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)
        fields = list(filter(lambda x: not x.startswith("_") , dir(self.__settings.company))) 
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False        

        return True

    # Параметры настроек по умолчанию
    def default(self):
        company = company_model()
        company.name = "Ромашка"
        self.__settings = settings_model()
        self.__settings.company = company

    """
    Обработка событий
    """
    def handle(self, event:str, params:dict):
        validator.validate(params, dict)
        super().handle(event, params)

        if event == event_type.change_block_period():
            new_block_date = params["new_block_date"]
            validator.validate(new_block_date, datetime)
            self.__settings.block_date = new_block_date