from src.dtos.filter_dto import filter_dto
from src.core.validator import validator

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

    def __init__(self, filters, sorting):
        validator.validate(filters, list)
        validator.validate(sorting, list)
        self.__filters = filters
        self.__sorting = sorting