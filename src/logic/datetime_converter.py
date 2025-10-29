from src.core.abstract_converter import abstract_coverter
from src.core.validator import validator
from datetime import datetime

"""
Конвертер для дат и времени
"""
class datetime_converter(abstract_coverter):
    # Формат даты
    format = "%Y-%m-%d %H:%M:%S"

    # Дата преобразуется в строку согласно указанному формату
    # field - наименование поля (передается из reference_converter -> factory_converter -> basic_converter)
    def convert(self, obj, field: str = "value") -> dict:
        validator.validate(obj, datetime)        
        return {field : obj.strftime(datetime_converter.format)}