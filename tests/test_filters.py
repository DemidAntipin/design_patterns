import unittest
from src.core.prototype import prototype
from src.start_service import start_service
from src.reposity import reposity
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.models.nomenclature_group_model import nomenclature_group_model

class test_filters(unittest.TestCase):

    # Проверить создание прототипа
    def test_create_empty_prototype(self):
        # Подготовка
        proto = prototype([])

        # Действие

        # Проверка
        assert isinstance(proto, prototype)
        assert isinstance(proto.data, list)
        assert len(proto.data) == 0

    # Проверить клонирование прототипа
    # prototype и prototype.clone() 2 разных объекта класса prototype, но имеют одинаковые данные
    def test_clone_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        transactions = service.data[reposity.income_transaction_key()]
        proto = prototype(transactions)

        # Действие
        proto2 = prototype.clone(proto)

        # Проверки
        assert isinstance(proto, prototype)
        assert isinstance(proto2, prototype)
        assert proto != proto2
        assert proto.data == proto2.data

    # Проверить пустой фильтр
    # Фильтрация должна склонировать прототип с теми же данными
    def test_filter_empty_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        transactions = service.data[reposity.income_transaction_key()]
        proto = prototype(transactions)
        filters = filter_sorting_dto([], [])

        # Действие
        proto2 = prototype.filter(proto,filters)

        # Проверки
        assert isinstance(proto, prototype)
        assert isinstance(proto2, prototype)
        assert proto != proto2
        assert proto.data == proto2.data

    # Проверить фильтрацию
    # Фильтрация должна склонировать прототип, удалив данные, что не подходят
    def test_filter_equals_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        data = [nomenclature_group_model().create("test1"), nomenclature_group_model().create("test2")]
        proto = prototype(data)
        filters = filter_sorting_dto([{
            "field_name": "name",
            "value": "test1",
            "format": "=="
        }], [])

        # Действие
        proto2 = prototype.filter(proto,filters)

        # Проверки
        assert isinstance(proto, prototype)
        assert isinstance(proto2, prototype)
        assert len(proto.data) == 2
        assert len(proto2.data) == 1
        assert 'test1' in [item.name for item in proto.data] and 'test2' in [item.name for item in proto.data] 
        assert 'test1' in [item.name for item in proto2.data] and 'test2' not in [item.name for item in proto2.data]

    # Проверить фильтрацию
    # Фильтрация должна учитывать подстроки
    def test_filter_like_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        data = [nomenclature_group_model().create("test1"), nomenclature_group_model().create("test2"), nomenclature_group_model().create("wrong")]
        proto = prototype(data)
        filters = filter_sorting_dto([{
            "field_name": "name",
            "value": "test",
            "format": "like"
        }], [])

        # Действие
        proto2 = prototype.filter(proto,filters)

        # Проверки
        assert isinstance(proto, prototype)
        assert isinstance(proto2, prototype)
        assert len(proto.data) == 3
        assert len(proto2.data) == 2
        assert 'test1' in [item.name for item in proto.data] and 'test2' in [item.name for item in proto.data] 
        assert 'test1' in [item.name for item in proto2.data] and 'test2' in [item.name for item in proto2.data]

    # Проверить фильтрацию объектов
    # Фильтрация должна вернуть транзакции в ед. измерения "Грамм"
    def test_filter_object_equals_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        data = service.data[reposity.income_transaction_key()]
        measure = service.data[reposity.measure_key()][0]
        proto = prototype(data)
        filters = filter_sorting_dto([{
            "field_name": "measure",
            "value": measure,
            "format": "=="
        }], [])

        # Действие
        proto2 = prototype.filter(proto,filters)

        # Проверки
        assert isinstance(proto2, prototype)
        for transaction in proto2.data:
            assert transaction.measure == measure

    # Проверить фильтрацию объектов
    # Фильтрация должна вернуть транзакции в ед. измерения "Грамм" (учитывая базовые единицы измерения)
    def test_filter_object_equals_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        data = service.data[reposity.income_transaction_key()]
        measure = service.data[reposity.measure_key()][0]
        proto = prototype(data)
        filters = filter_sorting_dto([{
            "field_name": "measure",
            "value": measure,
            "format": "like"
        }], [])

        # Действие
        proto2 = prototype.filter(proto,filters)
        unique_measures = []
        for trans in proto2.data:
            if trans.measure not in unique_measures:
                unique_measures.append(trans.measure)

        # Проверки
        assert isinstance(proto2, prototype)
        for transaction in proto2.data:
            assert transaction.measure == measure or transaction.measure.base_unit == measure
        assert len(unique_measures) == 2
        assert "Грамм" in [m.name for m in unique_measures]
        assert "Киллограмм" in [m.name for m in unique_measures]

    # Проверить сортировку объектов
    # Фильтрация сортирует объекты по указанным полям, причем порядок полей указывает на их приоритет от самого важного к наименее важному
    def test_filter_sorting_prototype(self):
        # Подготовка
        service = start_service()
        service.start()
        data = service.data[reposity.income_transaction_key()]
        proto = prototype(data)
        filters = filter_sorting_dto([], ["measure", "unique_code"])

        # Действие
        proto2 = prototype.filter(proto,filters)

        # Проверки
        assert isinstance(proto2, prototype)
        assert len(proto2.data) > 1
        prev_transaction = proto2.data[0]
        for transaction in proto2.data[1:]:
            assert transaction.measure >= prev_transaction.measure
            if transaction.measure == prev_transaction.measure:
                assert transaction.unique_code >= prev_transaction.unique_code
            prev_transaction = transaction

if __name__ == "__main__":
    unittest.main()