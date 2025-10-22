from src.core.validator import validator
from src.models.nomenclature_model import nomeclature_model
from src.core.entity_model import entity_model
from src.models.ingredient_model import ingredient_model

# модель рецепта
class recipe_model(entity_model):
    # список ингредиентов
    __ingredients: list = None
    # алгоритм приготовления
    __description: list = None

    def __init__(self):
       super().__init__()
       self.__ingredients: list = list()
       self.__description: list = list()

    @staticmethod
    def create(name):
        validator.validate(name, str)
        item = recipe_model()
        item.name = name
        item.ingredients = list()
        item.description = list()
        return item

    @property
    def ingredients(self) -> list:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, ingredient_list: list):
        validator.validate(ingredient_list, list)
        for ingredient in ingredient_list:
            validator.validate(ingredient, ingredient_model)
            self.__ingredients.append(ingredient)

    @property
    def description(self) -> list:
        return self.__description
    
    @description.setter
    def description(self, algorithm: list):
        validator.validate(algorithm, list)
        for step in algorithm:
            validator.validate(step, str)
            self.description.append(step)
