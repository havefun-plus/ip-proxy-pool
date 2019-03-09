from typing import Tuple

from flask import Flask, jsonify, request

from ipfeeder.db import db

app = Flask('__name__')


def validate(kwargs: dict) -> Tuple[bool, str]:
    try:
        n = kwargs.get('n')
        if n:
            int(n)
    except ValueError:
        return False, 'The type of n must be int.'
    protocol = kwargs.get('protocol')
    if protocol and protocol not in ['http', 'https']:
        return False, 'The protocol must be http or https.'
    return True, ''


@app.route('/proxies/', methods=['GET'])
def proxies():
    args = request.args.to_dict()
    validated, msg = validate(args)
    n = args.get('n')
    data = db.to_dict(
        n=int(n) if n else None,
        protocol=args.get('protocol'),
    ) if validated else {}
    return jsonify(dict(msg=msg, data=data)), 200 if validated else 400
