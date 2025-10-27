from src.core.abstract_converter import abstract_coverter
from src.core.validator import validator
"""
Базовый конвертер для преобразования простых типов данных (int, str, bool, None)
"""
class basic_converter(abstract_coverter):

    """Простые типы не изменяются при сериализации"""
    def convert(self, obj) -> dict:
        validator.validate(obj, (int, float, str, bool), allow_null=True)
        return obj