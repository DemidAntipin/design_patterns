from src.models.measure_model import measure_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.core.validator import validator
from src.core.abstract_reference import abstact_reference
import uuid

######################################
# Модель номенклатуры
class nomeclature_model(abstact_reference):    
    # группа номенклатуры
    __nomenclature_group: nomenclature_group_model = None

    # единица измерения
    __measure_unit: measure_model = None

    # Проверка на уникальность номенклатуры
    __instances = {}
    def __new__(cls, name, *args, **kwargs):
        if not name in cls.__instances:
            instance = super().__new__(cls)
            cls.__instances[name] = instance
        return cls.__instances[name]

    def __init__(self, name:str):
        super().__init__()
        self.name=name

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
        item = nomeclature_model(name)
        item.nomenclature_group=group
        item.measure_unit=measure_unit
        return item
    
    @staticmethod
    def create_empty():
        id = uuid.uuid4().hex
        item = nomeclature_model(id)
        item.name = "Default_name"
        return item