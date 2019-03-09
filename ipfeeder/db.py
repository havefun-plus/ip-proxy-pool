from typing import Generator

from redis import StrictRedis

from cronjob.settings import settings

RAW_IPS = 'raw_proxy_ip'
VALIDATED_HTTP = 'valicated_http_ip'
VALIDATED_HTTPS = 'valicated_https_ip'


class DB:
    def __init__(self, **kwargs) -> None:
        self.conn = StrictRedis(**kwargs)

    @classmethod
    def from_settings(cls) -> 'DB':
        return cls(**settings.REDIS_SETTINGS)

    def _push_set(self, list_name: str, *values: str) -> None:
        lvalues = list(filter(None, values))
        if lvalues:
            self.conn.sadd(list_name, *lvalues)

    def add_raw(self, *values: str) -> None:
        self._push_set(RAW_IPS, *values)

    def add_http(self, *values: str) -> None:
        self._push_set(VALIDATED_HTTP, *values)

    def add_https(self, *values: str) -> None:
        self._push_set(VALIDATED_HTTPS, *values)

    def add_validated(self, *values: str) -> None:
        for ip in values:
            if ip.startswith('https'):
                self.add_https(ip)
            elif ip.startswith('http'):
                self.add_http(ip)
            else:
                pass

    def _pop_iter(self, ip_type: str) -> Generator[str, None, None]:
        bip = self.conn.spop(ip_type)
        while bip:
            yield bip and bip.decode()
            bip = self.conn.spop(ip_type)

    def _iter(self, ip_type: str) -> Generator[str, None, None]:
        for bip in self.conn.sscan_iter(ip_type):
            self.conn.srem(ip_type, bip)
            ip = bip and bip.decode()
            yield ip

    def raw_pop_iter(self):
        yield from self._pop_iter(RAW_IPS)

    def http_pop_iter(self):
        yield from self._iter(VALIDATED_HTTP)

    def https_pop_iter(self):
        yield from self._iter(VALIDATED_HTTPS)

    def _get_all_http(self) -> list:
        result = self.conn.smembers(VALIDATED_HTTP)
        return list(map(lambda x: x.decode(), result))

    def _get_all_https(self) -> list:
        result = self.conn.smembers(VALIDATED_HTTPS)
        return list(map(lambda x: x.decode(), result))

    def to_dict(self) -> dict:
        return dict(
            http=self._get_all_http(),
            https=self._get_all_https(),
        )


db = DB.from_settings()
