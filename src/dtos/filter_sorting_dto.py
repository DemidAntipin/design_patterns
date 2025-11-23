from src.dtos.filter_dto import filter_dto
from src.core.validator import validator
from datetime import datetime
from src.core.filter_format import filter_format
from src.models.nomenclature_model import nomeclature_model
from src.models.storage_model import storage_model

class filter_sorting_dto:
    """
    DTO для передачи параметров фильтрации и сортировки
    Используется в методах фильтрации prototype
    """

    __filters = []
    __sorting = []

    def __init__(self, filters, sorting):
        validator.validate(filters, list)
        validator.validate(sorting, list)
        self.__filters = filters
        self.__sorting = sorting

    @property
    def filters(self) -> list:
        return self.__filters

    @property
    def sorting(self) -> list:
        return self.__sorting
    
    @staticmethod
    def create_by_before_date(date: datetime):
        validator.validate(date, datetime)
        return filter_sorting_dto([{
            "field_name": "date",
            "value": date,
            "format": filter_format.less()
        }], [])
    
    @staticmethod
    def create_by_period_date(start_date: datetime, end_date: datetime):
        validator.validate(start_date, datetime)
        validator.validate(end_date, datetime)
        return filter_sorting_dto([{
            "field_name": "date",
            "value": start_date,
            "format": filter_format.not_less()
        },
        {
            "field_name": "date",
            "value": end_date,
            "format": filter_format.not_greater()
        }], [])
    

    @staticmethod
    def create_by_nomenclature(nomenclature:nomeclature_model):
        validator.validate(nomenclature, nomeclature_model)
        return filter_sorting_dto([{
            "field_name": "nomenclature",
                "value": nomenclature,
                "format": filter_format.equals()
        }], [])
    
    @staticmethod
    def create_by_storage(storage_id:str):
        validator.validate(storage_id, str)
        return filter_sorting_dto([{
            "field_name": "storage",
                "value": storage_id,
                "format": filter_format.like()
        }], [])