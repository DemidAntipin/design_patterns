from src.models.settings_model import settings_model
from src.core.validator import argument_exception
from src.core.validator import operation_exception
from src.core.validator import validator
from src.models.company_model import company_model
from src.core.abstract_subscriber import abstract_subscriber
from src.core.event_type import event_type
from src.core.observe_service import observe_service
from datetime import datetime
from src.dtos.logger_dto import logger_dto
import json
import os
from src.dtos.block_date_dto import block_date_dto

####################################################3
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class settings_manager(abstract_subscriber):
    # Наименование файла (полный путь)
    __file_name:str = ""

    # Настройки
    __settings:settings_model = None

    # Логгер
    __logger = None

    # Singletone
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
            observe_service.add(cls.instance)
        return cls.instance

    def __init__(self):
        self.default()

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

    @property
    def logger(self):
        return self.__logger
    
    @logger.setter
    def logger(self, logger):
        from src.logic.logger_service import logger_service
        validator.validate(logger, logger_service)
        self.__logger = logger

    # Загрузить настройки из Json файла
    def load(self) -> bool:
        if self.__file_name == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            __load_match = {
               "company": self.__load_company,
               "logging": self.__load_logging_settings
            }
            with open( self.__file_name, 'r', encoding="utf-8") as file_instance:
                settings = json.load(file_instance)
                result = True
                for key in settings.keys():
                    if key in __load_match:
                        data = settings[key]
                        result = result and __load_match[key](data)
            return result
        except:
            return False
        
    # Загрузить модель компании
    def __load_company(self, data: dict) -> bool:
        validator.validate(data, dict)
        fields = list(filter(lambda x: not x.startswith("_") , dir(self.__settings.company))) 
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self.__settings.company, key, data[key])
        except:
            return False        

        return True
    
    def __load_logging_settings(self, data: dict) -> bool:
        validator.validate(data, dict)
        fields = list(filter(lambda x: not x.startswith("_") , dir(self.__settings))) 
        matching_keys = list(filter(lambda key: key in fields, data.keys()))
        try:
            for key in matching_keys:
                setattr(self.__settings, key, data[key])
        except:
            return False        
        return True


    # Параметры настроек по умолчанию
    def default(self):
        company = company_model()
        company.name = "Ромашка"
        self.__settings = settings_model()
        self.__settings.company = company
        self.__settings.block_date = datetime(1900, 1, 1)
        self.__settings.logging_level = "DEBUG"
        self.__settings.logging_mode = "BOTH"
        self.__settings.logging_format = "{timestamp} | {level} | {source} | {message}"
        self.__settings.logging_dir = "logs"

    """
    Обработка событий
    """
    def handle(self, event:str, params:block_date_dto):
        super().handle(event, params)

        if event == event_type.change_block_period():
            validator.validate(params, block_date_dto)
            new_block_date = params.new_block_date
            validator.validate(new_block_date, datetime)
            old_date = self.__settings.block_date
            self.__settings.block_date = new_block_date

            # Логгирование
            log_message = f"Изменена дата блокировки c {old_date.strftime(self.settings.datetime_format)} на {new_block_date.strftime(self.settings.datetime_format)}"
            log_dto = logger_dto().create_info("settings_manager", log_message)
            observe_service.create_event(event_type.log(), log_dto)