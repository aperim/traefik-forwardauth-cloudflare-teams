from flask import request, abort
from werkzeug import Response
from .jwt import decode_token
from jwt.exceptions import ExpiredSignatureError, InvalidKeyError, InvalidTokenError, PyJWKClientError, PyJWKSetError, PyJWKError


def index():
    return Response('use: /auth/<audience>', 404)


def auth(audience):
    jwt = request.headers.get('Cf-Access-Jwt-Assertion')

    if jwt is None:
        abort(Response('Token is missing.', 401))

    try:
        payload = decode_token(jwt, audience)
        # Use email for user logins, common_name for service tokens
        user = payload.get('email') or payload.get('common_name', 'unknown')
        return Response('Verified.', 200, {'X-Auth-User': user})
    except ExpiredSignatureError:
        abort(Response('Token is expired.', 401))
    except InvalidTokenError:
        abort(Response('Token is invalid.', 400))
    except (InvalidKeyError, PyJWKError, PyJWKSetError, PyJWKClientError):
        abort(Response('Service temporarily unavailable.', 503))
    except:
        abort(Response('An unknown error occurred.', 500))
