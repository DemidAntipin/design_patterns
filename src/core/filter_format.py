
"""Форматы сравнения"""
class filter_format:
    @staticmethod
    def equals() -> str:
        return "=="
    
    @staticmethod
    def like() -> str:
        return "like"

    @staticmethod
    def less() -> str:
        return "<"
    
    @staticmethod
    def greater() -> str:
        return ">"
    
    @staticmethod
    def not_less() -> str:
        return ">="
    
    @staticmethod
    def not_greater() -> str:
        return "<="


    """Получить все доступные типы фильтров"""
    @classmethod
    def get_types(cls) -> list[str]:
        return [method() for method in cls.__dict__.values() 
                if isinstance(method, staticmethod) 
                and callable(method)]