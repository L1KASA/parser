from Parser import ProductListParser, ProductDetailParser
from Parser.HttpClient import HttpClient
import aiohttp
import asyncio


class ProductAutomation:
    def __init__(self, http_client: HttpClient, list_parser: ProductListParser, detail_parser: ProductDetailParser):
        """
        Внедрение зависимостей через интерфейсы.
        :param http_client: Интерфейс для выполнения HTTP-запросов.
        :param list_parser: Интерфейс для парсинга страниц с товарами.
        :param detail_parser: Интерфейс для парсинга конкретной страницы с товаром.
        """
        self.http_client = http_client
        self.list_parser = list_parser
        self.detail_parser = detail_parser

    def fetch_and_parse_product_list(self, endpoint):
        """Загружает и парсит страницу со списком товаров."""
        html = self.http_client.get(endpoint)
        return self.list_parser.parse(html)

    def fetch_and_parse_product_details(self, product_url):
        """Загружает и парсит страницу с товаром."""
        html = self.http_client.get(product_url)
        return self.detail_parser.parse(html)

    def parse(self, list_endpoint):
        """Основной метод для обработки товаров."""
        product_list = self.fetch_and_parse_product_list(list_endpoint)
        detailed_products = []

        for product in product_list:
            if 'url' in product and product['url']:
                try:
                    details = self.fetch_and_parse_product_details(product['url'])
                    product.update(details)
                    detailed_products.append(product)
                except Exception as e:
                    print(f"Error fetching details for {product['url']}: {e}")

        return detailed_products


# Использование
if __name__ == "__main__":
    from Parser.HttpClient.HttpClient import HttpClient
    from Parser.ProductDetailParser import ProductDetailParser
    from Parser.ProductListParser import ProductListParser

    BASE_URL = "https://dns-shop.by/ru/category/17a8a01d16404e77/smartfony/?page=2"

    http_client = HttpClient(BASE_URL)
    list_parser = ProductListParser()
    detail_parser = ProductDetailParser()

    automation = ProductAutomation(http_client, list_parser, detail_parser)
    all_products = automation.parse(BASE_URL)

    for product in all_products:
        print(product)
