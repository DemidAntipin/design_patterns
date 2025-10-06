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

    # Проверка на уникальность ед. измерения
    __instances = {}
    def __new__(cls, name, *args, **kwargs):
        if not name in cls.__instances:
            instance = super().__new__(cls)
            cls.__instances[name] = instance
        return cls.__instances[name]

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

    @staticmethod
    def create_kilogramm():
        base_unit = measure_model.create_gramm()
        return measure_model.create("килограмм", 1000, base_unit)

    @staticmethod
    def create_gramm():
        return measure_model.create("грамм", 1)
    
    @staticmethod
    def create_piece():
        return measure_model.create("шт", 1)

    # Универсальный метод - фабричный.
    @staticmethod
    def create(name: str, coef: int, base: 'measure_model' = None):
        validator.validate(name, str)
        validator.validate(coef, int)
        inner_base = None
        if not base is None:
            validator.validate(base, measure_model)
            inner_base = base
        item = measure_model(name, coef, inner_base)
        return item