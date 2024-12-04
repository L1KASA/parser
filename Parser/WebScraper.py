# Главный класс для выполнения всей задачи
from Parser.HttpClient import HttpClient
from Parser.HttpSaver import HtmlSaver
from Parser.ParserBase import Parser


class WebScraper:
    def __init__(self, client: HttpClient, parser: Parser):
        self.client = client
        self.parser = parser

    def scrape(self, endpoint, output_file=None):
        html = self.client.get(endpoint)
        if output_file:
            HtmlSaver.save_to_file(html, output_file)
        return self.parser.parse(html)