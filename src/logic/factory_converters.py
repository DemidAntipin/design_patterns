from datetime import datetime
from src.core.abstract_reference import abstact_reference
from src.core.abstract_converter import abstract_coverter
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter
from src.logic.list_converter import list_converter
from src.logic.dict_converter import dict_converter
from src.core.validator import argument_exception

"""Класс-фабрика для конвертации любых объектов и списков в JSON-формат"""
class factory_converters:
    def create(self, obj) -> abstract_coverter:
        if isinstance(obj, (int, float, bool, str)) or obj is None:
            return basic_converter()
        elif isinstance(obj, datetime):
            return datetime_converter()
        elif isinstance(obj, abstact_reference):
            return reference_converter()
        elif isinstance(obj, (list, tuple)):
            return list_converter()
        elif isinstance(obj, dict):
            return dict_converter()
        else:
            raise argument_exception(f"The method to serialize {type(obj)} is't defined.")
        
    def convert(self, obj):
        return self.create(obj).convert(obj)