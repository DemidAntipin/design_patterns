from src.core import validator
from src.core import abstact_reference
from src.core.entity_model import entity_model
import uuid

###############################################
# Модель организации
class company_model(entity_model):
    __inn:int = 0
    __bic:int = 0
    __corr_account:int = 0
    __account:int = 0
    __ownership:str = ""

    # ИНН : 12 симв
    # Счет 11 симв
    # Корреспондентский счет 11 симв
    # БИК 9 симв
    # Вид собственности 5 симв

    # Конструктор глубокого копирования
    def __init__(self, settings: 'settings_model' = None):
        super().__init__()
        try:
            from src.models.settings_model import settings_model
            validator.validate(settings, settings_model)
            fields = list(filter(lambda x: not x.startswith("_") , dir(settings.company)))
            for field in fields:
                value = getattr(settings.company, field)
                if not callable(value):
                    setattr(self, field, value)
            self.unique_code = uuid.uuid4().hex
        except:
            return


    # ИНН
    @property
    def inn(self) -> int:
        return self.__inn
    
    @inn.setter
    def inn(self, value:int):
        validator.validate(value, int, 12)
        self.__inn = value

    # КПП
    @property
    def bic(self) -> int:
        return self.__bic

    @bic.setter
    def bic(self, value:int):
        validator.validate(value, int, 9)
        self.__bic = value

    # Корреспондентский счет
    @property
    def corr_account(self) -> int:
        return self.__corr_account
        
    @corr_account.setter
    def corr_account(self, value:int):
        validator.validate(value, int, 11)
        self.__corr_account = value

    # Счёт
    @property
    def account(self) -> int:
        return self.__account
    
    @account.setter
    def account(self, value:int):
        validator.validate(value, int, 11)
        self.__account = value

    # Вид собственности
    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value:str):
        validator.validate(value, str, 5)
        self.__ownership = value.strip()