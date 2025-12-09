from src.core.abstract_dto import abstact_dto
from src.core.validator import validator
from src.core.log_level import log_level

class logger_dto(abstact_dto):
    __level: log_level = None
    __source: str = None
    __message: str = None

    @property
    def level(self) -> log_level:
        return self.__level
    
    @level.setter
    def level(self, value):
        validator.validate(value, str)
        if value in log_level.levels():
            self.__level = log_level[value]

    @property
    def source(self) -> str:
        return self.__source
    
    @source.setter
    def source(self, value):
        validator.validate(value, str)
        self.__source = value

    @property
    def message(self) -> str:
        return self.__message
    
    @message.setter
    def message(self, value):
        validator.validate(value, str)
        self.__message = value

    @staticmethod
    def create_info(source:str, message:str):
        validator.validate(source, str)
        validator.validate(message, str)
        return logger_dto().create({
            "level": "INFO",
            "source": source,
            "message": message
        })
    
    @staticmethod
    def create_debug(source:str, message:str):
        validator.validate(source, str)
        validator.validate(message, str)
        return logger_dto().create({
            "level": "DEBUG",
            "source": source,
            "message": message
        })
    
    @staticmethod
    def create_error(source:str, message:str):
        validator.validate(source, str)
        validator.validate(message, str)
        return logger_dto().create({
            "level": "ERROR",
            "source": source,
            "message": message
        })