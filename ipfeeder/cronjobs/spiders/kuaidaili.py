import gevent
from cronjob.apps.spider_app import SpiderJob
from lxml import etree

from ipfeeder.db import db
from ipfeeder.utils import ProxyIP


class KuaiProxy(SpiderJob):
    rule = '30m'
    right_now = True
    cancelled = False

    urls = [
        'https://www.kuaidaili.com/free/inha/',
        'https://www.kuaidaili.com/free/intr/'
    ]

    def run(self):
        for url in self.urls:
            response = self.http.get(url)
            if not response.ok:
                self.logger.error(f'request failed {response.status_code}')
                continue
            html = etree.HTML(response.content)
            trs = html.xpath('.//table//tr')
            for tr in trs:
                tds = tr.xpath('./td/text()')
                if len(tds) < 4:
                    continue
                ip = tds[0]
                port = tds[1]
                protocol = tds[3]
                proxy_ip = ProxyIP(ip, port, protocol)
                if proxy_ip.ok:
                    self.logger.info(f'kuai daili got raw proxy_ip {str(proxy_ip)}')
                    db.add_raw(str(proxy_ip))
            gevent.sleep(10)
