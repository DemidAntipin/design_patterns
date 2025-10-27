from src.core.validator import validator
from src.core.abstract_converter import abstract_coverter

# Конвертер для обработки словарей
class dict_converter(abstract_coverter):

    # Формируется словарь в виде "ключ поля": converter.convert(значение поля), где тип converter умеет обрабатывать тип поля.
    def convert(self, obj: dict) -> dict:
        from src.logic.factory_converters import factory_converters
        validator.validate(obj, dict)
        factory = factory_converters()
        result = {}
        for key in obj.keys():
            value = obj[key]
            if isinstance(value, dict):
                result[key] = self.convert(value)
            else:
                result[key] = factory.create(value).convert(value)
        return result