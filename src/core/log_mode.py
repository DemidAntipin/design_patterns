from enum import IntEnum, auto

class log_mode(IntEnum):
    CONSOLE = auto()
    FILE = auto()
    BOTH = auto()

    # Получить список всех режимов логирования
    @staticmethod
    def mods() -> list:
        return log_mode.__members__.keys()