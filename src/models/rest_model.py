from src.models.measure_model import measure_model
from src.models.nomenclature_model import nomeclature_model
from src.core.validator import validator
from src.dtos.rest_dto import rest_dto
from src.core.abstract_reference import abstact_reference
import uuid

######################################
# Модель номенклатуры
class rest_model(abstact_reference):
    # номенклатура
    __nomenclature: nomeclature_model = None

    # единица измерения
    __measure: measure_model = None

    # остаток
    __value: float = 0

    # номенклатура
    @property
    def nomenclature(self) -> nomeclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomeclature_model):
        validator.validate(value, nomeclature_model)
        self.__nomenclature = value

    # Текущая единица измерения
    @property
    def measure(self):
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value

    # остаток
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: float):
        validator.validate(value, (int, float))
        self.__value = value

    # Универсальный метод - фабричный.
    @staticmethod
    def create(nomenclature: nomeclature_model, measure: measure_model, value: float):
        validator.validate(nomenclature, nomeclature_model)
        validator.validate(measure, measure_model)
        validator.validate(value, (int, float))
        item = rest_model()
        item.nomenclature = nomenclature
        item.measure = measure
        item.value = value
        return item
    
    """
    Фабричный метод из Dto
    """
    def from_dto(dto:rest_dto, cache:dict):
        validator.validate(dto, rest_dto)
        validator.validate(cache, dict)
        range =  cache[ dto.measure_id ] if dto.measure_id in cache else None
        nomenclature =  cache[ dto.nomenclature_id] if dto.nomenclature_id in cache else None
        item  = rest_model.create(nomenclature, range, dto.rest)
        return item