import unittest
from src.logic.response_csv import response_csv
from src.models.nomenclature_group_model import nomenclature_group_model
from src.logic.factory_entities import factory_entities
from src.core.response_format import response_format
from src.core.validator import validator
from src.core.abstract_response import abstract_response

# Тесты для проверки логики 
class test_logics(unittest.TestCase):

    # Проверим формирование CSV
    def test_notNone_response_csv_buld(self):
        # Подготовка
        response = response_csv()
        data = []
        entity = nomenclature_group_model.create("test")
        data.append( entity )

        # Дейстие
        result = response.create( "csv", data)

        # Проверка
        assert result is not None


    def test_notNone_factory_create(self):
        # Подготовка
        factory = factory_entities()
        data = []
        entity = nomenclature_group_model.create( "test" )
        data.append( entity )

        # Действие
        logic = factory.create( response_format.csv() )

        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate( instance,  abstract_response)
        text =    instance.create(  response_format.csv() , data )
        assert len(text) > 0 



        
  
if __name__ == '__main__':
    unittest.main()   