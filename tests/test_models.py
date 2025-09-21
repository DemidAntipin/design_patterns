from src.models.company_model import company_model
from src.settings_manager import settings_manager
import unittest

class test_models(unittest.TestCase):
    # проверить создание основной модели
    # данные должны быть пустые
    def test_empty_createmodel_company_model(self):
        # подготовка
        model = company_model()
        # действие

        # проверки
        assert model.name == ""

    # проверить создание основной модели
    # данные должны быть не пустые
    def test_notEmpty_createmodel_company_model(self):
        # подготовка
        model = company_model()

        # действие
        model.name = "test"

        # проверки
        assert model.name == "test"

    # Проверить создание основной модели
    # Данные загружаются через json настройки
    def test_load_createmodel_company_model(self):
        # подготовка
        file_name = './settings.json'
        manager = settings_manager()
        manager.file_name=file_name

        # действие
        result = manager.load()
        
        # проверки
        assert result == True

    # Проверить создание основной модели
    # Данные загружаем. Проверяем работу Singletone
    def test_loadCombo_createmodel_companymodel(self):
        # подготовка
        file_name = './settings.json'
        manager1 = settings_manager()
        manager1.file_name = file_name
        manager2 = settings_manager()

        # действие
        manager1.load()

        # проверки
        assert manager1.company == manager2.company


if __name__ == "__main__":
    unittest.main()