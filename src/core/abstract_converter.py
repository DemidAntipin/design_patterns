from abc import ABC, abstractmethod


"""
Абстрактный класс для преобразования данных
"""
class abstract_coverter(ABC):

    @abstractmethod
    def convert(self, obj) -> dict:
        pass