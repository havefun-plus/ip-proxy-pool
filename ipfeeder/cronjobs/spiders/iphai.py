import random

import gevent
from cronjob.apps.spider_app import SpiderJob
from lxml import etree

from ipfeeder.db import db
from ipfeeder.utils import ProxyIP


class IphaiProxy(SpiderJob):
    rule = '1h'
    right_now = True
    cancelled = False

    urls = [
        'http://www.iphai.com/free/ng',
        'http://www.iphai.com/free/np',
        'http://www.iphai.com/free/wg',
        'http://www.iphai.com/free/wp',
    ]

    def run(self):
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
                        self.logger.info(
                            f'iphai proxy got raw proxy_ip {str(proxy_ip)}')
                        db.add_raw(str(proxy_ip))
            gevent.sleep(random.randint(11, 23))
