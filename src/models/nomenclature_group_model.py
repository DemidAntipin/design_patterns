from src.core.abstract_reference import abstact_reference

######################################
# Модель группы номенклатуры
class nomenclature_group_model(abstact_reference):

    @staticmethod
    def create():
        item = nomenclature_group_model()
        return item