from src.core.abstract_response import abstract_response
from src.logic.response_csv import response_csv
from src.logic.response_markdown import response_markdown
from src.logic.response_xml import response_xml
from src.logic.response_json import response_json
from src.core.validator import validator, operation_exception
from src.models.settings_model import settings_model

class factory_entities:
    __match = {
        "csv":  response_csv,
        "markdown": response_markdown,
        "xml" : response_xml,
        "json" : response_json
    }
    __settings: settings_model = None

    def __init__(self, settings: settings_model):
        validator.validate(settings, settings_model)
        self.__settings = settings

    # Получить нужный тип
    def create(self, format:str) -> abstract_response:
        if callable(format):
            format = format()
            
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")
        
        return self.__match[  format ]
    
    # Получить тип ответа по умолчанию
    def create_default(self) -> abstract_response:
        return self.create(self.__settings.response_format)