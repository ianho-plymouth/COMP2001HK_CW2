from flask import jsonify


def ping():
    return {"status": "ok"}, 200
