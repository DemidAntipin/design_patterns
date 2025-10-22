# Форматы ответов
class response_format:

    @staticmethod
    def csv_format() -> str:
        return "csv"
    
    @staticmethod
    def xml_format() -> str:
        return "xml"
    
    @staticmethod
    def json_format() -> str:
        return "json"
    
    @staticmethod
    def markdown_format() -> str:
        return "markdown"
    
    """
    Получить список всех форматов
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(response_format) if
                    callable(getattr(response_format, method)) and method.endswith('_format')]
        for method in methods:
            key = getattr(response_format, method)()
            result.append(key)

        return result