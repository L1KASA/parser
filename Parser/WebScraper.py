from Parser.HttpClient.HttpClient import HttpClient
from Parser.ParserBase import Parser


class WebScraper:
    def __init__(self, http_client: HttpClient, parser: Parser):
        self.client = http_client
        self.parser = parser

    def scrape(self, url):
        html = self.client.get(url)
        return self.parser.parse(html)
