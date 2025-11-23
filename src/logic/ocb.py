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
    # Все транзакции отфильтрованы по номенклатуре, по типу (приход или расход) и по периоду дат
    def calculate(self, transaction_list:list):
        validator.validate(transaction_list, list)
        value = 0
        for transaction in transaction_list:
            validator.validate(transaction, transaction_model)
            value += transaction.measure.to_base_unit_value(transaction.value)
        return value

    # Создание отчёта, возвращает список словарей, каждый из которых соответствует 1 строчке таблицы
    def create(self, start_date, end_date, storage_id, filter) -> list:
        validator.validate(filter, (filter_sorting_dto, filter_dto))
        income_transactions = prototype(ocb.service.data[reposity.income_transaction_key()])
        outcome_transactions = prototype(ocb.service.data[reposity.outcome_transaction_key()])

        storage_filter = filter_sorting_dto.create_by_storage(storage_id)

        income_transactions = prototype.filter(income_transactions, storage_filter)
        outcome_transactions = prototype.filter(outcome_transactions, storage_filter)

        # Применение остальных фильтров
        income_transactions = prototype.filter(income_transactions, filter)
        outcome_transactions = prototype.filter(outcome_transactions, filter)

        filter_before = filter_sorting_dto.create_by_before_date(start_date)
        before_income_transactions = prototype.filter(income_transactions, filter_before)
        before_outcome_transactions = prototype.filter(outcome_transactions, filter_before)
        filter_period = filter_sorting_dto.create_by_period_date(start_date, end_date)
        period_income_transactions = prototype.filter(income_transactions, filter_period)
        period_outcome_transactions = prototype.filter(outcome_transactions, filter_period)

        result = []
        for nomenclature in ocb.service.data[reposity.nomenclature_key()]:
            row = {}
            filter_nomenclature = filter_sorting_dto.create_by_nomenclature(nomenclature)
            start_value = self.calculate(prototype.filter(before_income_transactions, filter_nomenclature).data) - self.calculate(prototype.filter(before_outcome_transactions, filter_nomenclature).data)
            income = self.calculate(prototype.filter(period_income_transactions, filter_nomenclature).data)
            outcome = self.calculate(prototype.filter(period_outcome_transactions, filter_nomenclature).data)
            row["start_value"]=start_value
            row["nomenclature"]=nomenclature
            row["measure"]=nomenclature.measure.get_base_unit()
            row["income"] = income
            row["outcome"] = outcome
            row["end_value"] = start_value + income - outcome
            result.append(row)
        return result