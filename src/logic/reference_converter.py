from src.core.validator import validator
from src.core.abstract_reference import abstact_reference
from src.core.abstract_converter import abstract_coverter
from src.core.common import common

# Конвертер для обработки классов, наследуемых от abstract_reference
class reference_converter(abstract_coverter):

    # Формируется словарь в виде "поле класса": converter.convert(значение поля), где тип converter умеет обрабатывать тип поля.
    # field не участвует в данном конвертере, но нужен в других конвертерах, что реализуют тот же метод абстрактного класса
    def convert(self, obj: abstact_reference, field: str = None) -> dict:
        from src.logic.factory_converters import factory_converters
        validator.validate(obj, abstact_reference)
        factory = factory_converters()
        result = {}
        properties = common.get_fields(obj)
        for property in properties:
            value = getattr(obj, property)
            if isinstance(value, abstact_reference):
                # Значение сложного типа
                # сериализация вернет словарь с множеством ключей
                # добавляем словарь внутрь result
                result[property] = self.convert(value)
            else:
                # Значение примитивного типа или datetime 
                # сериализация вернет словарь с 1 property и значением value 
                # объединяем словарь с result
                result.update(factory.convert(value, property))
        return result