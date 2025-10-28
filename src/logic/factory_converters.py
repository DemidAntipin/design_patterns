from src.core.abstract_reference import abstact_reference
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter
from src.core.validator import argument_exception
from src.core.converter_format import converter_format
from types import NoneType
from datetime import datetime

class factory_converters:
    __match = {
        converter_format.basic_format():  basic_converter,
        converter_format.datetime_format(): datetime_converter,
        converter_format.reference_format(): reference_converter
    }

    # Использовать нужный конвертер
    def convert(self, obj):
        if isinstance(obj, (int, float, bool, str)) or isinstance(obj, NoneType):
            return self.__match[converter_format.basic_format()]().convert(obj)
        elif isinstance(obj, datetime):
            return self.__match[converter_format.datetime_format()]().convert(obj)
        elif isinstance(obj, abstact_reference):
            return self.__match[converter_format.reference_format()]().convert(obj)
        elif isinstance(obj, (list, tuple)):
            result = []
            for value in obj:
                result.append(self.convert(value))
            return result
        elif isinstance(obj, dict):
            result = {}
            for key in obj.keys():
                value = obj[key]
                result[key] = self.convert(value)
            return result
        else:
            raise argument_exception(f"The converter that able to serialize {type(obj)} is't defined.")