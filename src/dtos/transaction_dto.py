from src.core.abstract_dto import abstact_dto
import datetime

# Модель транзакции (dto)
# Пример
#                "date":"2024-01-15",
#                "storage_id":"adb7510f-687d-428f-a697-26e53d3f65b7",
#                "nomenclature_id":"cde8512g-789e-539g-b798-36f64e4f76c8", 
#                "measure_id":"fgh9513h-891f-641h-c899-47g75f5g87d9",
#                "value":100
class transaction_dto(abstact_dto):
    __date: datetime = None
    __storage_id: str = None
    __nomenclature_id: str = None
    __measure_id: str = None
    __value: int = 0

    @property
    def date(self) -> datetime:
        return self.__date
    
    @date.setter
    def date(self, value):
        self.__date = datetime.datetime.strptime(value, "%Y-%m-%d")

    @property
    def storage_id(self) -> str:
        return self.__storage_id
    
    @storage_id.setter
    def storage_id(self, value):
        self.__storage_id = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id
    
    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value

    @property
    def measure_id(self) -> str:
        return self.__measure_id
    
    @measure_id.setter
    def measure_id(self, value):
        self.__measure_id = value

    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value