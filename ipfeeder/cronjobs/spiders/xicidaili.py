import gevent
from cronjob.apps.spider_app import SpiderJob
from lxml import etree

from ipfeeder.db import db
from ipfeeder.utils import ProxyIP


class XiciProxy(SpiderJob):
    rule = '1h'
    right_now = True
    cancelled = False

    urls = [
        'https://www.xicidaili.com/wn/',
        'https://www.xicidaili.com/nn/',
        'https://www.xicidaili.com/nt/',
        'https://www.xicidaili.com/wt/',
    ]

    def run(self) -> None:
        for url in self.urls:
            response = self.http.get(url)
            if not response.ok:
                self.logger.error(f'request failed {response.status_code}')
                continue
            html = etree.HTML(response.content)
            trs = html.xpath('//table[@id="ip_list"]//tr/td')
            for tr in trs:
                tds = tr.xpath('..//text()')
                ip = tds[2]
                port = tds[4]
                protocol = tds[12]
                proxy_ip = ProxyIP(ip, port, protocol)
                if proxy_ip.ok:
                    self.logger.info(f'got raw proxy_ip {str(proxy_ip)}')
                    db.add_raw(str(proxy_ip))
            gevent.sleep(10)
