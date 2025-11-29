from src.dtos.transaction_dto import transaction_dto
from src.core.abstract_reference import abstact_reference
from src.core.validator import validator
from src.models.storage_model import storage_model
from src.models.nomenclature_model import nomeclature_model
from src.models.measure_model import measure_model
from datetime import datetime

# Модель единиц измерения для моделей номенклатуры
class transaction_model(abstact_reference):
    # Дата транзакции
    __date : datetime = None
    # Склад транзакции
    __storage : storage_model = None
    # Номенклатура транзакции
    __nomenclature: nomeclature_model = None
    # Ед измерения транзакции
    __measure: measure_model = None
    # Количество
    __value : int = None

    # Дата транзакции
    @property
    def date(self) -> datetime:
        return self.__date
    
    @date.setter
    def date(self, value: datetime):
        validator.validate(value, datetime)
        self.__date = value

    # Склад транзакции
    @property
    def storage(self) -> storage_model:
        return self.__storage
    
    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value

    # Номенклатура транзакции
    @property
    def nomenclature(self) -> nomeclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value: nomeclature_model):
        validator.validate(value, nomeclature_model)
        self.__nomenclature = value

    # Ед. измерения транзакции
    @property
    def measure(self) -> measure_model:
        return self.__measure
    
    @measure.setter
    def measure(self, value: measure_model):
        validator.validate(value, measure_model)
        self.__measure = value

    # Количество self.nomenclature транзакции в ед. измерения self.measure
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        self.__value = value

    # Универсальный фабричный метод
    @staticmethod
    def create(date: datetime, storage: storage_model, nomenclature: nomeclature_model, measure: measure_model, value: int):
        validator.validate(date, datetime)
        validator.validate(storage, storage_model)
        validator.validate(nomenclature, nomeclature_model)
        validator.validate(measure, measure_model)
        validator.validate(value, int)
        
        item = transaction_model()
        item.date = date
        item.value = value
        item.measure = measure
        item.nomenclature = nomenclature
        item.storage = storage
        return item
    
    """Фабричный метод для создания из DTO"""
    @staticmethod
    def from_dto(dto: transaction_dto, cache: dict):
        validator.validate(dto, transaction_dto)
        validator.validate(cache, dict)
        
        # Получаем связанные объекты из кэша
        storage = cache[dto.storage_id] if dto.storage_id in cache else None
        nomenclature = cache[dto.nomenclature_id] if dto.nomenclature_id in cache else None
        measure = cache[dto.measure_id] if dto.measure_id in cache else None
        
        item = transaction_model.create(date=dto.date, storage=storage, nomenclature=nomenclature, measure=measure, value=dto.value)
        return item