from src.core.entity_model import entity_model
from src.core.abstract_dto import abstact_dto

######################################
# Модель группы номенклатуры
class nomenclature_group_model(entity_model):

    """
    Фабричный метод из Dto
    """
    @staticmethod
    def from_dto(dto:abstact_dto, cache:dict):
        item  = nomenclature_group_model()
        item.name = dto.name
        item.unique_code = dto.id
        return item