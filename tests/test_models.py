from src.models.company_model import company_model
from src.settings_manager import settings_manager
from src.models.storage_model import storage_model
from src.core.validator import argument_exception, operation_exception
import uuid
import unittest

class test_models(unittest.TestCase):
    # проверить создание основной модели
    # данные должны быть пустые
    def test_create_empty_company(self):
        # подготовка
        model = company_model()
        # действие

        # проверки
        assert model.name == ""
        assert model.inn == 0
        assert model.account == 0
        assert model.corr_account == 0
        assert model.bic == 0
        assert model.ownership == ""

    # проверить создание основной модели
    # данные неверного типа
    def test_invalid_types_company_model(self):
        # подготовка
        model = company_model()

        # действие

        # проверки
        with self.assertRaises(argument_exception):
            model.name = dict()
        with self.assertRaises(argument_exception):
            model.inn = dict()
        with self.assertRaises(argument_exception):
            model.account = dict()
        with self.assertRaises(argument_exception):
            model.corr_account = dict()
        with self.assertRaises(argument_exception):
            model.bic = dict()
        with self.assertRaises(argument_exception):
            model.ownership = dict()

    # проверить создание основной модели
    # данные содержат ошибки 
    def test_invalid_data_company_model(self):
        # подготовка
        model = company_model()
        
        # действие

        # проверки
        with self.assertRaises(argument_exception):
            model.name = "  "
        with self.assertRaises(argument_exception):
            model.inn = 123
        with self.assertRaises(argument_exception):
            model.account = 123
        with self.assertRaises(argument_exception):
            model.corr_account = 123
        with self.assertRaises(argument_exception):
            model.bic = 123
        with self.assertRaises(argument_exception):
            model.ownership = "OOOAAAOOO"
        


    # проверить создание основной модели
    # данные должны быть не пустые
    def test_create_not_empty_company_model(self):
        # подготовка
        model = company_model()

        # действие
        model.name = "test"
        model.inn = 123456789012
        model.account = 12345678901
        model.corr_account = 12345678901
        model.bic = 123456789
        model.ownership = "OOOOO"

        # проверки
        assert model.name == "test"
        assert model.inn == 123456789012
        assert model.account == 12345678901
        assert model.corr_account == 12345678901
        assert model.bic == 123456789
        assert model.ownership == "OOOOO"

    # Проверить создание основной модели
    # Данные загружаются через json настройки
    def test_load_company_model(self):
        # подготовка
        file_name = './settings.json'
        manager = settings_manager()
        manager.file_name=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == True
        assert manager.settings.company.name == "test"
        assert manager.settings.company.inn == 123456789012
        assert manager.settings.company.account == 12345678901
        assert manager.settings.company.corr_account == 12345678901
        assert manager.settings.company.bic == 123456789
        assert manager.settings.company.ownership == "OOOOO"

    # Проверить создание основной модели
    # Данные загружаются через json настройки из другой директории
    def test_load_other_directory_company_model(self):
        # подготовка
        file_name = 'D:/design_patterns/tests/data/other_settings.json'
        manager = settings_manager()
        manager.file_name=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == True
        assert manager.settings.company.name == "test"
        assert manager.settings.company.inn == 123456789012
        assert manager.settings.company.account == 12345678901
        assert manager.settings.company.corr_account == 12345678901
        assert manager.settings.company.bic == 123456789
        assert manager.settings.company.ownership == "OOOOO"

    # Проверить создание основной модели
    # Файл настроек не существует
    def test_load_not_exist_settings_settings_manager(self):
        # подготовка
        file_name = './invalid_settings.json'
        manager = settings_manager()

        # действие
        
        # проверки
        with self.assertRaises(argument_exception):
            manager.file_name=file_name

    # Проверить создание основной модели
    # Файл настроек поврежден
    def test_load_bad_settings_settings_manager(self):
        # подготовка
        file_name = './tests/data/bad_settings.json'
        manager = settings_manager()
        manager.file_name=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == False

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_singleton_company_model(self):
        # подготовка
        manager1 = settings_manager()
        manager2 = settings_manager()

        # действие

        # проверки
        assert manager1.settings == manager2.settings
        assert manager1.settings.company == manager2.settings.company

    # Проверка на сравнение двух по значению одинаковых моделей
    def test_create_equal_storage_model(self):
        # Подготовка
        id = uuid.uuid4().hex
        storage1 = storage_model()
        storage1.unique_code = id
        storage2 = storage_model()   
        storage2.unique_code = id
        # Действие GUID

        # Проверки
        assert storage1 == storage2

if __name__ == "__main__":
    unittest.main()