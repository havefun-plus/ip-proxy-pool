from cronjob.settings import settings
from redis import StrictRedis

RAW_IPS = 'raw_proxy_ip'
VALIDATED_HTTP = 'valicated_http_ip'
VALIDATED_HTTPS = 'valicated_https_ip'


class DB:
    def __init__(self, **kwargs):
        self.conn = StrictRedis(**kwargs)

    @classmethod
    def from_settings(cls):
        return cls(**settings.REDIS_SETTINGS)

    def _push_set(self, list_name, *value):
        self.conn.sadd(list_name, *value)

    def add_raw(self, *values):
        self._push_set(RAW_IPS, *values)

    def add_http(self, *values):
        self._push_set(VALIDATED_HTTP, *values)

    def add_https(self, *values):
        self._push_set(VALIDATED_HTTPS, *values)

    def add_validated(self, *values):
        for ip in values:
            if ip.startswith('https'):
                self.add_https(ip)
            elif ip.startswith('http'):
                self.add_http(ip)
            else:
                pass

    def _iter(self, ip_type):
        for ip in self.conn.sscan_iter(ip_type):
            yield ip.decode()
            self.conn.srem(ip_type, ip)

    def raw_iter(self):
        yield from self._iter(RAW_IPS)

    def http_iter(self):
        yield from self._iter(VALIDATED_HTTP)

    def https_iter(self):
        yield from self._iter(VALIDATED_HTTPS)

    def _get_all_http(self):
        result = self.conn.smembers(VALIDATED_HTTP)
        return list(map(lambda x: x.decode(), result))

    def _get_all_https(self):
        result =  self.conn.smembers(VALIDATED_HTTPS)
        return list(map(lambda x: x.decode(), result))

    def to_dict(self):
        return dict(
            http=self._get_all_http(),
            https=self._get_all_https(),
        )


db = DB.from_settings()
