from src.models.measure_model import measure_model
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomeclature_model
from src.models.storage_model import storage_model
from src.dtos.category_dto import category_dto
from src.dtos.measure_dto import measure_dto
from src.dtos.nomenclature_dto import nomenclature_dto
from src.dtos.storage_dto import storage_dto
from src.reposity import reposity
from src.core.validator import validator, argument_exception
from src.start_service import start_service
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from src.core.abstract_subscriber import abstract_subscriber

class reference_service(abstract_subscriber):
    __service = start_service()

    def __init__(self):
        self.__service.start()
        observe_service.add(self)

    @staticmethod
    def add(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = {"model": reference, "properties": properties}
        # Формируем событие о добавлении нового объекта  
        observe_service.create_event( event_type.add_reference(), params)

    @staticmethod
    def change(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = {"model": {"type":reference,"unique_code": properties["unique_code"]}, "properties": properties}
        # Формируем событие об изменении объекта  
        observe_service.create_event( event_type.change_reference(), params)

    @staticmethod
    def remove(reference:str, properties:dict):
        validator.validate(reference, str)
        validator.validate(properties, dict)
        params = {"model": {"type":reference,"unique_code": properties["unique_code"]}, "properties": properties}
        # Формируем событие об изменении объекта  
        observe_service.create_event( event_type.remove_reference(), params)