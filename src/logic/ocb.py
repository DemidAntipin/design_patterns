from src.core.validator import validator
from src.start_service import start_service
from src.reposity import reposity
from src.models.nomenclature_model import nomeclature_model
from src.models.transaction_model import transaction_model
from datetime import datetime

class ocb:
    # Репозиторий данных, копируется из start_service.data
    __data: dict = None

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, dict_:dict):
        validator.validate(dict_, dict)
        self.__data = dict_

    # Фильтрация транзакций по заданным условиям
    # Обязательный аргумент:
    #   end_date - конец расчётного периода
    # Необязательные аргументы:
    #   start_date - начало расчётного периода, если не передан - любая дата считается позже начала расчётного периода
    #   nomenclature - номенклатура, если передан - отбор только тех транзакций, что содержат ту же номенклатуру
    #   storage_id - id склада, если передан - отбор только тех транзакций, id склада которых соответсвует переданному
    # Возвращает кортеж отфильтрованных транзакций:
    #   (список_приходных_транзакций, список_расходных_транзакций)
    def filter_transactions(self, end_date:datetime, start_date:datetime = None, nomenclature:nomeclature_model = None, storage_id: str = None):
        validator.validate(end_date, datetime)
        income_transactions = []
        for transaction in self.__data["income_transaction_model"]:
            if start_date:
                validator.validate(start_date, datetime)
                if transaction.date < start_date:
                    continue
            if transaction.date > end_date:
                continue
            if nomenclature and transaction.nomenclature != nomenclature:
                continue
            if storage_id and transaction.storage.unique_code != storage_id:
                continue
            income_transactions.append(transaction)
        outcome_transactions = []
        for transaction in self.__data["outcome_transaction_model"]:
            if start_date:
                if transaction.date < start_date:
                    continue
            if transaction.date > end_date:
                continue
            if nomenclature:
                validator.validate(nomenclature, nomeclature_model)
                if transaction.nomenclature != nomenclature:
                    continue
            if storage_id:
                validator.validate(storage_id, str)
                if transaction.storage.unique_code != storage_id:
                    continue
            outcome_transactions.append(transaction)
        return income_transactions, outcome_transactions

    # Функция подсчёта остатков в базовых единицах
    # Подразумевается что transaction_list содержит отфильтрованный список транзакций
    # Все транзакции отфильтрованы по номенклатуре, по типу (приход или расход) и по периоду дат
    def calculate(self, transaction_list:list):
        validator.validate(transaction_list, list)
        value = 0
        for transaction in transaction_list:
            validator.validate(transaction, transaction_model)
            value += transaction.measure.to_base_unit_value(transaction.value)
        return value

    # Создание отчёта, возвращает список словарей, каждый из которых соответствует 1 строчке таблицы
    def create(self, start_date:str, end_date:str, storage_id:str, service: start_service) -> list:
        start_date, end_date = validator.validate_period(start_date, end_date)
        validator.validate_id(storage_id, [value for value in service.data[reposity.storage_key()]])
        self.__data = service.data
        result = []

        for nomenclature in service.data[reposity.nomenclature_key()]:
            row = {}
            # транзакции в указанном периоде
            income_transactions, outcome_transactions = self.filter_transactions(start_date=start_date, end_date=end_date, nomenclature=nomenclature, storage_id=storage_id)
            income = self.calculate(income_transactions)
            outcome = self.calculate(outcome_transactions)
            # дополнительно включает транзакции до начала периода
            income_transactions, outcome_transactions = self.filter_transactions(end_date=end_date, nomenclature=nomenclature, storage_id=storage_id)
            # транзакции за все время - транзакции в периоде = транзакции до периода
            start_value = (self.calculate(income_transactions) - income) - (self.calculate(outcome_transactions) - outcome)
            row["start_value"]=start_value
            row["nomenclature"]=nomenclature
            row["measure"]=nomenclature.measure.get_base_unit()
            row["income"] = income
            row["outcome"] = outcome
            row["end_value"] = start_value + income - outcome
            result.append(row)
        return result