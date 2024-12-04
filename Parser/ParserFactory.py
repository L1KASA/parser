# Фабрика парсеров
from Parser.ProductDetailParser import ProductDetailParser
from Parser.ProductListParser import ProductListParser


class ParserFactory:
    @staticmethod
    def get_parser(site_name):
        if site_name == "product_detail":
            return ProductDetailParser()
        if site_name == "product_list":
            return ProductListParser()
        else:
            raise ValueError(f"Parser for {site_name} not implemented")