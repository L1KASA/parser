from DatabaseManager.PostgreSQLManager import PostgreSQLManager
from Parser.HttpClient import HttpClient
from Parser.ParserFactory import ParserFactory
from Parser.WebScraper import WebScraper

if __name__ == "__main__":
    # Настройка клиента и фабрики парсеров
    client = HttpClient(base_url="https://dns-shop.by")
    parser = ParserFactory.get_parser("product_detail")
    scraper = WebScraper(client, parser)

    # Выполнение парсинга
    data = scraper.scrape("/ru/product/23d64ecc97914591/6.78-smartfon-tecno-spark-10-pro-128-gb-cernyj/", output_file="result.html")

    # Вывод результата
    print(data)


    db = PostgreSQLManager(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="123123"
        )

    db.insert_data_dynamic_columns("test1", data)



    db.close_connection()