from src.core.validator import validator
from src.start_service import start_service
from src.reposity import reposity
from src.models.nomenclature_model import nomeclature_model
from src.models.transaction_model import transaction_model
from src.core.prototype import prototype
from src.dtos.filter_dto import filter_dto
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.start_service import start_service
from src.core.filter_format import filter_format

class ocb:

    service: start_service = None

    def __init__(self, service):
        ocb.service = service

    # Функция подсчёта остатков в базовых единицах
    # Подразумевается что transaction_list содержит отфильтрованный список транзакций
    # Все транзакции отфильтрованы по номенклатуре и по периоду дат
    def calculate(self, transaction_list:list):
        validator.validate(transaction_list, list)
        income = 0
        outcome = 0
        for transaction in transaction_list:
            validator.validate(transaction, transaction_model)
            if transaction.value > 0:
                income += transaction.measure.to_base_unit_value(transaction.value)
            else:
                outcome += transaction.measure.to_base_unit_value(transaction.value)
        return income, outcome

    # Создание отчёта, возвращает список словарей, каждый из которых соответствует 1 строчке таблицы
    def create(self, start_date, end_date, storage_id, filter) -> list:
        validator.validate(filter, (filter_sorting_dto, filter_dto))
        transactions = prototype(ocb.service.data[reposity.transaction_key()])

        storage_filter = filter_sorting_dto.create_by_storage(storage_id)

        transactions = prototype.filter(transactions, storage_filter)

        # Применение остальных фильтров
        transactions = prototype.filter(transactions, filter)

        filter_before = filter_sorting_dto.create_by_before_date(start_date)
        before_transactions = prototype.filter(transactions, filter_before)
        filter_period = filter_sorting_dto.create_by_period_date(start_date, end_date)
        period_transactions = prototype.filter(transactions, filter_period)

        result = []
        for nomenclature in ocb.service.data[reposity.nomenclature_key()]:
            row = {}
            filter_nomenclature = filter_sorting_dto.create_by_nomenclature(nomenclature)
            start_value = sum(self.calculate(prototype.filter(before_transactions, filter_nomenclature).data))
            income, outcome = self.calculate(prototype.filter(period_transactions, filter_nomenclature).data)
            row["start_value"]=start_value
            row["nomenclature"]=nomenclature
            row["measure"]=nomenclature.measure.get_base_unit()
            row["income"] = income
            row["outcome"] = outcome
            row["end_value"] = start_value + income + outcome
            result.append(row)
        return result