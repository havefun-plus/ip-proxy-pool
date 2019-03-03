import random


class ProxyIP:
    def __init__(self, ip='', port='', protocol='', ip_port=''):
        self.ip = ip
        self.port = port
        self.protocol = protocol and protocol.lower()
        if ip_port:
            self.ip, self.port = ip_port.split(':')

    @property
    def ok(self)->bool:
        if not self.protocol or self.protocol not in ['http', 'https']:
            return False
        if not self.ip or not self.port:
            return False
        return True

    def __str__(self):
        return f'{self.protocol}://{self.ip}:{self.port}'


def shuffle_pages(start: int, end: int)->list:
    pages = list(range(start, end))
    random.shuffle(pages)
    return pages


def decode_port(raw: str) -> int:
    flag = 'ABCDEFGHIZ'
    parsed = ''.join([str(flag.index(x)) for x in raw])
    return int(parsed) >> 3
