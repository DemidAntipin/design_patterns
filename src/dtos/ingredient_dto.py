from src.core.abstract_dto import abstact_dto

class ingredient_dto(abstact_dto):
    __name: str = None
    __nomenclature_id: str = None
    __value: int = 0

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id
    
    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value

    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, val):
        self.__value = val