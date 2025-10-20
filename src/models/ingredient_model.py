from src.core.entity_model import entity_model
from src.models.nomenclature_model import nomeclature_model
from src.core.validator import validator

# Модель элемента рецепта
class ingredient_model(entity_model):
    __nomenclature:nomeclature_model
    __value:int

    @property
    def nomenclature(self) -> nomeclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value:nomeclature_model):
        validator.validate(value, nomeclature_model)
        self.__nomenclature=value

    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, amount: int):
        validator.validate(amount, int)
        self.__value=amount

    # Фабричный метод
    def create(nomenclature:nomeclature_model,  value:int):
        item = ingredient_model()
        item.__nomenclature = nomenclature
        item.__value = value
        item.name = item.nomenclature.name
        return item