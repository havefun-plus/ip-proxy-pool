from typing import Tuple

from flask import Flask, jsonify, request

from ipfeeder.db import db

app = Flask('__name__')


def validate(kwargs: dict) -> Tuple[bool, str]:
    try:
        limit = kwargs.get('limit')
        if limit:
            int(limit)
    except ValueError:
        return False, 'The type of limit must be int.'
    protocol = kwargs.get('protocol')
    if protocol and protocol not in ['http', 'https']:
        return False, 'The protocol must be http or https.'
    return True, ''


@app.route('/proxies/', methods=['GET'])
def proxies():
    args = request.args.to_dict()
    validated, msg = validate(args)
    limit = args.get('limit')
    data = db.to_dict(
        n=int(limit) if limit else None,
        protocol=args.get('protocol'),
    ) if validated else {}
    return jsonify(dict(msg=msg, data=data)), 200 if validated else 400
