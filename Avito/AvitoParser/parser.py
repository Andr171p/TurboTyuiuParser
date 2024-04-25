# html code parse:
from bs4 import BeautifulSoup
# fake web-driver:
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# fake User-agent:
from fake_useragent import UserAgent
# AVITO url:
from Avito.AvitoParser.config import AVITO_URL
# tools:
import time
import os
# critical info of ads:
from Avito.AvitoParser.utils.avito import Critical, Additional
# drop None values in data-ads:
from Avito.AvitoParser.utils.preprocessing_data import drop_none
# 2D array --> csv file:
from Avito.AvitoParser.utils.preprocessing_data import save_to_csv
# fake proxy:
from Proxies.proxy import Proxy


class HTMLLoader:
    def __init__(self, region, driver_version="122.0.6261.95"):
        # avito.ru page:
        self.url = f"https://www.avito.ru/{region}/zemelnye_uchastki/prodam/promnaznacheniya-ASgBAgICAkSWA9oQpgjqVQ?p="
        # Chrome driver options:
        self.options = webdriver.ChromeOptions()
        # fake User-agent:
        self.user_agent = UserAgent().random
        # add options user-agent:
        self.options.add_argument(f"user-agent={self.user_agent}")
        # Chrome web-driver:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version=driver_version).install()),
                                       options=self.options, seleniumwire_options=Proxy().get_proxy())
        # init current links array:
        self.current_links = []
        # pages number:
        self.pages_number = 100

    def get_requests(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(10)

    def parse_links(self, page_iterator):
        all_links = []
        for page in range(1, 6):
            self.get_requests(f"{AVITO_URL}{page_iterator}")
            time.sleep(10)
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            html_content = soup.find_all("a", attrs={"data-marker": "item-title"})
            links = [f"https://www.avito.ru" + link["href"] for link in html_content]
            all_links.append(links)

        with open(r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\AvitoParser\URL\all_url.txt", "w",
                  encoding="utf-8") as file:
            for link in all_links:
                for i in range(len(link)):
                    file.write(link[i] + "\n")

    def html_loader(self):
        with open(r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\AvitoParser\URL\all_url.txt",
                  encoding="utf-8") as file:
            for url in file:
                self.current_links.append(url.strip())

        ads_number = 1
        try:
            for link in range(len(self.current_links)):
                self.get_requests(self.current_links[link])
                time.sleep(10)
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                with open(
                        fr"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\AvitoParser\avito_html\ads_{ads_number}.html",
                        "w", encoding="utf-8"
                ) as file:
                    file.write(str(soup.prettify()))
                ads_number += 1
        except Exception as _ex:
            print(f"[WARNING] : {_ex}")
        finally:
            self.driver.close()
            self.driver.quit()


class AvitoParser:
    def __init__(self):
        self.data = []

    # this method parse html files in current directory:
    def get_parse(self):
            directory = r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\AvitoParser\avito_html"
            iterator = 0
            for filename in os.listdir(directory):
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "html.parser")
                    # critical characterize:
                    critical = Critical(soup=soup)
                    ads = critical.parse_html(iterator=iterator)
                    iterator += 1
                    # additional characterize:
                    additional = Additional(soup=soup)
                    ads_additional = additional.parse_html()
                    print(50 * "=" + "ADS SAVED" + 50 * "=")
                    print(54 * "=" + str(iterator) + 54 * "=")

                self.data.append([*ads, *ads_additional])

            self.data = drop_none(data=self.data)

            csv_path = r"C:\Users\andre\TyuiuProjectParser\TurboTyuiuParser\Avito\Data\ads.csv"
            save_to_csv(data=self.data,
                        file_path=csv_path)

            return self.data


parser = AvitoParser()
data = parser.get_parse()
print(data)