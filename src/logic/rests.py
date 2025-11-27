from src.core.validator import validator, argument_exception
from src.reposity import reposity
from src.models.nomenclature_model import nomeclature_model
from src.models.transaction_model import transaction_model
from src.core.prototype import prototype
from src.dtos.filter_dto import filter_dto
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.start_service import start_service
from src.core.filter_format import filter_format
from datetime import datetime
from src.models.rest_model import rest_model
from src.logic.factory_converters import factory_converters

class rests:

    service: start_service = None

    def __init__(self):
        rests.service = start_service()
        rests.service.start()

    # Функция подсчёта остатков в базовых единицах
    # транзакции отфильтрованы по номенклатуре, складу и позже дате блокировки
    def calculate(self, income_transaction_list:list, outcome_transaction_list:list):
        validator.validate(income_transaction_list, list)
        validator.validate(outcome_transaction_list, list)
        value = 0
        for transaction in income_transaction_list:
            validator.validate(transaction, transaction_model)
            value += transaction.measure.to_base_unit_value(transaction.value)
        for transaction in outcome_transaction_list:
            validator.validate(transaction, transaction_model)
            value -= transaction.measure.to_base_unit_value(transaction.value)
        return value
    
    # Обновить дату блокировки и пересчитать остатки.
    def update_block_date(self, new_date:datetime):
        validator.validate(new_date, datetime)
        income_transactions = prototype(rests.service.data[reposity.income_transaction_key()])
        outcome_transactions = prototype(rests.service.data[reposity.outcome_transaction_key()])
        filter = filter_sorting_dto.create_by_before_date(new_date)
        income_transactions = prototype.filter(income_transactions, filter)
        outcome_transactions = prototype.filter(outcome_transactions, filter)
        result = {}
        for transaction in income_transactions.data:
            value = transaction.measure.to_base_unit_value(transaction.value)
            nomenclature = transaction.nomenclature
            if nomenclature.unique_code in result:
                rest = result[nomenclature.unique_code]
                validator.validate(rest, rest_model)
                rest.value += rest.measure.from_base_unit_value(value)
            else:
                measure = nomenclature.measure
                rest = rest_model.create(nomenclature=nomenclature, measure=measure, value=measure.from_base_unit_value(value))
                result[nomenclature.unique_code] = rest
        for transaction in outcome_transactions.data:
            value = transaction.measure.to_base_unit_value(transaction.value)
            nomenclature = transaction.nomenclature
            if nomenclature.unique_code in result:
                rest = result[nomenclature.unique_code]
                validator.validate(rest, rest_model)
                rest.value -= rest.measure.from_base_unit_value(value)
            else:
                measure = nomenclature.measure
                rest = rest_model.create(nomenclature=nomenclature, measure=measure, value=-measure.from_base_unit_value(value))
                result[nomenclature.unique_code] = rest
        rests.service.data[reposity.rest_key()] = result
        rests.service.block_date = new_date


    # Подсчёт остатков к указанной дате, возвращает список словарей, содержащих остатки номенклатур
    def show_rests(self, date) -> list:
        validator.validate(date, datetime)
        income_transactions = prototype(rests.service.data[reposity.income_transaction_key()])
        outcome_transactions = prototype(rests.service.data[reposity.outcome_transaction_key()])

        # если указана дата раньше даты блокировки - проигнорировать и заменить на дату блокировки
        date = rests.service.block_date if date < rests.service.block_date else date

        # фильтр для периода с даты блокировки до указанной даты
        filter_period = filter_sorting_dto.create_by_period_date(rests.service.block_date, date)
        period_income_transactions = prototype.filter(income_transactions, filter_period)
        period_outcome_transactions = prototype.filter(outcome_transactions, filter_period)

        result = []
        for nomenclature in rests.service.data[reposity.nomenclature_key()]:
            row = {}
            filter_nomenclature = filter_sorting_dto.create_by_nomenclature(nomenclature)
            # получить сохраненный остаток
            rest_value = rests.service.data[reposity.rest_key()][nomenclature.unique_code].value if nomenclature.unique_code in rests.service.data[reposity.rest_key()] else 0
            # подсчёт текущего остатка = сохраненный остаток + остаток активного периода
            value = rest_value + nomenclature.measure.from_base_unit_value(self.calculate(prototype.filter(period_income_transactions, filter_nomenclature).data, prototype.filter(period_outcome_transactions, filter_nomenclature).data))
            row["nomenclature"]=factory_converters().convert(nomenclature)
            row["measure"]=factory_converters().convert(nomenclature.measure)
            row["value"] = value
            result.append(row)
        return result