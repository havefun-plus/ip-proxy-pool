from flask import Flask, jsonify

from ipfeeder.db import db

app = Flask('__name__')


@app.route('/', methods=['GET'])
def proxies():
    result = db.to_dict()
    return jsonify(result)
