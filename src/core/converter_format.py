# Форматы конвертеров
class converter_format:

    @staticmethod
    def basic_format() -> str:
        return "basic"
    
    @staticmethod
    def datetime_format() -> str:
        return "datetime"
    
    @staticmethod
    def reference_format() -> str:
        return "reference"
    
    @staticmethod
    def list_format() -> str:
        return "list"
    
    @staticmethod
    def dict_format() -> str:
        return "dict"

    """
    Получить список всех форматов
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(converter_format) if
                    callable(getattr(converter_format, method)) and method.endswith('_format')]
        for method in methods:
            key = getattr(converter_format, method)()
            result.append(key)

        return result