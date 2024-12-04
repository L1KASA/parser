# Класс для сохранения HTML в файл
class HtmlSaver:
    @staticmethod
    def save_to_file(html, file_name):
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(html)