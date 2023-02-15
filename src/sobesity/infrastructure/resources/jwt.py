import re
from dataclasses import asdict
from datetime import datetime, timedelta
from http import HTTPStatus

import jwt
from flask import abort, jsonify, request
from http_constants.headers import HttpHeaders

from sobesity.domain.entities import JWTEntity, JWTToken, UserId
from sobesity.domain.exceptions import CorruptedToken, ExpiredToken
from sobesity.domain.interfaces.resources import IJWTResource
from sobesity.domain.serializers.base import BadRequestSerializer

UNPROTECTED_ENDPOINTS = ("openapi\..*", "user\..*")
PROTECTED_ENDPOINTS = ("user\.current_user", )


class JWTResource(IJWTResource):
    def __init__(self, secret, access_token_duration_days, refresh_token_duration_days):
        self.secret = secret
        self.access_token_duration_days = access_token_duration_days
        self.refresh_token_duration_days = refresh_token_duration_days
        self.algorithm = "HS256"

    def is_endpoint_protected(self, endpoint: str) -> bool:
        if endpoint is None:
            raise ValueError(f"Endpoint can't be None. {request}")
        for endpoint_pattern in PROTECTED_ENDPOINTS:
            if re.match(endpoint_pattern, endpoint) is not None:
                return True

        for endpoint_pattern in UNPROTECTED_ENDPOINTS:
            if re.match(endpoint_pattern, endpoint) is not None:
                return False
        return True

    def unauthorized_abort(self, message):
        response = jsonify(BadRequestSerializer(message=message).dict())
        response.status_code = HTTPStatus.UNAUTHORIZED
        abort(response)

    def get_token(self):
        auth_header = request.headers.get(HttpHeaders.AUTHORIZATION)
        if auth_header is None:
            self.unauthorized_abort("No token provided")

        token = auth_header.split(" ")[1]
        return token

    def get_user_id_from_request(self) -> UserId:
        token = self.get_token()
        return self.get_user_id_from_jwt(token)

    def verify_jwt(self):
        if not self.is_endpoint_protected(request.endpoint):
            return

        token = self.get_token()
        try:
            self.get_user_id_from_jwt(token)
        except CorruptedToken as exc:
            self.unauthorized_abort(exc.message)
        except ExpiredToken as exc:
            self.unauthorized_abort(exc.message)

    def get_user_id_from_jwt(self, token) -> UserId:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.DecodeError:
            raise CorruptedToken()
        except jwt.ExpiredSignatureError:
            raise ExpiredToken()

        jwt_entity = JWTEntity(**payload)
        return jwt_entity.sub

    def encode_jwt(self, user_id: UserId) -> JWTToken:
        jwt_entity = JWTEntity(
            sub=user_id,
            exp=datetime.now() + timedelta(days=self.access_token_duration_days),
            iat=datetime.now(),
        )
        token = jwt.encode(asdict(jwt_entity), self.secret, algorithm=self.algorithm)
        return JWTToken(token)
