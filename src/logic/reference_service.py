from src.core.validator import validator
from src.start_service import start_service
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.abstract_subscriber import abstract_subscriber
from src.dtos.reference_dto import reference_dto
from src.dtos.logger_dto import logger_dto

class reference_service(abstract_subscriber):
    __service = start_service()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(reference_service, cls).__new__(cls)
            observe_service.add(cls.instance)
        return cls.instance

    def __init__(self):
        self.__service.start()

    @staticmethod
    def add(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = reference_dto().create({"name": reference, "model_dto_dict":properties})
        # Формируем событие о добавлении нового объекта  
        observe_service.create_event( event_type.add_reference(), params)

        # Логгирование
        log_message = f"В репозиторий добавлен новый объект {reference} c dto {properties}."
        log_dto = logger_dto().create_info("CRUD", log_message)
        observe_service.create_event(event_type.log(), log_dto)

    @staticmethod
    def change(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = reference_dto().create({"name":reference, "id": properties["unique_code"], "model_dto_dict": properties})
        # Формируем событие об изменении объекта  
        observe_service.create_event( event_type.change_reference(), params)

        # Логгирование
        log_message = f"Изменен объект {reference} c id {properties['unique_code']} и dto {properties}."
        log_dto = logger_dto().create_info("CRUD", log_message)
        observe_service.create_event(event_type.log(), log_dto)

    @staticmethod
    def remove(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = reference_dto().create({"name":reference, "id": properties["unique_code"], "model_dto_dict": properties})
        # Формируем событие об изменении объекта  
        observe_service.create_event( event_type.remove_reference(), params)

        # Логгирование
        log_message = f"Удален объект {reference} c id {properties['unique_code']}."
        log_dto = logger_dto().create_info("CRUD", log_message)
        observe_service.create_event(event_type.log(), log_dto)