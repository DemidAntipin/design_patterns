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
    def convert(self, obj) -> dict:
        validator.validate(obj, datetime)        
        return obj.strftime(datetime_converter.format)