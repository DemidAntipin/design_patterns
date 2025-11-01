from src.core.validator import validator
from src.core.entity_model import entity_model
from src.core.abstract_dto import abstact_dto

######################################
# Модель склада
class storage_model(entity_model):
    
    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:abstact_dto, cache:dict):
        item  = storage_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item