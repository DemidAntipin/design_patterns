import unittest
from src.logic.basic_converter import basic_converter
from src.logic.datetime_converter import datetime_converter
from src.logic.reference_converter import reference_converter
from src.start_service import start_service
from src.reposity import reposity
from src.core.validator import validator, argument_exception
import datetime

class test_converters(unittest.TestCase):

    def test_convert_valid_types_basic_converter(self):
        # Подготовка
        converter = basic_converter()
        values = [1, "2", "three", True, 4.5, None]

        # Действие

        # Проверки
        for v in values:
            assert {"value" :v} == converter.convert(v)

    def test_convert_invalid_types_basic_converter(self):
        # Подготовка
        converter = basic_converter()
        
        service = start_service()
        service.start()

        measure = service.data[reposity.measure_key()][0]
        nomenclature = service.data[reposity.nomenclature_key()][0]
        group = service.data[reposity.nomenclature_group_key()][0]
        recipe = service.data[reposity.recipe_key()][0]

        # Действие

        # Проверки
        with self.assertRaises(argument_exception):
            converter.convert([0,1,2])
        with self.assertRaises(argument_exception):
            converter.convert((0,1,2))
        with self.assertRaises(argument_exception):
            converter.convert({"field":"value"})
        with self.assertRaises(argument_exception):
            converter.convert(datetime.time())
        with self.assertRaises(argument_exception):
            converter.convert(measure)
        with self.assertRaises(argument_exception):
            converter.convert(nomenclature)
        with self.assertRaises(argument_exception):
            converter.convert(group)
        with self.assertRaises(argument_exception):
            converter.convert(recipe)

    def test_convert_valid_types_datetime_converter(self):
        # Подготовка
        converter = datetime_converter()
        value = datetime.datetime.now()
        format = "%Y-%m-%d"

        # Действие
        result = converter.convert(value)

        # Проверки
        assert result == {"value" :value.strftime(format)}

    def test_convert_invalid_types_datetime_converter(self):
        # Подготовка
        converter = datetime_converter()
        
        service = start_service()
        service.start()

        measure = service.data[reposity.measure_key()][0]
        nomenclature = service.data[reposity.nomenclature_key()][0]
        group = service.data[reposity.nomenclature_group_key()][0]
        recipe = service.data[reposity.recipe_key()][0]
        invalid_values = [1, "2", "three", True, 4.5, None]

        # Действие

        # Проверки
        for value in invalid_values:
            with self.assertRaises(argument_exception):
                converter.convert(value)
        with self.assertRaises(argument_exception):
            converter.convert([datetime.datetime.now(), datetime.datetime.now()])
        with self.assertRaises(argument_exception):
            converter.convert((datetime.datetime.now(), datetime.datetime.now()))
        with self.assertRaises(argument_exception):
            converter.convert({"field":"value"})
        with self.assertRaises(argument_exception):
            converter.convert(measure)
        with self.assertRaises(argument_exception):
            converter.convert(nomenclature)
        with self.assertRaises(argument_exception):
            converter.convert(group)
        with self.assertRaises(argument_exception):
            converter.convert(recipe)

    def test_convert_valid_types_reference_converter(self):
        # Подготовка
        converter = reference_converter()
        
        service = start_service()
        service.start()

        measure = service.data[reposity.measure_key()][0]
        nomenclature = service.data[reposity.nomenclature_key()][0]
        group = service.data[reposity.nomenclature_group_key()][0]
        
        expected_measure = {
            "name": measure.name, 
            "base_unit": measure.base_unit, 
            "coef": measure.coef, 
            "unique_code": measure.unique_code
            }
        expected_group = {
            "name": group.name, 
            "unique_code": group.unique_code
            }
        expected_nomenclature = {
            "name": nomenclature.name, 
            "category":expected_group, 
            "measure":expected_measure, 
            "unique_code":nomenclature.unique_code
            }

        # Действие
        result_measure = converter.convert(measure)
        result_group = converter.convert(group)
        result_nomenclature = converter.convert(nomenclature)

        # Проверки
        assert result_measure == expected_measure
        assert result_group == expected_group
        assert result_nomenclature == expected_nomenclature

    def test_convert_invalid_types_reference_converter(self):
        # Подготовка
        converter = reference_converter()

        invalid_values = [1, "2", "three", True, 4.5, None, datetime.datetime.now().date()]

        # Действие

        # Проверки
        for value in invalid_values:
            with self.assertRaises(argument_exception):
                converter.convert(value)

if __name__ == "__main__":
    unittest.main()