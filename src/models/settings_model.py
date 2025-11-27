from src.models import company_model
from src.core.validator import validator
from datetime import datetime

######################################
# Модель настроек приложения
class settings_model():
    __company:company_model = None
    __response_format:str = None
    __datetime_format: str = "%Y-%m-%d"
    __start_date: datetime = datetime(1900, 1, 1)
    __block_date: datetime = None

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