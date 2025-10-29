from src.core.abstract_reference import abstact_reference
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter
from src.core.validator import argument_exception
from types import NoneType
from datetime import datetime

class factory_converters:
    __match = {
        int:  basic_converter(),
        float: basic_converter(),
        bool: basic_converter(),
        str: basic_converter(),
        NoneType: basic_converter(),
        datetime: datetime_converter(),
        abstact_reference: reference_converter()
    }

    # Использовать нужный конвертер
    def convert(self, obj):
        if isinstance(obj, (list, tuple)):
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
        for key in tuple(self.__match.keys()):
            if isinstance(obj, key):
                return self.__match[key].convert(obj)
        raise argument_exception(f"The converter that able to serialize {type(obj)} is't defined.")