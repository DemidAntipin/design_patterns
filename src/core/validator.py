from types import NoneType
from datetime import datetime

"""
Исключение при проверки аргумента
"""   
class argument_exception(Exception):
    pass     
    
"""
Исключение при выполнении бизнес операции
"""  
class operation_exception(Exception):
    pass    
    

"""
Набор проверок данных
"""
class validator:

    @staticmethod
    def validate( value, type_, len_= None, allow_null = False):
        """
            Валидация аргумента по типу и длине
        Args:
            value (any): Аргумент
            type_ (object): Ожидаемый тип
            len_ (int): Максимальная длина
            allow_null (bool): Пропустить пустой аргумент
        Raises:
            argument_exception: Некорректный тип
            argument_exception: Нулевая длина
            argument_exception: Некорректная длина аргумента
        Returns:
            True или Exception
        """
        if value is None:
            if allow_null or (isinstance(type_, (list, tuple)) and NoneType in type_) or (type_ is NoneType):
                return True
            else:
                raise argument_exception("Пустой аргумент")

        # Проверка типа
        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {value.__class__.__name__}")

        # Проверка аргумента
        if len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            raise argument_exception("Некорректная длина аргумента")

        return True
    
    @staticmethod
    def validate_id(value, array):
        """
            Валидация наличия элемента в array с id = значению аргумента
        Args:
            value (str): Аргумент
            array (list):
        Raises:
            argument_exception: Элемент не существует
        Returns:
            True или Exception
        """
        available_values = [item.unique_code for item in array]
        if value in available_values:
            return True
        else:
            raise argument_exception(f"Элемент с id {value} не существует")
        
    @staticmethod
    def validate_period(start_date:str, end_date:str):
        try:
            validator.validate(start_date, str)
            validator.validate(end_date, str)
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise argument_exception("Дата должна быть строкой в формате yyyy-mm-dd")
        if start_date > end_date:
            raise argument_exception(f"start_date не может быть позжё end_date")
        return (start_date, end_date)
