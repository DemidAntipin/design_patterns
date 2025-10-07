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
    