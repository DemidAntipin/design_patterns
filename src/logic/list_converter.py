from src.core.validator import validator
from src.core.abstract_converter import abstract_coverter

# Конвертер для обработки массивов и кортежей
class list_converter(abstract_coverter):

    # Формируется массив из элементов converter.convert(значение элемента массива obj), где тип converter умеет обрабатывать тип элемента.
    def convert(self, obj) -> dict:
        from src.logic.factory_converters import factory_converters
        validator.validate(obj, (list, tuple))
        value_type = type(obj[0])
        factory = factory_converters()
        result = []
        for value in obj:
            # Проверка что все элементы одного типа
            validator.validate(value, value_type)
            if isinstance(value, (list, tuple)):
                result.append(self.convert(value))
            else:
                result.append(factory.create(value).convert(value))
        return result