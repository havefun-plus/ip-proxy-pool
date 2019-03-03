import random
import socket
from typing import TypeVar


class ProxyIP:
    def __init__(self,
                 ip: str = '',
                 port: TypeVar('Port', str, int) = '',
                 protocol: str = '',
                 ip_port: str = ''):
        self.ip = ip
        self.port = port
        self.protocol = protocol and protocol.lower()
        if ip_port:
            try:
                self.ip, self.port = ip_port.split(':')
            except ValueError:
                pass

    @property
    def ok(self) -> bool:
        try:
            if all([
                    self._validate_ip(),
                    self._validate_port(),
                    self._validate_protocol()
            ]):
                return True
            return False
        except Exception:
            return False

    def _validate_protocol(self) -> bool:
        if not self.protocol or self.protocol not in ['http', 'https']:
            return False
        return True

    def _validate_ip(self) -> bool:
        try:
            socket.inet_aton(self.ip)
            return True
        except socket.error:
            return False

    def _validate_port(self) -> bool:
        if not self.port or not 0 <= int(self.port) <= 65535:
            return False
        return True

    def __str__(self):
        return f'{self.protocol}://{self.ip}:{self.port}'


def shuffle_pages(start: int, end: int) -> list:
    pages = list(range(start, end))
    random.shuffle(pages)
    return pages


def decode_port(raw: str) -> int:
    flag = 'ABCDEFGHIZ'
    parsed = ''.join([str(flag.index(x)) for x in raw])
    return int(parsed) >> 3
