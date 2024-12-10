from typing import Protocol


class Parser(Protocol):
    def parse(self, html: str) -> dict[str, any]:
        """ Парсит HTML-файл и возвращает словарь данных. """
        pass
