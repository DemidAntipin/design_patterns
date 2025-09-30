from src.core.abstract_reference import abstact_reference
from src.core.validator import validator

# Модель единиц измерения для моделей номенклатуры
class measure_model(abstact_reference):
    # Базовая единица измерения
    __base_unit = None
    # Коэффициент пересчёта
    __coef: int

    def __init__(self, name: str, coef: int, base_unit = None):
        super().__init__()
        
        self.name = name
        self.coef = coef
        self.base_unit = base_unit

    # Поле коэффициента пересчёта
    @property
    def coef(self) -> float:
        return self.__coef
    
    @coef.setter
    def coef(self, value: int):
        validator.validate(value, int)
        self.__coef = float(value)     

    # Базовая единица измерения
    @property
    def base_unit(self):
        return self.__base_unit
    
    @base_unit.setter
    def base_unit(self, value):
        validator.validate(value, measure_model, allow_null=True)
        self.__base_unit = value