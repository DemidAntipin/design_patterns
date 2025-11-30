from src.core.event_type import event_type
from src.core.validator import validator, operation_exception

class abstract_subscriber:
    """
    Обработка события
    """
    def handle(self,  event: str, params):
        validator.validate(event, str)
        events =  event_type.events()
        if event not in events:
            raise operation_exception(f"{events} - не является событием!")