from src.core.validator import validator, argument_exception
from src.start_service import start_service
from src.reposity import reposity
from src.models.nomenclature_model import nomeclature_model
from src.models.transaction_model import transaction_model
from src.models.measure_model import measure_model
from src.models.storage_model import storage_model
from src.logic.ocb import ocb
from datetime import datetime
import unittest

class test_ocb(unittest.TestCase):

    # Проверка фильтрации транзакций по датам
    # Фильтрация только с end_date вернет список транзакций из service.data в которых transaction.date <= end_date
    # Фильтрация с start_date и end_date вернет список транзакций из service.data в которых transaction.date между start_date и end_date
    # Фильтрация без end_date вызовет argument_exception
    def test_filter_dates_transactions(self):
        # Подготовка
        service = start_service()
        service.start()
        ocb_ = ocb()
        ocb_.data = service.data

        start_date = datetime(2024, 1, 12)
        end_date = datetime(2024, 1, 15)

        # Действие
        period_transactions, _ = ocb_.filter_transactions(start_date=start_date, end_date=end_date)
        include_before_transactions, _ = ocb_.filter_transactions(end_date=end_date)

        # Проверки
        assert isinstance(period_transactions, list)
        assert isinstance(include_before_transactions, list)
        assert len(period_transactions) <= len(include_before_transactions)
        for transaction in period_transactions:
            assert isinstance(transaction, transaction_model)
            assert transaction.date >= start_date and transaction.date <= end_date
        for transaction in include_before_transactions:
            assert isinstance(transaction, transaction_model)
            assert transaction.date <= end_date
        with self.assertRaises(argument_exception):
            ocb_.filter_transactions(end_date=None)

    # Проверка фильтрации транзакций по номенклатурам
    # Фильтрация с номенклатурой вернет список транзакций, в которых все transaction.nomenclature соответствуют заданной
    def test_filter_nomenclature_transactions(self):
        # Подготовка
        service = start_service()
        service.start()
        nomenclature = service.data[reposity.nomenclature_key()][0]
        ocb_ = ocb()
        ocb_.data = service.data

        start_date = datetime(1, 1, 1)
        end_date = datetime(9999, 12, 31)

        # Действие
        nomenclature_transactions, _ = ocb_.filter_transactions(start_date=start_date, end_date=end_date, nomenclature=nomenclature)

        # Проверки
        assert isinstance(nomenclature_transactions, list)
        for transaction in nomenclature_transactions:
            assert isinstance(transaction, transaction_model)
            assert transaction.nomenclature == nomenclature

    # Проверка фильтрации транзакций по складам
    # Фильтрация с id склада вернет список транзакций, в которых все transaction.storage.unique_code соответствуют заданному
    def test_filter_storage_transactions(self):
        # Подготовка
        service = start_service()
        service.start()
        storage = service.data[reposity.storage_key()][0]
        ocb_ = ocb()
        ocb_.data = service.data

        start_date = datetime(1, 1, 1)
        end_date = datetime(9999, 12, 31)

        # Действие
        storage_transactions, _ = ocb_.filter_transactions(start_date=start_date, end_date=end_date, storage_id=storage.unique_code)

        # Проверки
        assert isinstance(storage_transactions, list)
        for transaction in storage_transactions:
            assert isinstance(transaction, transaction_model)
            assert transaction.storage == storage

    # Проверка функции подсчёта
    # Функция вернет сумму transaction.value из transaction_list в базовых ед transaction.measure
    def test_calculate_transaction_summary_value(self):
        # Подготовка
        service = start_service()
        service.start()
        nomenclature = service.data[reposity.nomenclature_key()][0]
        ocb_ = ocb()
        ocb_.data = service.data
        expected_value = 0
        for transaction in service.data[reposity.income_transaction_key()]:
            if transaction.nomenclature == nomenclature:
                expected_value += transaction.measure.to_base_unit_value(transaction.value)

        start_date = datetime(1, 1, 1)
        end_date = datetime(9999, 12, 31)
        nomenclature_transactions, _ = ocb_.filter_transactions(start_date=start_date, end_date=end_date, nomenclature=nomenclature)

        # Действие
        value = ocb_.calculate(nomenclature_transactions)

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
        expected_fields = {"start_value", "nomenclature", "measure", "income", "outcome", "end_value"}

        start_date = datetime(1, 1, 1)
        end_date = datetime(9999, 12, 31)

        # Действие
        report = ocb().create(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), storage.unique_code, service)

        # Проверки
        assert isinstance(report, list)
        for row in report:
            assert set(row.keys()) == expected_fields
            assert row["nomenclature"] in service.data[reposity.nomenclature_key()]
        assert len(report) == len(service.data[reposity.nomenclature_key()])      

if __name__ == '__main__':
    unittest.main() 