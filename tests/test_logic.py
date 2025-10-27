import unittest
from src.logic.response_csv import response_csv
from src.logic.response_markdown import response_markdown
from src.logic.response_json import response_json
from src.logic.response_xml import response_xml
from src.models.nomenclature_group_model import nomenclature_group_model
from src.logic.factory_entities import factory_entities
from src.core.response_format import response_format
from src.core.validator import validator, operation_exception
from src.core.abstract_response import abstract_response
from src.models.settings_model import settings_model
from src.start_service import start_service
from src.reposity import reposity
import json

# Тесты для проверки логики 
class test_logics(unittest.TestCase):

    # Проверим формирование CSV
    def test_notNone_response_csv_buld(self):
        # Подготовка
        response = response_csv()
        data = []
        entity_group = nomenclature_group_model.create("test")
        data.append( entity_group )

        # Дейстие
        result = response.create(data)

        # Проверка
        assert result is not None

    def test_formating_response_csv(self):
        # Подготовка
        response = response_csv()
        
        start = start_service()
        start.start()

        data = []
        recipe = start.data[reposity.recipe_key()][0]
        data.append(recipe)
        kg = list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.measure_key()]))[0]
        data.append(kg)
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)
        nomenclature = start.data[reposity.nomenclature_key()][0]
        data.append(nomenclature)

        # Действие
        result_recipe = response.create(data[:1])
        result_measure = response.create(data[1:2])
        result_group = response.create(data[2:3])
        result_nomenclature = response.create(data[3:4])

        # Проверка
        assert result_recipe is not None
        assert result_measure is not None
        assert result_group is not None
        assert result_nomenclature is not None

    def test_formating_response_markdown(self):
        # Подготовка
        response = response_markdown()
        
        start = start_service()
        start.start()

        data = []
        recipe = start.data[reposity.recipe_key()][0]
        data.append(recipe)
        kg = list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.measure_key()]))[0]
        data.append(kg)
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)
        nomenclature = start.data[reposity.nomenclature_key()][0]
        data.append(nomenclature)

        # Действие
        result_recipe = response.create(data[:1])
        result_measure = response.create(data[1:2])
        result_group = response.create(data[2:3])
        result_nomenclature = response.create(data[3:4])

        # Проверка
        assert result_recipe is not None
        assert result_measure is not None
        assert result_group is not None
        assert result_nomenclature is not None

    def test_formating_response_json(self):
        # Подготовка
        response = response_json()
        
        start = start_service()
        start.start()

        data = []
        recipe = start.data[reposity.recipe_key()][0]
        data.append(recipe)
        kg = list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.measure_key()]))[0]
        data.append(kg)
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)
        nomenclature = start.data[reposity.nomenclature_key()][0]
        data.append(nomenclature)

        # Действие
        result_recipe = response.create(data[:1])
        result_measure = response.create(data[1:2])
        result_group = response.create(data[2:3])
        result_nomenclature = response.create(data[3:4])

        # Проверка
        assert result_recipe is not None
        assert result_measure is not None
        assert result_group is not None
        assert result_nomenclature is not None

    def test_formating_response_xml(self):
        # Подготовка
        response = response_xml()
        
        start = start_service()
        start.start()

        data = []
        recipe = start.data[reposity.recipe_key()][0]
        data.append(recipe)
        kg = list(filter(lambda x: x.name == "Киллограмм", start.data[ reposity.measure_key()]))[0]
        data.append(kg)
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)
        nomenclature = start.data[reposity.nomenclature_key()][0]
        data.append(nomenclature)

        # Действие
        result_recipe = response.create(data[:1])
        result_measure = response.create(data[1:2])
        result_group = response.create(data[2:3])
        result_nomenclature = response.create(data[3:4])

        # Проверка
        assert result_recipe is not None
        assert result_measure is not None
        assert result_group is not None
        assert result_nomenclature is not None

    def test_notNone_factory_create(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_format.csv_format()
        factory = factory_entities(settings)
        data = []
        entity = nomenclature_group_model.create( "test" )
        data.append( entity )

        # Действие
        logic = factory.create( response_format.csv_format() )
        # Проверка
        assert logic is not None
        instance = logic()
        validator.validate( instance,  abstract_response)
        text =    instance.create(data )
        assert len(text) > 0

    def test_create_default_factory(self):
        # Подготовка
        settings = settings_model()
        settings.response_format = response_format.json_format()
        factory = factory_entities(settings)
        data = []
        entity = nomenclature_group_model.create( "test" )
        data.append( entity )

        # Действие
        logic = factory.create_default()

        # Проверка
        assert logic is not None
        instance = logic()
        text =  instance.create( data )
        assert len(text) > 0
        dict_=json.loads(text)[0]
        assert "name" in dict_.keys()
        assert "unique_code" in dict_.keys()
        assert dict_['name'] == "test"

    def test_create_response_from_array(self):
        # Подготовка
        response = response_json()
        
        start = start_service()
        start.start()

        data = []
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)
        data.append(group)

        # Действие
        result_group = response.create(data)

        # Проверка
        assert result_group is not None
        result_group = json.loads(result_group)
        assert isinstance(result_group, list)
        assert len(result_group)==2
        assert "name" in result_group[0].keys()
        assert "unique_code" in result_group[0].keys()

    def test_create_response_from_array_of_different_models(self):
        # Подготовка
        response = response_csv()
        
        start = start_service()
        start.start()

        data = []
        nomenclature = start.data[reposity.nomenclature_key()][0]
        data.append(nomenclature)
        group = start.data[reposity.nomenclature_group_key()][0]
        data.append(group)

        # Проверки
        with self.assertRaises(operation_exception):
            response.create(data)