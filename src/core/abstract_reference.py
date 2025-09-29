from abc import ABC
import uuid
from src.core.validator import validator


# Абстрактная модель с полем уникального кода для однозначной идентификации объектов. От AbstractModel наследуются все модели приложения.
class abstact_reference(ABC):
    # Уникальный ID модели
    __unique_code:str

    # Наименование модели (50)
    __name: str = ""

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    
    # Уникальный код
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()
    
    # Наименование модели 
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 50)
        self.__name = value.strip()

    # Перегрузка штатного варианта сравнения
    def __eq__(self, value: str) -> bool:
        return self.__unique_code == value
