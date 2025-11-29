from abc import ABC
import uuid
from src.core.validator import validator, operation_exception
from functools import total_ordering


# Абстрактная модель с полем уникального кода для однозначной идентификации объектов. От AbstractModel наследуются все модели приложения.
# total_ordering, используя методы __eq__ и __lt__, сгенерирует остальные сравнения автоматически
@total_ordering
class abstact_reference(ABC):
    # Уникальный ID модели
    __unique_code:str

    # Наименование модели (50)
    __name: str = None

    def __init__(self) -> None:
        super().__init__()
        self.__unique_code = uuid.uuid4().hex

    
    # Уникальный код
    @property
    def unique_code(self) -> str:
        return self.__unique_code
    
    @unique_code.setter
    def unique_code(self, value: str):
        validator.validate(value, str)
        self.__unique_code = value.strip()
    
    # Наименование модели 
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        validator.validate(value, str, 50)
        self.__name = value.strip()

    # Перегрузка штатного варианта сравнения
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, abstact_reference):
            return False
        return self.unique_code == value.unique_code
    
    # Перегрузка штатного варианта сравнения
    def __lt__(self, value: object):
        if not isinstance(value, abstact_reference):
            return False
        return self.unique_code < value.unique_code
    
    def __contains__(self, value) -> bool:
        from src.core.common import common
        values = common.get_values(self)
        return any(value == item or (isinstance(item, (list, tuple, abstact_reference, str)) and value in item) for item in values)
    
    def __str__(self):
        return self.unique_code
    
    # Получить зависимости класса (список моделей, которые прямо или косвенно (через list, dict или другой класс) имеют поле данного класса)
    # Например для nomenclature_model вернутся [transaction_model, rest_model, recipe_model, ingredient_model]
    @classmethod
    def get_dependencies(cls) -> list:
        result = []
        all_classes = cls.get_all_subclasses(abstact_reference)
    
        for target_class in all_classes:
            if cls.check_class_annotations(target_class):
                result.append(target_class)
    
        return result
    
    @classmethod
    def get_all_subclasses(cls, base_class):
        """Рекурсивно получить все подклассы"""
        all_subclasses = []
        stack = [base_class]
        while stack:
            current = stack.pop()
            for subclass in current.__subclasses__():
                if subclass not in all_subclasses:
                    all_subclasses.append(subclass)
                    stack.append(subclass)
        return all_subclasses
    
    @classmethod
    def check_class_annotations(cls, target_class, visited=None):
        """Проверить аннотации класса на наличие текущего типа"""
        if visited is None:
            visited = set()
        # Избегаем бесконечной рекурсии при циклических зависимостях
        if target_class in visited:
            return False
        visited.add(target_class)
        # Получаем все аннотации (включая унаследованные)
        all_annotations = {}
        for base in target_class.__mro__:
            if hasattr(base, '__annotations__'):
                all_annotations.update(base.__annotations__)
        # Проверяем каждую аннотацию
        for annotation in all_annotations.values():
            if annotation is cls:
                return True
            if hasattr(annotation, '__args__'):
                for arg in annotation.__args__:
                    if arg is cls:
                        return True
                    if isinstance(arg, type) and issubclass(arg, abstact_reference):
                        return cls.check_class_annotations(arg, visited)
        return False