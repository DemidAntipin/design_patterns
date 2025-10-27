from src.core.validator import validator
from src.core.abstract_reference import abstact_reference
from src.core.abstract_converter import abstract_coverter
from src.core.common import common

# Конвертер для обработки классов, наследуемых от abstract_reference
class reference_converter(abstract_coverter):

    # Формируется словарь в виде "поле класса": converter.convert(значение поля), где тип converter умеет обрабатывать тип поля.
    def convert(self, obj: abstact_reference) -> dict:
        from src.logic.factory_converters import factory_converters
        validator.validate(obj, abstact_reference)
        factory = factory_converters()
        result = {}
        properties = common.get_fields(obj)
        for property in properties:
            value = getattr(obj, property)
            if isinstance(value, abstact_reference):
                result[property] = self.convert(value)
            else:
                result[property] = factory.create(value).convert(value)
        return result