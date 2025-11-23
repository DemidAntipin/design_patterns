import time
from datetime import datetime
import random
from src.start_service import start_service
from src.reposity import reposity
from src.logic.rests import rests
from src.models.transaction_model import transaction_model
import pathlib
import unittest

class test_performance(unittest.TestCase):
    
    # Файл с результами нагрузочного тестирования
    __file_path: str = "tests/data/performance_test.md"

    # Нагрузочный тест
    def test_time_for_different_block_date(self):
        # Подготовка
        service = start_service()
        service.start()
        rest_service= rests()
        measures = service.data[reposity.measure_key()]
        nomenclatures = service.data[reposity.nomenclature_key()]
        storages = service.data[reposity.storage_key()]
        # сохранение предыдущих значений
        old_income_transactions = service.data[reposity.income_transaction_key()]
        old_outcome_transactions = service.data[reposity.outcome_transaction_key()]

        # генерация транзакций, у которых дата раньше медианой 
        for i in range(5000):
            random_date = datetime(year=random.randint(1901, 2023), month=random.randint(1, 12), day=random.randint(1, 28))      
            random_measure = random.choice(measures)
            random_nomenclature = random.choice(nomenclatures)
            random_storage = random.choice(storages)
            random_value = random.randint(1, 1000)
        
            # генерация транзакции с случайными значениями
            transaction = transaction_model.create(random_date,random_storage,random_nomenclature,random_measure,random_value)

            if random.random() >= 0.5:
                service.data[reposity.income_transaction_key()].append(transaction)
            else:
                service.data[reposity.outcome_transaction_key()].append(transaction)
        # генерация транзакций, у которых дата позже медианой 
        for i in range(5000):
            random_date = datetime(year=random.randint(2025, 2100), month=random.randint(1, 12), day=random.randint(1, 28))      
            random_measure = random.choice(measures)
            random_nomenclature = random.choice(nomenclatures)
            random_storage = random.choice(storages)
            random_value = random.randint(1, 1000)
        
            # генерация транзакции с случайными значениями
            transaction = transaction_model.create(random_date,random_storage,random_nomenclature,random_measure,random_value)

            if random.random() >= 0.5:
                service.data[reposity.income_transaction_key()].append(transaction)
            else:
                service.data[reposity.outcome_transaction_key()].append(transaction)

        # Действие
        result = "|Дата блокировки|Число транзакций|Длительность расчёта остатоков (секунд)|\n"
        result += "|:---|:---|:---|\n"
        # далекая block_date (множество транзакций в активном периоде)
        block_date = datetime(1900, 1, 1)
        rest_service.update_block_date(block_date)
        start_time = time.time()
        rest_service.show_rests(datetime(2200, 5, 12))
        end_time = time.time()
        result+=f"{datetime.strftime(block_date, "%Y-%m-%d")}| {10000} | {end_time - start_time}|\n"
        # медианная block_date (половина транзакций в активном периоде, половина до block_date)
        block_date = datetime(2024, 6, 15)
        rest_service.update_block_date(block_date)
        start_time = time.time()
        rest_service.show_rests(datetime(2200, 5, 12))
        end_time = time.time()
        result+=f"{datetime.strftime(block_date, "%Y-%m-%d")}| {10000} | {end_time - start_time}|\n"
        # близкая block_date (множество операций до block_date)
        block_date = datetime(2200, 1, 1)
        rest_service.update_block_date(block_date)
        start_time = time.time()
        rest_service.show_rests(datetime(2199, 12, 31))
        end_time = time.time()
        result+=f"{datetime.strftime(block_date, "%Y-%m-%d")}| {10000} | {end_time - start_time}|\n"

        service.data[reposity.income_transaction_key()]=old_income_transactions
        service.data[reposity.outcome_transaction_key()]=old_outcome_transactions

        file_path = pathlib.Path(self.__file_path)
        file_path.touch(exist_ok=True)

        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(result)
            file.close()

            




if __name__ == '__main__':
    unittest.main() 