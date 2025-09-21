from src.models.settings import Settings
import json
import os

####################################################3
# Менеджер настроек. 
# Предназначен для управления настройками и хранения параметров приложения
class Settings_manager():
    __config_file:str = ""
    __settings:Settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings_manager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.default()

    @property
    def settings(self) -> Settings:
        return self.__settings
    
    @settings.setter
    def settings(self, value: Settings):
        if isinstance(value, Settings):
            self.__settings = value
    
    @property
    def config_file(self) -> str:
        return self.__config_file

    @config_file.setter
    def config_file(self, value:str):
        if value.strip() == "":
            return
        if os.path.exists(value):
            value=os.path.abspath(value.strip())
            self.__config_file = value
        else:
            raise FileNotFoundError("Не найден config файл!")

    def load(self) -> bool:
        try:
            with open( self.__config_file.strip(), 'r') as file_instance:
                return self.convert(json.load(file_instance))
        except:
            return False
        
    def convert(self, data: dict) -> bool:
        if "company" in data.keys():
            item = data["company"]
            required_keys = ["name", "inn", "account", "correspondent_account", "bic", "ownership"]
            missing_keys = [key for key in required_keys if key not in item]
            if missing_keys:
                raise KeyError(f"Отсутствуют обязательные поля: {', '.join(missing_keys)}!")
            self.settings.company.name = item["name"]
            self.settings.company.inn = item["inn"]
            self.settings.company.account = item["account"]
            self.settings.company.correspondent_account = item["correspondent_account"]
            self.settings.company.bic = item["bic"]
            self.settings.company.ownership = item["ownership"]
            return True
        else:
            raise ValueError("Неверный формат config файла или файл поврежден!")

    def default(self):
        self.settings = Settings()
        self.settings.company.name = "Default_name"
        self.settings.company.inn = "000000000000"
        self.settings.company.account = "00000000000"
        self.settings.company.corr_account = "00000000000"
        self.settings.company.bik = "000000000"
        self.settings.company.ownership = ""