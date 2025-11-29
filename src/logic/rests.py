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
from src.core.abstract_subscriber import abstract_subscriber
from src.core.observe_service import observe_service
from src.core.event_type import event_type

class rests(abstract_subscriber):

    service: start_service = None

    def __init__(self):
        rests.service = start_service()
        rests.service.start()
        observe_service.add(self)

    # Функция подсчёта остатков в базовых единицах
    # транзакции отфильтрованы по номенклатуре, складу и позже дате блокировки
    def calculate(self, transaction_list:list):
        validator.validate(transaction_list, list)
        value = 0
        for transaction in transaction_list:
            validator.validate(transaction, transaction_model)
            value += transaction.measure.to_base_unit_value(transaction.value)
        return value
    
    # Обновить дату блокировки и пересчитать остатки.
    def update_block_date(self, new_date:datetime):
        validator.validate(new_date, datetime)
        transactions = prototype(rests.service.data[reposity.transaction_key()])
        filter = filter_sorting_dto.create_by_before_date(new_date)
        transactions = prototype.filter(transactions, filter)
        result = {}
        for transaction in transactions.data:
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
        rests.service.data[reposity.rest_key()] = result


    # Подсчёт остатков к указанной дате, возвращает список словарей, содержащих остатки номенклатур
    def show_rests(self, date) -> list:
        validator.validate(date, datetime)
        transactions = prototype(rests.service.data[reposity.transaction_key()])

        # если указана дата раньше даты блокировки - проигнорировать и заменить на дату блокировки
        date = rests.service.block_date if date < rests.service.block_date else date

        # фильтр для периода с даты блокировки до указанной даты
        filter_period = filter_sorting_dto.create_by_period_date(rests.service.block_date, date)
        period_transactions = prototype.filter(transactions, filter_period)

        result = []
        for nomenclature in rests.service.data[reposity.nomenclature_key()]:
            row = {}
            filter_nomenclature = filter_sorting_dto.create_by_nomenclature(nomenclature)
            # получить сохраненный остаток
            rest_value = rests.service.data[reposity.rest_key()][nomenclature.unique_code].value if nomenclature.unique_code in rests.service.data[reposity.rest_key()] else 0
            # подсчёт текущего остатка = сохраненный остаток + остаток активного периода
            value = rest_value + nomenclature.measure.from_base_unit_value(self.calculate(prototype.filter(period_transactions, filter_nomenclature).data))
            row["nomenclature"]=factory_converters().convert(nomenclature)
            row["measure"]=factory_converters().convert(nomenclature.measure)
            row["value"] = value
            result.append(row)
        return result
    
    """
    Обработка событий
    """
    def handle(self, event:str, params:dict):
        validator.validate(params, dict)
        super().handle(event, params)

        # Инициализация rests() вызывает start_service.__init__() -> settings_manager.__init__()
        # Следовательно settings_manager, являясь singleton, подпишется на observe_service раньше,
        # rests, следовательно к моменту вызова rests.handle() дата блокировки будет гарантировано изменена.
        if event == event_type.change_block_period():
            new_block_date = params["new_block_date"]
            validator.validate(new_block_date, datetime)
            self.update_block_date(new_block_date)  