import json
import jwt
import re

from flask import request, abort, jsonify
from sobesity.domain.entities import UserId


unprotected_endpoints = ["openapi\..*", "user\..*"]

def is_endpoint_protected(endpoint) -> bool:
    for endpoint_pattern in unprotected_endpoints:
        if re.match(endpoint_pattern, endpoint) is not None:
            return False
    return True

def verify_jwt():
    if not is_endpoint_protected(request.endpoint):
        return

    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        response = jsonify({"message":"No token provided"})
        response.status_code = 401
        abort(response)

    token = auth_header.split(" ")[1]
    try:
        get_user_id_from_jwt(token)
    except Exception as exc:
        breakpoint()
        pass

def get_user_id_from_jwt(token)-> UserId:
    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        raise
    return payload["sub"]

def encode_jwt(user_id: UserId) -> str:
    return jwt.encode({"sub": user_id}, "secret", algorithm="HS256")
