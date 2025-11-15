from src.core.abstract_dto import abstact_dto

# Фильтрация
class filter_dto(abstact_dto):
    __field_name:str = ""
    __value:str = ""
    __format:str = ""


    @property
    def field_name(self) -> str:
        return self.__field_name
    
    @field_name.setter
    def field_name(self, value:str):
        self.__field_name = value

    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value:str):
        self.__value = value

    @property
    def format(self) -> str:
        return self.__format
    
    @format.setter
    def format(self, value: str):
        self.__format = value