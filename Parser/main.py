from Parser.HttpClient.HttpClient import HttpClient

from Parser.ProductDetailParser import ProductDetailParser
from Parser.ProductListParser import ProductListParser
from Parser.WebScraper import WebScraper

if __name__ == "__main__":
    # Настройка клиента и фабрики парсеров
    #client = HttpClient(base_url="https://dns-shop.by/ru/product/cb714a0dc797ed20/34-monitor-titan-army-c34chr-cernyj/")
    #parser = ParserFactory.get_parser("product_detail")
    #scraper = WebScraper(client, parser)

    # Выполнение парсинга
    #data = scraper.scrape("/ru/product/cb714a0dc797ed20/34-monitor-titan-army-c34chr-cernyj/", output_file="result.html")
    #data = scraper.scrape("/ru/category/fa58a48980ca51bf/detskie-casy/?page=2", output_file="result.html")
    # Вывод результата
    #print(data)
    #for item in data:
    #    scraper = WebScraper(client, parser)
    #    print(data)
    #    for item in data:
    #        print(item['url'].replace("https://dns-shop.by", ""))
    # for i in range(0, 16):
    #
    #     print(i)
    #     client = HttpClient(base_url="https://dns-shop.by")
    #     parser = ParserFactory.get_parser("product_detail")
    #     scraper = WebScraper(client, parser)
    #     data = scraper.scrape(f"/ru/category/17a8943716404e77/monitory/?page={i}",
    #                           output_file="result.html")
    #     print(data)
    #     for item in data:
    #         parser = ParserFactory.get_parser("product_detail")
    #         #scraper = WebScraper(client, parser)
    #         scraper = WebScraper(client, parser)
    #         # print(scraper.scrape(item['url'].replace("https://dns-shop.by", ""), output_file="result.html"))
    #     # Вывод результата
    #     #print(data)

    base_url = "https://dns-shop.by/ru/category/17a8943716404e77/monitory/"
    client = HttpClient()
    list_parser = ProductListParser()
    detail_parser = ProductDetailParser()

    # Парсинг списка продуктов
    list_scraper = WebScraper(client, list_parser)
    product_list = list_scraper.scrape(base_url)

    print("Список продуктов:")
    for product in product_list:
        print(product)

    # Парсинг деталей продукта
    if product_list:
        first_product = product_list[0]
        print("\nДетали первого продукта:")
        detail_scraper = WebScraper(client, detail_parser)
        details = detail_scraper.scrape(first_product['url'])
        print(details)


#    db = PostgreSQLManager(
#            host="localhost",
#            port="5432",
#            database="postgres",
#            user="postgres",
#            password="123123"
#        )
#
#    db.create_table('products',
#                    )
#
#
#    db.close_connection()