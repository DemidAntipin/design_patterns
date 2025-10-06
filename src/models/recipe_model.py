from src.core.validator import validator
from src.core.abstract_reference import abstact_reference
from src.models.nomenclature_model import nomeclature_model
from queue import Queue

# модель рецепта
class recipe_model(abstact_reference):
    # список ингредиентов
    __ingredients: dict = None
    # алгоритм приготовления
    __description: Queue = None

    def __init__(self):
       super().__init__()
       self.__ingredients: dict = dict()
       self.__description: Queue = Queue()

    @property
    def ingredients(self) -> dict:
        return self.__ingredients
    
    # метод для добавления ингредиента
    def add_ingredient(self, ingredient: nomeclature_model, count: int):
        # номенклатура ингредиента
        validator.validate(ingredient, nomeclature_model)
        # количество ингредиента в ед. измерения указанной в ingredient.measure_unit
        validator.validate(count, int)
        self.ingredients[ingredient.name] = (ingredient, count)

    @property
    def description(self) -> Queue:
        return self.__description

    # метод для нового шага алгоритма
    def push(self, elem: str):
        validator.validate(elem, str, 255)
        self.description.put(elem)

    # метод для извлечения текущего шага алгоритма
    def pop(self) -> str:
        elem = self.description.get()
        return elem