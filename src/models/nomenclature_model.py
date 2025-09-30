from src.models.measure_model import measure_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.core.validator import validator
from src.core.abstract_reference import abstact_reference

######################################
# Модель номенклатуры
class nomeclature_model(abstact_reference):
    # полное наименование
    __full_name: str = ""
    
    # группа номенклатуры
    __nomenclature_group: nomenclature_group_model = None

    # единица измерения
    __measure_unit: measure_model = None

    # Полное название номенклатуры
    @property
    def full_name(self) -> str:
        return self.__full_name
    
    @full_name.setter
    def full_name(self, value: str) -> str:
        validator.validate(value, str, 255)
        self.__full_name = value

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