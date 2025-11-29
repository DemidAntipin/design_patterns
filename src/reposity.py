from src.core.validator import validator

# репозиторий данных
class reposity:
    # словарь наименований моделей
    __data = {}

    @property
    def data(self):
        return self.__data
    
    # ключ для ед. измерения
    @staticmethod
    def measure_key():
        return "measure_model"
    
    # ключ для групп номенклатуры
    @staticmethod
    def nomenclature_group_key():
        return "nomenclature_group_model"
    
    # ключ для номенклатуры
    @staticmethod
    def nomenclature_key():
        return "nomenclature_model"
    
    # ключ для рецептов
    @staticmethod
    def recipe_key():
        return "recipe_model"
    
    # ключ для складов
    @staticmethod
    def storage_key():
        return "storage_model"

    # ключ для транзакций
    @staticmethod
    def transaction_key():
        return "transaction_model"
    
    @staticmethod
    def rest_key():
        return "rest_model"

    """
    Получить список всех ключей
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(reposity) if
                    callable(getattr(reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(reposity, method)()
            result.append(key)

        return result

    
    """
    Инициализация
    """
    def initalize(self):
        keys = reposity.keys()
        for key in keys:
            self.__data[ key ] = []
        self.__data[self.rest_key()] = {}

    """Метод получения объекта в памяти по уникальному коду"""
    def get_by_unique_code(self, unique_code: str):
        validator.validate(unique_code, str)
        for key in self.keys():
            items = self.data[key]
            for item in items:
                if item.unique_code == unique_code:
                    return item
        return None