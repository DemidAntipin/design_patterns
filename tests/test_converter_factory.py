import unittest
from src.core.validator import validator, argument_exception
import datetime
from src.logic.factory_converters import factory_converters
from src.start_service import start_service
from src.reposity import reposity
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter
from src.logic.list_converter import list_converter
from src.logic.dict_converter import dict_converter

class test_converter_factory(unittest.TestCase):
    
    def test_create_factory_converter(self):
        # Подготовка
        factory = factory_converters()

        service = start_service()
        service.start()

        group = service.data[reposity.nomenclature_group_key()][0]
        
        values = [1, datetime.datetime.now(), group, [1,2,3], {"name":"name", "code":245}]
        excepted_types = [basic_converter, datetime_converter, reference_converter, list_converter, dict_converter]
    
        # Действие

        # Проверки
        for i, v in enumerate(values):
            assert isinstance(factory.create(v), excepted_types[i])

    def test_convert_undefined_type_factory_converter(self):
        # Подготовка
        class SomeClass:
            pass
        factory = factory_converters()

        # Действие

        # Проверки
        with self.assertRaises(argument_exception):
            factory.create(SomeClass())
    