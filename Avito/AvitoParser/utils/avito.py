from Avito.AvitoParser.utils.preprocessing_data import replace_symbol
from Avito.AvitoParser.utils.tools import DatetimeConverter
from datetime import date
import re


class Critical:
    def __init__(self, soup):
        self.soup = soup
        self.elements = []

    # this function return info of sector --> str:
    def get_info(self):
        content = self.soup.find("h1", attrs={"data-marker": "item-view/title-info"})
        info = replace_symbol(content.text)[14:-13]
        self.elements.append(info)

    # this function return price per m^2 of sector --> int:
    def get_price(self):
        content = self.soup.find("div", attrs={"class": "style-item-price-sub-price-_5RUD"})
        price = content.text.replace("\n", "").replace("\xa0", " ").replace(" ", "")[:-8]
        self.elements.append(int(price))

    # this function return area of sector --> float:
    def get_area(self):
        try:
            content = self.soup.find("li", attrs={"class": "params-paramsList__item-_2Y2O"})
            area = replace_symbol(content.text).replace(" ", "")[8:-5]
            self.elements.append(float(area))
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")
            self.elements.append(None)

    # this function return location of sector --> str:
    def get_location(self):
        try:
            content = self.soup.find("span", attrs={"class": "style-item-address__string-wt61A"})
            location = replace_symbol(content.text)[17:-16]
            self.elements.append(location)
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")
            self.elements.append(None)

    # this function return datetime of ads --> datetime object:
    def get_datetime(self):
        converter = DatetimeConverter()
        try:
            content = self.soup.find("span", attrs={"data-marker": "item-view/item-date"})
            date_time = f"· {replace_symbol(content.text)[50:-15]}"
            self.elements.append(converter.current_date(date_time))
        except Exception as _ex:
            print(f"[WARNING] : {_ex}")
            self.elements.append(date.today())

    def get_url(self, iterator):
        with open(r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\AvitoParser\URL\all_url.txt",
                  encoding="utf-8") as file:
            urls = file.read()
        array = [url for url in urls.split("\n")]

        self.elements.append(array[iterator])

        self.elements.append(iterator)

        if "avito" in array[iterator]:
            self.elements.append("avito")
        else:
            self.elements.append("cian")

    def parse_html(self, iterator):
        self.get_info()
        self.get_price()
        self.get_area()
        self.get_location()
        self.get_datetime()
        self.get_url(iterator=iterator)

        return self.elements


class Additional:
    def __init__(self, soup):
        self.soup = soup
        self.elements = []

    def get_image_link(self):
        try:
            # links_collection = set()
            content = self.soup.find("div", attrs={"data-marker": "image-frame/image-wrapper"})
            for tag in content.find_all():
                # if "data-url" in tag.attrs:
                    # links_collection.add(tag["data-url"])
                if "src" in tag.attrs:
                    self.elements.append(str(tag["src"]))

            # self.elements.append(links_collection)

            return self.elements
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")

    def get_cadastral_number(self):
        try:
            content = self.soup.find("div", attrs={"data-marker": "item-view/item-description"})
            description = replace_symbol(content.text)

            def check_number(text):
                pattern = r'\b\d{2}:\d{2}:\d{7}:\d{1,3}\b'
                match = re.search(pattern, text)
                if match:
                    return match.group()
                else:
                    return "Не указан"

            cadastral_number = check_number(text=description)
            self.elements.append(cadastral_number)
            return description
        except Exception as _ex:
            print(f"Не указан кадастровый номер: {_ex}")

    def parse_html(self):
        self.get_cadastral_number()
        self.get_image_link()

        return self.elements

