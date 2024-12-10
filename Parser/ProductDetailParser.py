import re
from bs4 import BeautifulSoup

class ProductDetailParser:
    def parse(self, html) -> dict[str, any]:
        soup = BeautifulSoup(html, 'lxml')

        # Извлечение цены
        price_tag = (
            soup.find('div', class_='main__container')
            .find('div', class_='product-card')
            .find('section', class_='product-card__main-content')
            .find('div', class_='product-card-purchase__price')
            .find('div')
        )
        price = price_tag.get_text(strip=True) if price_tag else "Цена не найдена"
        price = float(price.replace(' BYN', '').replace(',', '.').replace(' ', ''))


        product_data = {"price": price}

        # Извлечение характеристик
        specs_wrappers = (
            soup.find('div', class_='main__container')
            .find('div', class_='product-card')
            .find('div', attrs={'js--product-card-tabs-contents': True})
            .findAll('div', class_='product-card-characteristics__specs-wrapper')
        )

        for wrapper in specs_wrappers:
            if wrapper:
                key = wrapper.find('div', class_='product-card-characteristics__spec-title').get_text(strip=True)
                value = wrapper.find('div', class_='product-card-characteristics__spec-values').get_text(strip=True)
                product_data[key] = value

        cleaned_product_data = {re.sub(r'[ \-]', '_', re.sub(r'[\[\](){},]', '', key)): value for key, value in product_data.items()}

        # Извлечение изображений
        images_tag = (
            soup.find('div', class_='main__container')
            .find('div', class_='product-card')
            .find('section', class_='product-card__main-content')
            .findAll('li', attrs={'js--product-card-slider__slide': True})
        )

        # Добавление изображений в словарь
        images = [text.find('img').get('src') for text in images_tag if text.find('img')]
        #product_data["images"] = images

        return cleaned_product_data
