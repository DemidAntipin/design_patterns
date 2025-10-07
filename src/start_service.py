from src.reposity import reposity
from src.models.measure_model import measure_model
from src.models.recipe_model import recipe_model
from src.models.nomenclature_model import nomeclature_model
from src.models.nomenclature_group_model import nomenclature_group_model

class start_service():
    __repo:reposity = reposity()

    def __init__(self):
        self.__repo.data[reposity.measure_key()] = {}

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance
    
    # метод для генерации эталонных ед. измерения
    def __create_default_measures(self):
        self.__repo.data[reposity.measure_key()] = {}
        gramm = measure_model.create_gramm()
        kilogramm = measure_model.create_kilogramm(gramm)
        piece = measure_model.create_piece()
        measures=[gramm, kilogramm, piece]
        for measure in measures:
            # Проверка на уникальность
            if not measure.name in self.__repo.data[reposity.measure_key()]:
                self.__repo.data[reposity.measure_key()][measure.name] = measure
    
    # метод для генерации эталонных групп номенклатур
    def __create_default_nomenclature_groups(self):
        self.__repo.data[reposity.nomenclature_group_key()] = {}
        empty_group = nomenclature_group_model.create()
        # Проверка на уникальность
        if not "empty" in self.__repo.data[reposity.nomenclature_group_key()]:
            self.__repo.data[reposity.nomenclature_group_key()]["empty"]=empty_group

    # метод для генерации эталонных номенклатур
    def __create_default_nomenclatures(self):
        self.__repo.data[reposity.nomenclature_key()] = {}
        potato = nomeclature_model.create("Картофель", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["грамм"])
        mushroom = nomeclature_model.create("Грибы", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["грамм"])
        onion = nomeclature_model.create("Лук", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["шт"])
        ketchup = nomeclature_model.create("Кетчуп", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["грамм"])
        mayo = nomeclature_model.create("Майонез", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["грамм"])
        cheese = nomeclature_model.create("Сыр", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["грамм"])
        tomato = nomeclature_model.create("Помидор", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["шт"])
        nomenclatures = [potato, mushroom, onion, ketchup, mayo, cheese, tomato]
        for nomenclature in nomenclatures:
            # Проверка на уникальность
            if not nomenclature.name in self.__repo.data[reposity.nomenclature_key()]:
                self.__repo.data[reposity.nomenclature_key()][nomenclature.name] = nomenclature

    # метод для генерации эталонных рецептов
    def __create_default_recipes(self):
        self.__repo.data[reposity.recipe_key()] = {}
        recipe = recipe_model()
        recipe.name = "Картофельная запеканка с грибами"
        ingredient_list = [("Картофель", 400), ("Грибы", 300), ("Лук", 1), ("Кетчуп", 200), ("Майонез", 200), ("Сыр", 200), ("Помидор", 3)]
        ingredients=[]
        for ingredient in ingredient_list:
            ingredient_name, ingredient_count = ingredient
            ingredients.append((self.__repo.data[reposity.nomenclature_key()][ingredient_name], ingredient_count))
        recipe.ingredients = ingredients
        algorithm = ["Как приготовить вкустную картофельную запеканку? Подготовьте необходимые продукты. Из данного количества у меня получилось 3 большие порции.", 
                     "Картофель почистить, порезать крупными кусочками и равномерно распределить по противеню.", 
                     "Предварительно сварите грибы, порежьте средними кусочками и добавьте в запеканку.", 
                     "Крупную луковицу порезать кольцами и распределить по противеню.", 
                     "Выдавить сетку из майонеза и кетчупа, размещать тонким слоем по запеканке.", 
                     "Порежьте помидоры кружочками и разложите по запеканке.", 
                     "Обильно посыпать запеканку сверху тертым сыром.", 
                     "Поставьте запеканку в предварительно разогретую духовку до 200°C. Выпекать 60 минут, после чего дайте запеканке остыть. В горячем виде запеканка разваливается на части."]
        recipe.description = algorithm
        # Проверка на уникальность
        if not "default_recipe" in self.__repo.data[reposity.recipe_key()]:
            self.__repo.data[reposity.recipe_key()]["default_recipe"] = recipe

    @property
    def data(self):
        return self.__repo.data
    # основной метод для генерации эталонных данных
    def start(self):
        self.__create_default_measures()
        self.__create_default_nomenclature_groups()
        self.__create_default_nomenclatures()
        self.__create_default_recipes()