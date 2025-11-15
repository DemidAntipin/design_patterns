from src.start_service import start_service
from src.reposity import reposity
from src.logic.ocb import ocb
from datetime import datetime
from src.dtos.filter_sorting_dto import filter_sorting_dto
import unittest

class test_ocb(unittest.TestCase):


    # Проверка функции подсчёта
    # Функция вернет сумму transaction.value из transaction_list в базовых ед transaction.measure
    def test_calculate_transaction_summary_value(self):
        # Подготовка
        service = start_service()
        service.start()
        ocb_ = ocb(service)
        ocb_.data = service.data
        expected_value = 0
        for transaction in service.data[reposity.income_transaction_key()]:
            expected_value += transaction.measure.to_base_unit_value(transaction.value)

        # Действие
        value = ocb_.calculate(service.data[reposity.income_transaction_key()])

        # Проверки
        assert value == expected_value

    # Проверка создания отчёта ocb
    # Метод create() вернет список словарей
    # Каждый словарь имеет одинаковый набор ключей expected_fields
    # для каждой nomenclature из service.data[reposity.nomenclature_key()] будет соответсвовать свой словарь (значение по "nomenclature" == nomenclature)
    def test_create_ocb_report(self):
        # Подготовка
        service = start_service()
        service.start()
        storage = service.data[reposity.storage_key()][0]

        filters = filter_sorting_dto([{
            "field_name": "storage",
            "value": storage,
            "format": "=="
        }], [])
        expected_fields = {"start_value", "nomenclature", "measure", "income", "outcome", "end_value"}

        start_date = datetime(1, 1, 1)
        end_date = datetime(9999, 12, 31)

        # Действие
        report = ocb(service).create(start_date.date(), end_date.date(), filters)

        # Проверки
        assert isinstance(report, list)
        for row in report:
            assert set(row.keys()) == expected_fields
            assert row["nomenclature"] in service.data[reposity.nomenclature_key()]
        assert len(report) == len(service.data[reposity.nomenclature_key()])      

if __name__ == '__main__':
    unittest.main() 