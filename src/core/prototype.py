from src.core.validator import validator, argument_exception
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.dtos.filter_dto import filter_dto
from src.core.common import common
from src.core.filter_format import filter_format
from src.core.abstract_reference import abstact_reference
from datetime import datetime, date

class prototype:
    __data = []    

    @classmethod
    def __match(cls):
        return {
            "types":{
                abstact_reference: cls.compare_objects,
                str: cls.compare_str,
                datetime: cls.compare_datetime,
                int: cls.compare_numbers,
                float: cls.compare_numbers
            },
            "operations":{
                filter_format.equals() : lambda a, b: a == b,
                filter_format.like(): lambda a, b: str(a) in b,
                filter_format.less(): lambda a, b: a < b,
                filter_format.greater(): lambda a, b: a > b,
                filter_format.not_less(): lambda a, b: a >= b,
                filter_format.not_greater(): lambda a, b: a <= b
            }
        }

    # Набор данных
    @property
    def data(self):
        return self.__data

    def __init__(self, data:list):
        validator.validate(data, list)
        self.__data = data
        
    # Клонирование        
    def clone(self, data:list = None)-> "prototype":
        inner_data = None
        if data is None:
            inner_data = self.__data
        else:
            inner_data = data

        instance =  prototype(inner_data)
        return instance   
    
    # Универсальный фильтр
    @staticmethod
    def filter(source: "prototype", filter) -> "prototype":
        data = source.data
        if len(data) == 0:
            return source.clone(data)

        if isinstance(filter, filter_dto):
            result=[]
            validator.validate(filter.format, str)
            for field in common.get_fields(data[0]):
                for item in data:
                    if field == filter.field_name:
                        value = getattr(item, field)
                        if prototype.compare(value, filter.value, filter.format):
                            result.append(item)
        elif isinstance(filter, filter_sorting_dto):
            for filt in filter.filters:
                dto = filter_dto()
                dto.field_name = filt["field_name"]
                dto.value = filt["value"]
                dto.format = filt["format"]
                source = prototype.filter(source, dto)
            result = source.data
            # сортировка с учётом приоритетов (порядка правила в списке)
            for field in filter.sorting[::-1]:
                result.sort(key=lambda item: getattr(item, field) if hasattr(item, field) else float('inf'))
        return source.clone(result)
    
    @staticmethod
    def compare(value, filter_value:str, format:str) -> bool:
        for key in prototype.__match()["types"].keys():
            if isinstance(value, key):
                return prototype.__match()["types"][key](value, filter_value, format)
    
    @staticmethod
    def compare_datetime(value:datetime, filter_value, format:filter_format) -> bool:
        validator.validate(value, datetime)
        available_formats=[filter_format.equals(), filter_format.greater(), filter_format.less(), filter_format.not_greater(), filter_format.not_less()]
        if format not in available_formats:
            raise argument_exception(f"Неподдерживаемый формат сравнения для дат. Доступные форматы {available_formats}, получен {format}.")
        if not isinstance(filter_value, date):
            filter_value = datetime.strptime(filter_value, "%Y-%m-%d")
        return prototype.__match()["operations"][format](value, filter_value)
    
    @staticmethod
    def compare_str(value:str, filter_value:str, format:filter_format) -> bool:
        validator.validate(value, str)
        available_formats=[filter_format.equals(), filter_format.like()]
        if format not in available_formats:
            raise argument_exception(f"Неподдерживаемый формат сравнения для строк. Доступные форматы {available_formats}, получен {format}.")
        return prototype.__match()["operations"][format](filter_value, value)
    
    @staticmethod
    def compare_objects(value, filter_value:abstact_reference, format:filter_format) -> bool:
        validator.validate(value, abstact_reference)
        available_formats=[filter_format.equals(), filter_format.like()]
        if format not in available_formats:
            raise argument_exception(f"Неподдерживаемый формат сравнения для объектов. Доступные форматы {available_formats}, получен {format}.")
        if format == filter_format.like():
            value = common.get_values(source=value, recurse=True)
        return prototype.__match()["operations"][format](filter_value, value)
    
    @staticmethod
    def compare_numbers(value, filter_value:str, format:filter_format) -> bool:
        validator.validate(value, (int, float))
        available_formats=[filter_format.equals(), filter_format.greater(), filter_format.less(), filter_format.not_greater(), filter_format.not_less()]
        if format not in available_formats:
            raise argument_exception(f"Неподдерживаемый формат сравнения для чисел. Доступные форматы {available_formats}, получен {format}.")
        filter_value = float(filter_value)
        return prototype.__match()["operations"][format](value, filter_value)
            
