from abc import ABC, abstractmethod


# Абстрактный интерфейс для парсеров
class Parser(ABC):
    @abstractmethod
    def parse(self, html):
        pass
