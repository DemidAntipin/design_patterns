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
        for measure in dir(measure_model):
            if measure.startswith("create_"):
                measure_name = measure.split("_")[1]
                self.__repo.data[reposity.measure_key()][measure_name] = getattr(measure_model, measure)()
    
    # метод для генерации эталонных групп номенклатур
    def __create_default_nomenclature_groups(self):
        self.__repo.data[reposity.nomenclature_group_key()] = {}
        self.__repo.data[reposity.nomenclature_group_key()]["empty"] = nomenclature_group_model.create()

    # метод для генерации эталонных номенклатур
    def __create_default_nomenclatures(self):
        self.__repo.data[reposity.nomenclature_key()] = {}
        self.__repo.data[reposity.nomenclature_key()]["Картофель"] = nomeclature_model.create("Картофель", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["gramm"])
        self.__repo.data[reposity.nomenclature_key()]["Грибы"] = nomeclature_model.create("Грибы", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["gramm"])
        self.__repo.data[reposity.nomenclature_key()]["Лук"] = nomeclature_model.create("Лук", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["piece"])
        self.__repo.data[reposity.nomenclature_key()]["Кетчуп"] = nomeclature_model.create("Кетчуп", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["gramm"])
        self.__repo.data[reposity.nomenclature_key()]["Майонез"] = nomeclature_model.create("Майонез", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["gramm"])
        self.__repo.data[reposity.nomenclature_key()]["Сыр"] = nomeclature_model.create("Сыр", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["gramm"])
        self.__repo.data[reposity.nomenclature_key()]["Помидор"] = nomeclature_model.create("Помидор", self.__repo.data[reposity.nomenclature_group_key()]["empty"], self.__repo.data[reposity.measure_key()]["piece"])

    # метод для генерации эталонных рецептов
    def __create_default_recipes(self):
        self.__repo.data[reposity.recipe_key()] = {}
        recipe = recipe_model()
        recipe.name = "Картофельная запеканка с грибами"
        ingredient_list = [("Картофель", 400), ("Грибы", 300), ("Лук", 1), ("Кетчуп", 200), ("Майонез", 200), ("Сыр", 200), ("Помидор", 3)]
        for ingredient in ingredient_list:
            ingredient_name, ingredient_count = ingredient
            recipe.add_ingredient(self.__repo.data[reposity.nomenclature_key()][ingredient_name], ingredient_count)
        algorithm = ["Как приготовить вкустную картофельную запеканку? Подготовьте необходимые продукты. Из данного количества у меня получилось 3 большие порции.", 
                     "Картофель почистить, порезать крупными кусочками и равномерно распределить по противеню.", 
                     "Предварительно сварите грибы, порежьте средними кусочками и добавьте в запеканку.", 
                     "Крупную луковицу порезать кольцами и распределить по противеню.", 
                     "Выдавить сетку из майонеза и кетчупа, размещать тонким слоем по запеканке.", 
                     "Порежьте помидоры кружочками и разложите по запеканке.", 
                     "Обильно посыпать запеканку сверху тертым сыром.", 
                     "Поставьте запеканку в предварительно разогретую духовку до 200°C. Выпекать 60 минут, после чего дайте запеканке остыть. В горячем виде запеканка разваливается на части."]
        for step in algorithm:
            recipe.push(step)
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