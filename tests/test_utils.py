from ipfeeder.utils import ProxyIP, decode_port


def test_ProxyIP():
    cases = [
        (dict(ip="127.0.0.1", port="80", protocol='http'), True),
        (dict(ip="127.0.0.1", port="80", protocol='https'), True),
        (dict(ip="127.0.0.1", port="80", protocol=None), False),
        (dict(ip="127.0.0.1", port="80", protocol="whatever"), False),
        (dict(ip="827.0.0.1", port="80", protocol='https'), False),
        (dict(ip="xxx.xx.xx.1", port="80", protocol='https'), False),
        (dict(ip="whatever", port="80", protocol='https'), False),
        (dict(ip=None, port="80", protocol='https'), False),
        (dict(ip="127.0.0.1", port=80, protocol='https'), True),
        (dict(ip="127.0.0.1", port=65536, protocol='https'), False),
        (dict(ip="127.0.0.1", port="80", protocol='https'), True),
        (dict(ip="127.0.0.1", port=None, protocol='https'), False),
        (dict(ip_port="127.0.0.1:8080", protocol='https'), True),
        (dict(ip_port="whatever:8080", protocol='https'), False),
        (dict(ip_port="127.0.0.1:888888", protocol='https'), False),
        (dict(ip_port="127.0.0.1", protocol='https'), False),
    ]
    for params, result in cases:
        assert ProxyIP(**params).ok == result


def test_decode_post():
    cases = [
        ('GEGEA', 8080),
        ('CEABDG', 30017),
        ('DFGBZC', 44524),
    ]
    for arg, result in cases:
        assert decode_port(arg) == result
