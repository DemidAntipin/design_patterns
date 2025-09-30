from src.core.validator import validator
from src.core.abstract_reference import abstact_reference

######################################
# Модель склада
class storage_model(abstact_reference):
    __name:str = ""

    # Наименование
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str):
        validator.validate(value, str)
        self.__name = value.strip()