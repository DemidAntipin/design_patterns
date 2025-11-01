import abc
from src.core.common import common
from src.core.validator import validator, operation_exception
from datetime import datetime


"""
Абстрактный класс для наследования только dto структур
"""
class abstact_dto:
    __name:str = ""
    __id:str = ""

    @property
    def name(self) ->str:
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value   

    # Универсальный фабричный метод для загрузщки dto из словаря
    @abc.abstractmethod
    def create(self, data) -> "abstact_dto":
        validator.validate(data, dict)
        fields = common.get_fields(self)
        matching_keys = list(filter(lambda key: key in fields, data.keys()))

        try:
            for key in matching_keys:
                setattr(self, key, data[ key ])
        except:
            raise   operation_exception("Невозможно загрузить данные!")    

        return self

# Превращает сериализованные классы в dto объекты
# Поправляет название ключей и заменяет вложенные классы на их id
def object_to_dto(object):
    if isinstance(object, dict):
        result = {}
        for key in object.keys():
            if isinstance(object[key], dict):
                if "unique_code" in object[key]:
                    value = object_to_dto(object[key]["unique_code"])
                    key+="_id"
                else:
                    value=object_to_dto(object[key])
                result[key]=value
            elif key == "value" and len(object.keys())==1:
                # удаление лишнего словаря, берем только значение
                return object_to_dto(object[key])
            else:
                new_key = "id" if key == "unique_code" else key
                if object[key] is None and key != "name":
                    new_key += "_id"
                result[new_key]=object_to_dto(object[key])
        return result
    elif isinstance(object, list):
        result = []
        for item in object:
            result.append(object_to_dto(item))
        return result
    else:
        return object
            