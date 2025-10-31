from src.dtos.measure_dto import measure_dto
from src.core.entity_model import entity_model
from src.core.validator import validator

# Модель единиц измерения для моделей номенклатуры
class measure_model(entity_model):
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

    @staticmethod
    def create_kilogramm(gramm):
        validator.validate(gramm, measure_model)
        return measure_model.create("килограмм", 1000, gramm)

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
    
    # перевод value к базовым ед. измерения
    def to_base_unit_value(self, value: int):
        if self.base_unit is None:
            return value * self.coef
        else:
            return self.coef * self.base_unit.to_base_unit_value(value)
        
    # перевод value из базовых ед. измерения
    def from_base_unit_value(self, value: float):
        if self.base_unit is None:
            return value / self.coef
        else:
            return self.base_unit.from_base_unit_value(value) / self.coef

    # Получить базовую единицу измерения
    def get_base_unit(self) -> 'measure_model':
        if self.base_unit is None:
            return self
        else:
            return self.base_unit.get_base_unit()

    """
    Фабричный метод из Dto
    """
    def from_dto(dto:measure_dto, cache:dict):
        validator.validate(dto, measure_dto)
        validator.validate(cache, dict)
        base  = cache[ dto.base_id ] if dto.base_id in cache else None
        item = measure_model.create(dto.name, dto.value, base)
        return item