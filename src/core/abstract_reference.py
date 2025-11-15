from abc import ABC
import uuid
from src.core.validator import validator
from functools import total_ordering


# Абстрактная модель с полем уникального кода для однозначной идентификации объектов. От AbstractModel наследуются все модели приложения.
# total_ordering, используя методы __eq__ и __lt__, сгенерирует остальные сравнения автоматически
@total_ordering
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
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, abstact_reference):
            return False
        return self.unique_code == value.unique_code
    
    # Перегрузка штатного варианта сравнения
    def __lt__(self, value: object):
        if not isinstance(value, abstact_reference):
            return False
        return self.unique_code < value.unique_code
    
    def __contains__(self, value) -> bool:
        from src.core.common import common
        values = common.get_values(self)
        return any(value == item or (isinstance(item, (list, tuple, abstact_reference, str)) and value in item) for item in values)
    
    def __str__(self):
        return self.unique_code