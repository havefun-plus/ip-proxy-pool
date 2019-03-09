import random

import gevent

from cronjob.apps.spider_app import SpiderJob
from ipfeeder.db import db
from ipfeeder.utils import ProxyIP
from lxml import etree


class IphaiProxy(SpiderJob):
    rule = '15,45 * * * *'  #  每小时的第十五和第四十五分钟执行一次
    right_now = False  # 程序启动时候不立即执行
    cancelled = False

    urls = [
        'http://www.iphai.com/free/ng',
        'http://www.iphai.com/free/np',
        'http://www.iphai.com/free/wg',
        'http://www.iphai.com/free/wp',
    ]

    def run(self) -> None:
        for url in self.urls:
            response = self.http.get(url)
            if not response.ok:
                self.logger.error(f'request failed {response.status_code}')
                continue
            html = etree.HTML(response.content)
            trs = html.xpath('..//table//tr')
            for tr in trs:
                tds = tr.xpath('./td/text()')
                if len(tds) < 6:
                    continue
                ip = tds[0].strip()
                port = tds[1].strip()
                protocols = tds[3].strip().split(',')
                for protocol in protocols:
                    proxy_ip = ProxyIP(ip, port, protocol)
                    if proxy_ip.ok:
                        self.logger.info(f'got raw proxy_ip {str(proxy_ip)}')
                        db.add_raw(str(proxy_ip))
            gevent.sleep(random.randint(11, 23))
