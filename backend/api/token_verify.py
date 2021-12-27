import time

from authlib.jose import jwt
from flask import jsonify, request

from functools import wraps

from backend.config import Configuration


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        key_binary = Configuration.CERTIFICATE.encode('ascii')
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'A valid token is missing!'})

        try:
            decoded_token = jwt.decode(token, key_binary)
            expiration_time = decoded_token['exp']
            if expiration_time < int(time.time()):
                return jsonify({'message': 'Token has expired!'})
        except Exception:
            return jsonify({'message': 'Token is invalid!'})
        return f(*args, **kwargs)

    return decorator
