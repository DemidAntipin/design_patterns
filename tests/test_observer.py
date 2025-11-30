import unittest
from src.start_service import start_service
from src.reposity import reposity
from src.logic.reference_service import reference_service
from src.logic.factory_converters import factory_converters
from src.core.abstract_dto import object_to_dto
from src.models.nomenclature_model import nomeclature_model
from src.core.prototype import prototype
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.dtos.block_date_dto import block_date_dto
from src.core.observe_service import observe_service
from src.core.event_type import event_type
from datetime import datetime
from src.core.validator import operation_exception

class test_observer(unittest.TestCase):
    
    # Добавление новой сущности
    def test_add_reference_reference_service(self):
        # Подготовка
        service = start_service()
        service.start()
        model_type="nomenclature_model"
        params={
            "name": "Ананас",
            "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "category_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
            "id": "12345678"
        }
        nomenclature_len = len(service.data[reposity.nomenclature_key()])
        last_nomenclature = service.data[reposity.nomenclature_key()][-1]
        factory = factory_converters()

        # Действие
        reference_service.add(model_type, params)

        # Проверки
        assert len(service.data[reposity.nomenclature_key()]) > nomenclature_len
        assert len(service.data[reposity.nomenclature_key()]) == nomenclature_len + 1
        assert last_nomenclature != service.data[reposity.nomenclature_key()][-1]
        model_dict = factory.convert(service.data[reposity.nomenclature_key()][-1])
        assert object_to_dto(model_dict) == params

        reference_service.remove(model_type, model_dict)

    # Изменение сущности
    def test_change_reference_reference_service(self):
        # Подготовка
        service = start_service()
        service.start()
        date_dto = block_date_dto().create({"new_block_date": datetime(2025, 1, 1)})
        observe_service.create_event(event_type.change_block_period(), date_dto)
        model_type="nomenclature_model"
        params={
            "unique_code": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
            "id" : "51"
        }
        old_model=service.repo.get_by_unique_code("0c101a7e-5934-4155-83a6-d2c388fcc11a")
        transactions_prototype = prototype(service.data[reposity.transaction_key()])
        transactions = prototype.filter(transactions_prototype, filter_sorting_dto.create_by_nomenclature(old_model)).data
        rest = service.data[reposity.rest_key()][old_model.unique_code]
        ingredients_prototype = prototype(service.data[reposity.recipe_key()][0].ingredients)
        ingredients = prototype.filter(ingredients_prototype, filter_sorting_dto.create_by_nomenclature(old_model)).data

        # Действие
        reference_service.change(model_type, params)
        new_model = service.repo.get_by_unique_code("51")

        # Проверки
        assert isinstance(new_model, nomeclature_model)
        # Изменена сама модель номенклатуры
        assert new_model in service.data[reposity.nomenclature_key()]
        assert old_model not in service.data[reposity.nomenclature_key()]
        # Изменены зависимости от номенклатуры
        for transaction in transactions:
            assert transaction.nomenclature == new_model
            assert transaction in service.data[reposity.transaction_key()]
        assert service.data[reposity.rest_key()][new_model.unique_code] == rest
        for ingredient in service.data[reposity.recipe_key()][0].ingredients:
            if ingredient in ingredients:
                assert ingredient.nomenclature == new_model

    # Удаление сущности с ошибкой
    def test_remove_reference_with_dependencies_reference_service(self):
        # Подготовка
        service = start_service()
        service.start()
        model_type="nomenclature_model"
        params={
            "unique_code": "0c101a7e-5934-4155-83a6-d2c388fcc11a",
        }

        # Проверки
        with self.assertRaises(operation_exception) as e:
            reference_service.remove(model_type, params)
        error_message = str(e.exception)
        self.assertIn("Отказ в удалении объекта по причине: удаляемый объект содержится в", error_message)

    # Удаление сущности
    def test_remove_reference_without_dependencies_reference_service(self):
        # Подготовка
        service = start_service()
        service.start()
        model_type="nomenclature_model"
        params={
            "name": "Ананас",
            "measure_id": "adb7510f-687d-428f-a697-26e53d3f65b7",
            "category_id": "7f4ecdab-0f01-4216-8b72-4c91d22b8918",
            "id": "12345678"
        }
        params2={
            "unique_code": "12345678",
        }

        # Действие
        reference_service.add(model_type, params)
        model = service.repo.get_by_unique_code("12345678")
        reference_service.remove(model_type, params2)

        # Проверки
        assert isinstance(model, nomeclature_model)
        assert model not in service.data[reposity.nomenclature_key()]
        model = service.repo.get_by_unique_code("12345678")
        assert model is None

        
        

if __name__ == "__main__":
    unittest.main()