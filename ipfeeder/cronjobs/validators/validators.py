import logging
from typing import Callable, Generator
from urllib.parse import urlparse

import gevent
import requests
from cronjob.apps import BaseJob
from cronjob.settings import settings
from gevent import hub

from ipfeeder.db import db

hub.Hub.NOT_ERROR = (Exception, )

LOGGER = logging.getLogger(__name__)


def _validate(validate_urls: list, proxy_url: str, protocol: str) -> bool:
    threads = [
        gevent.spawn(
            requests.get,
            url,
            proxies={protocol: proxy_url},
            timeout=10,
        ) for url in validate_urls
    ]
    gevent.joinall(threads)
    for item in threads:
        response = item.value
        if response and response.ok:
            resp = response.json()
            origin = resp.get('origin', '').split(',')
            return origin[0] == urlparse(proxy_url).hostname
    return False


def validate(url: str) -> bool:
    try:
        if url.startswith('https'):
            return _validate(settings.VALIATE_HTTPS_URLS, url, 'https')
        elif url.startswith('http'):
            return _validate(settings.VALIATE_HTTP_URLS, url, 'http')
        else:
            return False
    except Exception as e:
        return False


class BaseValidator(BaseJob):
    rule = ''

    cancelled = True

    @property
    def get_value_func(self) -> Callable[[], Generator[str, None, None]]:
        raise NotImplementedError

    def run(self):
        for ip in self.get_value_func():
            if ip and validate(ip):
                self.logger.info(f'pass validator: {ip}')
                db.add_validated(ip)


class RawValidator(BaseValidator):
    rule = '2m'
    right_now = True

    @property
    def get_value_func(self) -> Callable[[], Generator[str, None, None]]:
        return getattr(db, 'raw_pop_iter')


class HttpValidator(BaseValidator):
    rule = '20m'
    right_now = False

    @property
    def get_value_func(self) -> Callable[[], Generator[str, None, None]]:
        return getattr(db, 'http_pop_iter')


class HttpsValidator(BaseJob):
    rule = '20m'
    right_now = False

    @property
    def get_value_func(self) -> Callable[[], Generator[str, None, None]]:
        return getattr(db, 'https_pop_iter')
