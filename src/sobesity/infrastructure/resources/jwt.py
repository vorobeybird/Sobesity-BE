import re
from dataclasses import asdict
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from flask import abort, jsonify, request
from http_constants.headers import HttpHeaders

from sobesity.domain.entities import JWTEntity, UserId
from sobesity.domain.interfaces.resources import IJWTResource
from sobesity.domain.serializers.base import BadRequestSerializer

UNPROTECTED_ENDPOINTS = ("openapi\..*", "user\..*")


class JWTResource(IJWTResource):
    def __init__(self, secret):
        self.secret = secret
        self.algorithm = "HS256"

    def is_endpoint_protected(self, endpoint) -> bool:
        for endpoint_pattern in UNPROTECTED_ENDPOINTS:
            if re.match(endpoint_pattern, endpoint) is not None:
                return False
        return True

    def unauthorized_abort(self, message):
        response = jsonify(BadRequestSerializer(message=message).dict())
        response.status_code = HTTPStatus.UNAUTHORIZED
        abort(response)

    def verify_jwt(self):
        if not self.is_endpoint_protected(request.endpoint):
            return

        auth_header = request.headers.get(HttpHeaders.AUTHORIZATION)
        if auth_header is None:
            self.unauthorized_abort("No token provided")

        token = auth_header.split(" ")[1]
        try:
            self.get_user_id_from_jwt(token)
        except Exception as exc:
            pass

    def get_user_id_from_jwt(self, token) -> UserId:
        payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        jwt_entity = JWTEntity(**payload)
        return jwt_entity.sub

    def encode_jwt(self, user_id: UserId) -> str:
        jwt_entity = JWTEntity(
            sub=user_id,
            exp=datetime.now() + timedelta(minutes=5),
            iat=datetime.now(),
        )
        return jwt.encode(asdict(jwt_entity), self.secret, algorithm=self.algorithm)
