import unittest
from src.core.validator import validator, argument_exception
import datetime
from src.logic.factory_converters import factory_converters
from src.start_service import start_service
from src.reposity import reposity
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter

class test_converter_factory(unittest.TestCase):
    
    def test_create_factory_converter(self):
        # Подготовка
        factory = factory_converters()

        service = start_service()
        service.start()

        group = service.data[reposity.nomenclature_group_key()][0]
        
        values = [1, datetime.datetime.now(), group]
        excepted_results = [
            basic_converter().convert(1),
            datetime_converter().convert(datetime.datetime.now()), 
            reference_converter().convert(group, "value")]
    
        # Действие

        # Проверки
        for i, v in enumerate(values):
            assert factory.convert(v) == excepted_results[i]

    def test_convert_undefined_type_factory_converter(self):
        # Подготовка
        class SomeClass:
            pass
        factory = factory_converters()

        # Действие

        # Проверки
        with self.assertRaises(argument_exception):
            factory.convert(SomeClass())

    def test_convert_array_factory_converter(self):
        # Подготовка
        factory = factory_converters()

        service = start_service()
        service.start()

        group = service.data[reposity.nomenclature_group_key()][0]

        values = [[1, 5, 9], datetime.datetime.now(), group]
        excepted_result = {"value":
                           [
                            {"value": 
                                [
                                    {"value":1}, 
                                    {"value":5}, 
                                    {"value":9}
                                ]
                            }, 
                                datetime_converter().convert(datetime.datetime.now()), 
                                reference_converter().convert(group)
                            ]
                        }

        # Действие
        result = factory.convert(values)

        # Проверки
        assert result == excepted_result

    def test_convert_dict_factory_converter(self):
        # Подготовка
        factory = factory_converters()

        service = start_service()
        service.start()
        time = datetime.datetime.now()

        group = service.data[reposity.nomenclature_group_key()][0]

        values = {"numbers": [1, 2, 3], "datetime": datetime.datetime.now(), "group": group}
        excepted_result = {
            "numbers": [
                {"value":1}, 
                {"value":2}, 
                {"value":3}
            ], 
            "datetime": datetime_converter().convert(datetime.datetime.now(), "value")["value"], 
            "group": reference_converter().convert(group)}

        # Действие
        result = factory.convert(values)

        # Проверки
        assert result == excepted_result  