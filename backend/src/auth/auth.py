import json
from urllib.request import urlopen
from functools import wraps
from os import environ as env
from dotenv import load_dotenv
from flask import request
from jose import jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError

from backend.src.exceptions.auth_error import AuthError

# Get Auth0 environment variables
load_dotenv()
app_secret_key = env["APP_SECRET_KEY"]
auth0_domain = env["AUTH0_DOMAIN"]
auth0_client_id = env["AUTH0_CLIENT_ID"]
auth0_client_secret = env["AUTH0_CLIENT_SECRET"]
api_audience = env["API_AUDIENCE"]


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                token = _get_token_auth_header()
                payload = _verify_token_auth(token)
                _check_permission(permission, payload)
                return f(*args, **kwargs)
            except Exception as e:
                raise e
        return decorated_function
    return requires_auth_decorator


def _get_token_auth_header():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    if not token:
        raise AuthError(401, {
            "message": "Authentication Token is missing!",
            "error": "Unauthorized"
        })
    return token


def _verify_token_auth(token):
    jsonurl = urlopen(f'https://{auth0_domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError(401, {
            "message": "Authorization malformed.",
            "error": "Unauthorized"
        })

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key,
                                 algorithms=["RS256"],
                                 audience=api_audience,
                                 issuer='https://' + auth0_domain + '/')
            return payload
        except ExpiredSignatureError:
            raise AuthError(401, {
                "message": "Token expired.",
                "error": "Unauthorized"
            })
        except JWTClaimsError:
            raise AuthError(401, {
                "message": "Incorrect claims. Please, check the audience and issuer.",
                "error": "invalid_claims"
            })
        except Exception as e:
            raise AuthError(400, {
                "message": "Unable to parse authentication token.",
                "error": "Unauthorized"
            })


def _check_permission(permission, payload):
    if "permissions" not in payload:
        raise AuthError(400, {
            "message": "Unable to parse authentication token.",
            "error": "invalid_claims"
        })
    if permission not in payload["permissions"]:
        raise AuthError(403, {
            'error': 'unauthorized',
            'message': 'Permission not found.'
        })
    return True
