import traceback

import gevent
from cronjob.apps.spider_app import SpiderJob
from lxml import etree

from ipfeeder.db import db
from ipfeeder.utils import ProxyIP, decode_port


class GoubanjiaProxy(SpiderJob):
    rule = '1h'
    right_now = True
    cancelled = False

    urls = ['http://www.goubanjia.com/']

    def run(self):
        for url in self.urls:
            response = self.http.get(url)
            if not response.ok:
                continue
            html = etree.HTML(response.content)
            trs = html.xpath('..//table[@class="table table-hover"]//tr')
            xpath_str = """./td[@class="ip"]//*[not(contains(@style, 'display: none'))
                                                        and not(contains(@style, 'display:none'))
                                                        and not(contains(@class, 'port'))
                                                        ]/text()
                                                        """
            for tr in trs:
                try:
                    tds = tr.xpath('./td')
                    if len(tds) < 5:
                        continue
                    protocol = tds[2].xpath('.//text()')[0]
                    ip = ''.join(tr.xpath(xpath_str))
                    raw_port = tr.xpath(
                        './/span[contains(@class, "port")]/@class')[0].split(
                            ' ')[1]
                    port = decode_port(raw_port)
                    proxy_ip = ProxyIP(ip, port, protocol)
                    if proxy_ip.ok:
                        self.logger.info(
                            f'goubanjia proxy got raw proxy_ip {str(proxy_ip)}')
                        db.add_raw(str(proxy_ip))
                except Exception:
                    self.logger.error(f'error in goubanjia {url}')
                    traceback.print_exc()
            gevent.sleep(10)
