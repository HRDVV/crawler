"""
 Created by hanruida on 2019-03-26
"""
import requests
from fake_useragent import UserAgent
from scrapy.selector import Selector
from gps.gps.utils.db import Db
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class ProxyIp:
    start_url = "https://www.xicidaili.com/nn/"

    def __init__(self):
        self.ua = UserAgent(path="../useragent.json")

    def collect_ip(self):
        with Db() as db:
            # for i in range(1, 3635):
            headers = {
                "User-Agent": self.ua.random
            }
            # proxies = {
            #     "http": "http://60.173.203.83:47300",
            #     # "https": "https://223.241.117.85:8010"
            # }
            re = requests.get(url=self.start_url, headers=headers)
            if re.status_code == 200:
                selector = Selector(re)
                ip_list = selector.css("#ip_list .odd")
                if ip_list:
                    for ip_info in ip_list:
                        ip = ip_info.css(".odd td::text").extract()[0]
                        port = ip_info.css(".odd td::text").extract()[1]
                        req_type = ip_info.css(".odd td::text").extract()[5]
                        sql = "INSERT INTO `proxy` (ip, port, type) VALUES ('{0}', '{1}', '{2}')".format(ip, port, req_type)
                        db.operator(sql)
            else:
                print("请求失败")

ProxyIp().collect_ip()
