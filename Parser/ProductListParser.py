from bs4 import BeautifulSoup
from Parser.ParserBase import Parser

class ProductListParser(Parser):

    def parse(self, html):

        soup = BeautifulSoup(html, 'lxml')

        # Ищем все элементы <li> с нужными классами
        product_list = (soup.find('div', class_='main__container')
                        .find('div', class_='catalog-category-products__product-list-wrapper')
                        .find('ul', class_='catalog-category-products__product-list')
                        .findAll('li', class_='catalog-category-products__product catalog-category-product'))

        # Проходим по каждому продукту и извлекаем всю информацию
        product_info = []
        for product in product_list:
            product_data = {}

            # Извлекаем название
            title_tag = product.find('a', class_='catalog-category-product__title')
            if title_tag:
                product_data['title'] = title_tag.text.strip()

            # Извлекаем ссылку на продукт
            product_data['url'] = title_tag['href'] if title_tag else None

            # Извлекаем изображение
            img_tag = product.find('img')
            if img_tag:
                product_data['image'] = img_tag['src']

            # Извлекаем цену
            price_tag = product.find('div', class_='catalog-product-purchase__current-price')
            if price_tag:
                product_data['price'] = price_tag.text.strip()

            # Извлекаем информацию о наличии товара
            availability_tag = product.find('p', class_='catalog-category-product__notification')
            if availability_tag:
                product_data['availability'] = availability_tag.text.strip()

            # Добавляем в список информацию о продукте
            product_info.append(product_data)

        return product_info

