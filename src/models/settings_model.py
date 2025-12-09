from src.models import company_model
from src.core.validator import validator
from datetime import datetime
from src.core.log_level import log_level
from src.core.log_mode import log_mode

######################################
# Модель настроек приложения
class settings_model():
    __company:company_model = None
    __response_format:str = None
    __datetime_format: str = "%Y-%m-%d"
    __start_date: datetime = datetime(1900, 1, 1)
    __block_date: datetime = None

    # Настройки логирования
    __logging_level: log_level = None
    __logging_mode: log_mode = None
    __logging_dir: str = None
    __logging_format: str = None

    # Текущая организация
    @property
    def company(self) -> company_model:
        return self.__company

    @company.setter
    def company(self, value: company_model):
        validator.validate(value, company_model)
        self.__company = value

    @property
    def response_format(self) -> str:
        return self.__response_format
    
    @response_format.setter
    def response_format(self, value: str):
        validator.validate(value, str)
        self.__response_format = value

    @property
    def datetime_format(self) -> str:
        return self.__datetime_format

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def block_date(self) -> datetime:
        return self.__block_date
    
    @block_date.setter
    def block_date(self, value: datetime):
        validator.validate(value, datetime)
        self.__block_date = value

    @property
    def logging_level(self) -> log_level:
        return self.__logging_level
    
    @logging_level.setter
    def logging_level(self, value: str):
        validator.validate(value, str)
        if value in log_level.levels():
            self.__logging_level = log_level[value]

    @property
    def logging_mode(self) -> log_mode:
        return self.__logging_mode
    
    @logging_mode.setter
    def logging_mode(self, value: str):
        validator.validate(value, str)
        if value in log_mode.mods():
            self.__logging_mode = log_mode[value]

    @property
    def logging_dir(self) -> str:
        return self.__logging_dir
    
    @logging_dir.setter
    def logging_dir(self, value: str):
        validator.validate(value, str)
        self.__logging_dir = value

    @property
    def logging_format(self) -> str:
        return self.__logging_format
    
    @logging_format.setter
    def logging_format(self, value: str):
        validator.validate(value, str)
        self.__logging_format = value