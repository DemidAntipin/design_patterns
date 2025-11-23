from src.core.abstract_dto import abstact_dto

class rest_dto(abstact_dto):
    __measure_id:str = ""
    __nomenclature_id:str = ""
    __rest: float = 0

    @property
    def measure_id(self) -> str:
        return self.__measure_id

    @measure_id.setter
    def measure_id(self, value):
        self.__measure_id = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value

    @property
    def rest(self) -> float:
        return self.__rest

    @rest.setter
    def rest(self, value):
        self.__rest = value
