from src.core.abstract_response import abstract_response
from src.logic.response_csv import response_csv
from src.core.validator import operation_exception

class factory_entities:
    __match = {
        "csv":  response_csv
    }


    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if callable(format):
            format = format()
            
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[  format ]