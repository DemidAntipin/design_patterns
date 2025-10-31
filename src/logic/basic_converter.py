from src.core.abstract_converter import abstract_coverter
from src.core.validator import validator
from types import NoneType
"""
Базовый конвертер для преобразования простых типов данных (int, str, bool, None)
"""
class basic_converter(abstract_coverter):

    """Простые типы не изменяются при сериализации"""
    # field - наименование поля (передается из reference_converter -> factory_converter -> basic_converter)
    def convert(self, obj, field: str = "value") -> dict:
        validator.validate(obj, (int, float, str, bool, NoneType))
        return {field : obj}