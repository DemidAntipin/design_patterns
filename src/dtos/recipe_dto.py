from src.core.abstract_dto import abstact_dto

class recipe_dto(abstact_dto):
    __name: str = None
    __ingredients: list = None
    __description: list = None

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def ingredients(self) -> list:
        return self.__ingredients
    
    @ingredients.setter
    def ingredients(self, value):
        self.__ingredients = value

    @property
    def description(self) -> list:
        return self.__description
    
    @description.setter
    def description(self, value):
        self.__description = value