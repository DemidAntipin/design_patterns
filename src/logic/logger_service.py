from src.core.abstract_subscriber import abstract_subscriber
from src.core.validator import validator
from src.settings_manager import settings_manager
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.log_level import log_level as level
from src.core.log_mode import log_mode as mode
from datetime import datetime
import pathlib
from src.dtos.logger_dto import logger_dto
from src.core.log_level import log_level

class logger_service(abstract_subscriber):

    __settings: settings_manager = None
    __log_level: level = None
    __log_mode: mode = None
    __log_dir: str = None
    __log_format: str = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(logger_service, cls).__new__(cls)        
            observe_service.add(cls.instance)
        return cls.instance

    def __init__(self):
        self.__settings = settings_manager()
        self.instance.log_level = self.__settings.settings.logging_level
        self.instance.log_mode = self.__settings.settings.logging_mode
        self.instance.log_dir = self.__settings.settings.logging_dir
        self.instance.log_format = self.__settings.settings.logging_format
        if self.log_dir:
            log_path = pathlib.Path(self.log_dir).absolute()
            log_path.mkdir(parents=True, exist_ok=True)    
        self.__settings.logger = self

    @property
    def log_level(self):
        return self.__log_level
    
    @log_level.setter
    def log_level(self, value):
        validator.validate(value, level)
        self.__log_level = value
    
    @property
    def log_mode(self):
        return self.__log_mode
    
    @log_mode.setter
    def log_mode(self, value):
        validator.validate(value, mode)
        self.__log_mode = value
    
    @property
    def log_dir(self):
        return self.__log_dir
    
    @log_dir.setter
    def log_dir(self, value):
        validator.validate(value, str)
        self.__log_dir = value

    @property
    def log_format(self):
        return self.__log_format
    
    @log_format.setter
    def log_format(self, value):
        validator.validate(value, str)
        self.__log_format = value
    
    # Получить актуальное имя файла логов
    def _get_log_filename(self) -> str:
        dt_str = datetime.now().strftime(self.__settings.settings.datetime_format)
        return f"log_{dt_str}.log"

    # Логирование в файл
    def log_to_file(self, log_message:str):
        validator.validate(log_message, str)
        dir_path = pathlib.Path(self.log_dir)
        file_path = pathlib.Path.absolute(dir_path / self._get_log_filename())
        file_path.touch(exist_ok=True)
        with open(file_path, "a", encoding="UTF-8") as file:
            file.write(log_message + "\n")

    # Логирование в консоль
    def log_to_console(self, log_message:str):
        validator.validate(log_message, str)
        print(log_message)

    """
    Обработка событий
    """
    def handle(self, event:str, params:logger_dto):
        super().handle(event, params)

        if event == event_type.log():
            validator.validate(params, logger_dto)
            log_level = params.level
            if log_level >= self.log_level:
                log_message = self.log_format.format(
                    timestamp=datetime.now().strftime("%H:%M:%S"), 
                    level=params.level.name, 
                    source=params.source, 
                    message=params.message)
                if self.log_mode == mode.FILE or self.log_mode == mode.BOTH:
                    self.log_to_file(log_message)
                if self.log_mode == mode.CONSOLE or self.log_mode == mode.BOTH:
                    self.log_to_console(log_message)
             