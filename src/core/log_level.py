from enum import IntEnum, auto

class log_level(IntEnum):
    DEBUG = auto()
    INFO = auto()
    ERROR = auto()

    # Получить список всех уровней логирования
    @staticmethod
    def levels() -> list:
        return log_level.__members__.keys()