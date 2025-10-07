from src.core.validator import validator
from src.core.abstract_reference import abstact_reference
from src.models.nomenclature_model import nomeclature_model

# модель рецепта
class recipe_model(abstact_reference):
    # список ингредиентов
    __ingredients: dict = None
    # алгоритм приготовления
    __description: list = None

    def __init__(self):
       super().__init__()
       self.__ingredients: dict = dict()
       self.__description: list = list()

    @property
    def ingredients(self) -> dict:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, ingredient_list: list):
        validator.validate(ingredient_list, list)
        for ingredient in ingredient_list:
            validator.validate(ingredient, tuple)
            validator.validate(ingredient[0], nomeclature_model)
            validator.validate(ingredient[1], int)
            self.ingredients[ingredient[0].name] = (ingredient[0], ingredient[1])

    @property
    def description(self) -> list:
        return self.__description
    
    @description.setter
    def description(self, algorithm: list):
        validator.validate(algorithm, list)
        for step in algorithm:
            validator.validate(step, str)
            self.description.append(step)
