import random
import socket
from typing import Union


class ProxyIP:
    def __init__(self,
                 ip: str = '',
                 port: Union[str, int] = '',
                 protocol: str = '',
                 ip_port: str = '') -> None:
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
            return all([
                self._validate_ip(),
                self._validate_port(),
                self._validate_protocol()
            ])
        except Exception:
            return False

    def _validate_protocol(self) -> bool:
        return bool(self.protocol) and self.protocol in ['http', 'https']

    def _validate_ip(self) -> bool:
        try:
            socket.inet_aton(self.ip)
            return True
        except socket.error:
            return False

    def _validate_port(self) -> bool:
        return bool(self.port) and 0 <= int(self.port) <= 65535

    def __str__(self) -> str:
        return f'{self.protocol}://{self.ip}:{self.port}'


def shuffle_pages(start: int, end: int) -> list:
    pages = list(range(start, end))
    random.shuffle(pages)
    return pages


def decode_port(raw: str) -> int:
    flag = 'ABCDEFGHIZ'
    parsed = ''.join([str(flag.index(x)) for x in raw])
    return int(parsed) >> 3
