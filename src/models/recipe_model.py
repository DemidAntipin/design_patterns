from src.core.validator import validator
from src.models.nomenclature_model import nomeclature_model
from src.core.entity_model import entity_model
from src.models.ingredient_model import ingredient_model
from src.dtos.recipe_dto import recipe_dto
from src.dtos.ingredient_dto import ingredient_dto

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

    # Фабричный метод
    def from_dto(dto:recipe_dto, cache:dict):
        validator.validate(dto, recipe_dto)
        validator.validate(cache, dict)
        item = recipe_model.create(dto.name)
        for ingredient in dto.ingredients:
            ing_dto = ingredient_dto().create(ingredient)
            ing = ingredient_model.from_dto(ing_dto, cache)
            item.ingredients.append(ing)
        for step in dto.description:
            item.description.append(step)
        return item