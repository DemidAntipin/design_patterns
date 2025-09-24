from src.models.company_model import Company_model
from src.settings_manager import Settings_manager
import unittest

class test_models(unittest.TestCase):
    # проверить создание основной модели
    # данные должны быть пустые
    def test_create_empty_company(self):
        # подготовка
        model = Company_model()
        # действие

        # проверки
        assert model.name == ""
        assert model.inn == ""
        assert model.account == ""
        assert model.correspondent_account == ""
        assert model.bic == ""
        assert model.ownership == ""

    # проверить создание основной модели
    # данные неверного типа
    def test_invalid_types_company_model(self):
        # подготовка
        model = Company_model()

        # действие

        # проверки
        with self.assertRaises(TypeError):
            model.name = dict()
        with self.assertRaises(TypeError):
            model.inn = dict()
        with self.assertRaises(TypeError):
            model.account = dict()
        with self.assertRaises(TypeError):
            model.correspondent_account = dict()
        with self.assertRaises(TypeError):
            model.bic = dict()
        with self.assertRaises(TypeError):
            model.ownership = dict()

    # проверить создание основной модели
    # данные содержат ошибки 
    def test_space_createmodel_company_model(self):
        # подготовка
        model = Company_model()
        
        # действие

        # проверки
        with self.assertRaises(ValueError):
            model.name = "  "
        with self.assertRaises(ValueError):
            model.inn = 123
        with self.assertRaises(ValueError):
            model.account = 123
        with self.assertRaises(ValueError):
            model.correspondent_account = 123
        with self.assertRaises(ValueError):
            model.bic = 123
        with self.assertRaises(ValueError):
            model.ownership = "OOOAAAOOO"
        


    # проверить создание основной модели
    # данные должны быть не пустые
    def test_notEmpty_createmodel_company_model(self):
        # подготовка
        model = Company_model()

        # действие
        model.name = "test"
        model.inn = "123456789012"
        model.account = "12345678901"
        model.correspondent_account = "12345678901"
        model.bic = "123456789"
        model.ownership = "OOO"

        # проверки
        assert model.name == "test"
        assert model.inn == "123456789012"
        assert model.account == "12345678901"
        assert model.correspondent_account == "12345678901"
        assert model.bic == "123456789"
        assert model.ownership == "OOO"

    # Проверить создание основной модели
    # Данные загружаются через json настройки
    def test_load_createmodel_company_model(self):
        # подготовка
        file_name = './settings.json'
        manager = Settings_manager()
        manager.config_file=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == True
        assert manager.settings.company.name == "test"
        assert manager.settings.company.inn == "123456789012"
        assert manager.settings.company.account == "12345678901"
        assert manager.settings.company.correspondent_account == "12345678901"
        assert manager.settings.company.bic == "123456789"
        assert manager.settings.company.ownership == "OOO"

    # Проверить создание основной модели
    # Данные загружаются через json настройки из другой директории
    def test_load_other_directory(self):
        # подготовка
        file_name = 'D:/design_patterns/tests/data/other_settings.json'
        manager = Settings_manager()
        manager.config_file=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == True
        assert manager.settings.company.name == "test"
        assert manager.settings.company.inn == "123456789012"
        assert manager.settings.company.account == "12345678901"
        assert manager.settings.company.correspondent_account == "12345678901"
        assert manager.settings.company.bic == "123456789"
        assert manager.settings.company.ownership == "OOO"

    # Проверить создание основной модели
    # Файл настроек не существует
    def test_load_not_exist_settings(self):
        # подготовка
        file_name = './invalid_settings.json'
        manager = Settings_manager()

        # действие
        
        # проверки
        with self.assertRaises(FileNotFoundError):
            manager.config_file=file_name

    # Проверить создание основной модели
    # Файл настроек поврежден
    def test_load_bad_settings(self):
        # подготовка
        file_name = './tests/data/bad_settings.json'
        manager = Settings_manager()
        manager.config_file=file_name
        file_name2 = './tests/data/bad_settings2.json'
        manager2 = Settings_manager()
        manager2.config_file=file_name2

        # действие
        result = manager.load()
        result2 = manager2.load()
        
        # проверки
        assert result == False
        assert result2 == False

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # подготовка
        manager1 = Settings_manager()
        manager2 = Settings_manager()

        # действие

        # проверки
        assert manager1.settings == manager2.settings
        assert manager1.settings.company == manager2.settings.company

    


if __name__ == "__main__":
    unittest.main()