import unittest
from src.start_service import start_service
from src.reposity import reposity
from src.models.measure_model import measure_model


class test_start(unittest.TestCase):
    __start_service: start_service = start_service()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start()

    # Проверка генерации эталонных ед. измерения
    # данные доступны по ключу "measure_key"
    # ед. измерения с уникальными именами являются синглтонами
    def test_measure_units_start_service(self):
        # подготовка
        gramm = measure_model.create_gramm()

        # действие

        # проверки
        assert len(self.__start_service.data[reposity.measure_key()]) > 0
        assert self.__start_service.data[reposity.measure_key()]["грамм"].name == "грамм"
        assert self.__start_service.data[reposity.measure_key()]["килограмм"].name == "килограмм"
        assert self.__start_service.data[reposity.measure_key()]["шт"].name == "шт"
        assert self.__start_service.data[reposity.measure_key()]["грамм"] == self.__start_service.data[reposity.measure_key()]["килограмм"].base_unit

    # Проверка генерации эталонных групп номенклатуры
    # данные доступны по ключу "nomenclature_group_key"
    def test_nomenclature_group_start_service(self):
        # подготовка

        # действие

        # проверки
        assert len(self.__start_service.data[reposity.nomenclature_group_key()])>0

    # Проверка генерации эталонных номенклатур (ингредиентов)
    # данные доступны по ключу "nomenclature_key"
    # Для каждого elem из списка существует номенклатура с именем elem[0], группой empty и ед. измерения elem[1]
    def test_nomenclature_start_service(self):
        # подготовка
        ingredient_list = [("Картофель", "грамм"), ("Грибы", "грамм"), ("Лук", "шт"), ("Кетчуп", "грамм"), ("Майонез", "грамм"), ("Сыр", "грамм"), ("Помидор", "шт")]


        # действие

        # проверки
        assert len(self.__start_service.data[reposity.nomenclature_key()])>0
        for (key, measure) in ingredient_list:
            assert self.__start_service.data[reposity.nomenclature_key()][key].name == key
            assert self.__start_service.data[reposity.nomenclature_key()][key].nomenclature_group == self.__start_service.data[reposity.nomenclature_group_key()]["empty"]
            assert self.__start_service.data[reposity.nomenclature_key()][key].measure_unit == self.__start_service.data[reposity.measure_key()][measure]

    # Проверка генерации эталонных рецептов
    # данные доступны по ключу "recipe_key"
    # В ингредиентах рецепта существуют номенклатуры с названиями elem[0] для каждого elem из ingredient_list и количеством elem[1],
    # указанном в ед. измерения номенклатуры
    # В описании рецепта указана пошаговая инструкция приготовления в виде строк, метод recipe.pop() возвращает текущий шаг рецепта.
    def test_recipe_start_service(self):
        # подготовка
        ingredient_list = [("Картофель", 400), ("Грибы", 300), ("Лук", 1), ("Кетчуп", 200), ("Майонез", 200), ("Сыр", 200), ("Помидор", 3)]
        recipe = self.__start_service.data[reposity.recipe_key()]["default_recipe"]
        algorithm = ["Как приготовить вкустную картофельную запеканку? Подготовьте необходимые продукты. Из данного количества у меня получилось 3 большие порции.", 
                     "Картофель почистить, порезать крупными кусочками и равномерно распределить по противеню.", 
                     "Предварительно сварите грибы, порежьте средними кусочками и добавьте в запеканку.", 
                     "Крупную луковицу порезать кольцами и распределить по противеню.", 
                     "Выдавить сетку из майонеза и кетчупа, размещать тонким слоем по запеканке.", 
                     "Порежьте помидоры кружочками и разложите по запеканке.", 
                     "Обильно посыпать запеканку сверху тертым сыром.", 
                     "Поставьте запеканку в предварительно разогретую духовку до 200°C. Выпекать 60 минут, после чего дайте запеканке остыть. В горячем виде запеканка разваливается на части."]

        # действие

        # проверки
        assert len(self.__start_service.data[reposity.recipe_key()])>0
        for (key, measure) in ingredient_list:
            assert recipe.ingredients[key][0] == self.__start_service.data[reposity.nomenclature_key()][key]
            assert recipe.ingredients[key][1] == measure
        assert len(recipe.description) == 8
        for step in algorithm:
            assert step in recipe.description