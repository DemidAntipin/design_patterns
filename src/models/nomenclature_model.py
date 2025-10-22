from src.models.measure_model import measure_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.core.validator import validator
from src.dtos.nomenclature_dto import nomenclature_dto
from src.core.entity_model import entity_model
import uuid

######################################
# Модель номенклатуры
class nomeclature_model(entity_model):
    # Полное наименование номенклатуры (255)
    __name: str = ""
    # группа номенклатуры
    __nomenclature_group: nomenclature_group_model = None

    # единица измерения
    __measure_unit: measure_model = None

    # Полное название номенклатуры
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> str:
        validator.validate(value, str, 255)
        self.__name = value

    # Текущая группа номенклатуры
    @property
    def nomenclature_group(self):
        return self.__nomenclature_group
    
    @nomenclature_group.setter
    def nomenclature_group(self, value: nomenclature_group_model):
        validator.validate(value, nomenclature_group_model)
        self.__nomenclature_group = value 

    # Текущая единица измерения
    @property
    def measure_unit(self):
        return self.__measure_unit
    
    @measure_unit.setter
    def measure_unit(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure_unit = value

    # Универсальный метод - фабричный.
    @staticmethod
    def create(name: str, group: nomenclature_group_model, measure_unit: measure_model):
        validator.validate(name, str, 255)
        validator.validate(group, nomenclature_group_model)
        validator.validate(measure_unit, measure_model)
        item = nomeclature_model()
        item.name = name
        item.nomenclature_group=group
        item.measure_unit=measure_unit
        return item
    
    """
    Фабричный метод из Dto
    """
    def from_dto(dto:nomenclature_dto, cache:dict):
        validator.validate(dto, nomenclature_dto)
        validator.validate(cache, dict)
        range =  cache[ dto.measure_id ] if dto.measure_id in cache else None
        category =  cache[ dto.category_id] if dto.category_id in cache else None
        item  = nomeclature_model.create(dto.name, category, range)
        return item