import requests
from flask import request

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"


def login(body):
    r = requests.post(
        AUTH_URL, json={"email": body["email"], "password": body["password"]}
    )
    try:
        data = r.json()
    except Exception:
        data = {"message": r.text}
    return (data, 200) if r.status_code == 200 else ({"error": data}, r.status_code)


def verify():
    email = request.headers.get("X-Auth-Email")
    password = request.headers.get("X-Auth-Password")
    if not email or not password:
        return False, ({"error": "Unauthorized"}, 401)
    r = requests.post(AUTH_URL, json={"email": email, "password": password})
    if r.status_code == 200:
        return True, None
    return False, ({"error": "Unauthorized"}, 401)
