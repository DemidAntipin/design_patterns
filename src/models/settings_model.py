from src.models import company_model
from src.core.validator import validator

######################################
# Модель настроек приложения
class settings_model():
    __company:company_model = None
    __response_format:str = None

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