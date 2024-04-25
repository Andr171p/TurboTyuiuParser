import random
from Proxies.auth_data import login, password, ip_list


class Proxy:
    def __init__(self):
        self.login = login
        self.password = password
        self.proxies = ip_list

    def random_proxy(self):
        return random.choice(self.proxies)

    def get_proxy(self):
        proxy = {
            "proxy": {
                "https": f"https://{self.login}:{self.password}@{self.random_proxy()}"
            }
        }
        return proxy