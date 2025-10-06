from src.models.company_model import company_model
from src.settings_manager import settings_manager
from src.models.nomenclature_group_model import nomenclature_group_model
from src.models.nomenclature_model import nomeclature_model
from src.models.measure_model import measure_model
from src.models.storage_model import storage_model
from src.core.validator import validator, argument_exception, operation_exception
from src.core.abstract_reference import abstact_reference
from src.models.recipe_model import recipe_model
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
            model.inn = 1234567890123456789
        with self.assertRaises(argument_exception):
            model.account = 1234567890123456789
        with self.assertRaises(argument_exception):
            model.corr_account = 1234567890123456789
        with self.assertRaises(argument_exception):
            model.bic = 1234567890123456789
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

    # Проверить создание абстрактной модели
    # Поле name задается вручную, а unique_code автоматически.
    def test_create_empty_abstract_reference(self):
        # подготовка
        empty_abstract = abstact_reference()
        not_empty_abstract = abstact_reference()

        # действие
        not_empty_abstract.name = "test"

        # проверки
        assert empty_abstract.name == ""
        assert validator.validate(empty_abstract.unique_code, str)
        assert not_empty_abstract.name == "test"
        assert validator.validate(not_empty_abstract.unique_code, str)

    # Проверить создание абстрактной модели
    # Некорректные данные
    def test_invalid_data_abstract_reference(self):
        # подготовка
        abstract = abstact_reference()

        # действие

        # проверки
        with self.assertRaises(argument_exception):
            abstract.name = 512
        with self.assertRaises(argument_exception):
            abstract.name = "A" * 51

    # Проверить создание абстрактной модели
    # Проверка на принадлежность или наследуемость класса от abstract_reference. Сравнение истинно, если у объектов совпадают unique_code.
    def test_comparsion_abstract_reference(self):
        # подготовка
        id = uuid.uuid4().hex
        abstract = abstact_reference()
        company = company_model()
        storage = storage_model()
        abstract.unique_code = id
        company.unique_code = id

        # действие

        # проверки
        with self.assertRaises(argument_exception):
            abstract == 512
        assert abstract == company
        assert abstract != storage

    # Проверить создание основной модели
    # Глубокая копия из settings, совпадают все данные кроме unique_id.
    def test_deep_copy_from_settings_company_model(self):
        # подготовка
        manager = settings_manager()
        manager.settings.company.name = "test"
        manager.settings.company.inn = 123456789012
        manager.settings.company.account = 12345678901
        manager.settings.company.corr_account = 12345678901
        manager.settings.company.bic = 123456789
        manager.settings.company.ownership = "OOOOO"

        # Действие
        company = company_model(manager.settings)

        # проверки
        assert company.name == "test"
        assert company.inn == 123456789012
        assert company.account == 12345678901
        assert company.corr_account == 12345678901
        assert company.bic == 123456789
        assert company.ownership == "OOOOO"
        assert company != manager.settings.company

    # Проверить создание основной модели
    # Данные загружаем. Файл настроек содержит только часть полей company_model. Остальные значения остаются по-умолчанию.
    def test_load_matching_parameters_settings_manager(self):
        # подготовка
        file_name = './tests/data/particular_settings.json'
        manager = settings_manager()
        manager.file_name=file_name

        # действие
        result = manager.load()

        # проверки
        assert result == True
        assert manager.settings.company.name == "test"
        assert manager.settings.company.inn == 0
        assert manager.settings.company.account == 12345678901
        assert manager.settings.company.corr_account == 0
        assert manager.settings.company.bic == 0
        assert manager.settings.company.ownership == ""

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

    # Проверка на сравнение двух разных по значению моделей
    def test_create_equal_storage_model(self):
        # Подготовка
        storage1 = storage_model()
        storage2 = storage_model()   
        # Действие

        # Проверки
        assert storage1 != storage2

    # Проверка создания базовой единицы измерения
    def test_create_base_measure_model(self):
        # Подготовка
        base_range = measure_model("грамм", 1)

        # Действие
        
        # Проверка
        assert base_range.name == "грамм"
        assert base_range.coef == 1
        assert base_range.base_unit == None

    # Проверить создание не базовой единицы измерения
    def test_create_not_base_measure_model(self):
        # Подготовка
        gr = measure_model("грамм", 1)
        kg = measure_model("кг", 1000, gr)
        ton = measure_model("тонна", 1000, kg)

        # Действие
        
        # Проверка
        assert kg.name == "кг"
        assert kg.coef == 1000
        assert kg.base_unit == gr
        assert ton.name == "тонна"
        assert ton.coef == 1000
        assert ton.base_unit == kg

    # Проверить создание номенклатуры
    # Данные должны быть пустыми
    def test_create_empty_nomenclature_model(self):
        # Подготовка
        nomeclature = nomeclature_model.create_empty()

        # Действие

        # Проверки
        assert nomeclature.name == "Default_name"
        assert nomeclature.measure_unit is None
        assert nomeclature.nomenclature_group is None

    # Проверить создание номенклатуры
    # Данные с ошибками
    def test_invalid_data_nomenclature_model(self):
        # Подготовка
        nomeclature = nomeclature_model.create_empty()

        # Действие

        # Проверки
        with self.assertRaises(argument_exception):
            nomeclature.name = dict()
        with self.assertRaises(argument_exception):
            nomeclature.name = "A" * 256
        with self.assertRaises(argument_exception):
            nomeclature.nomenclature_group = 512
        with self.assertRaises(argument_exception):
            nomeclature.measure_unit = tuple()
        
    # Проверить создание номенклатуры
    # Данные должны быть не пустые
    def test_create_not_empty_nomenclature_model(self):
        # подготовка
        name = "A" * 255
        group = nomenclature_group_model()
        measure = measure_model("грамм", 1)
        nomeclature = nomeclature_model.create(name, group, measure)

        # действие
        

        # проверки
        assert nomeclature.name == "A" * 255
        assert nomeclature.measure_unit.name == "грамм"
        assert nomeclature.measure_unit.coef == 1
        assert nomeclature.measure_unit.base_unit is None
        assert isinstance(nomeclature.nomenclature_group, nomenclature_group_model)

    # Проверить создание рецепта
    # Данные должны быть пустые
    def test_create_empty_recipe_model(self):
        # подготовка
        recipe = recipe_model()

        # действие

        # проверки
        assert recipe.name == ""
        assert isinstance(recipe.ingredients, dict)
        assert len(recipe.ingredients) == 0
        assert recipe.description.qsize() == 0

    # Проверить создание рецепта
    # Данные должны не пустые
    def test_create_not_empty_recipe_model(self):
        # подготовка
        recipe = recipe_model()
        recipe.name = "Запеканка"
        measure_unit = measure_model.create_gramm()
        group = nomenclature_group_model.create()
        ingredient = nomeclature_model.create("Специи", group, measure_unit)
        recipe.add_ingredient(ingredient, 20)
        recipe.push("Печь до готовности")

        # действие
        step = recipe.pop()

        # проверки
        print(step)
        assert recipe.name == "Запеканка"
        assert recipe.ingredients["Специи"][0]==ingredient
        assert step == "Печь до готовности"


if __name__ == "__main__":
    unittest.main()