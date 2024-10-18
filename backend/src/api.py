from flask import Flask, request
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth

from exceptions.auth_error import AuthError
from exceptions.bad_request_exception import BadRequestException
from exceptions.not_found_exception import NotFoundException
from service import DrinkService
from utils.response_utils import get_response_json_error, get_response

app = Flask(__name__)
CORS(app)
oauth = OAuth(app)
service = DrinkService()


# ROUTES
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        response = service.get_drinks()
        return get_response(200, response)
    except Exception as e:
        if e.__class__.__name__ == 'AuthError':
            raise AuthError(e.status_code, e.error)
        raise e


@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
    try:
        response = service.get_drinks_detail()
        return get_response(200, response)
    except Exception as e:
        if e.__class__.__name__ == 'AuthError':
            raise AuthError(e.status_code, e.error)
        raise e

@app.route('/drinks', methods=['POST'])
def post_drinks():
    try:
        request_body = request.get_json()
        response = service.post_drink(request_body)
        return get_response(200, response)
    except Exception as e:
        if e.__class__.__name__ == 'AuthError':
            raise AuthError(e.status_code, e.error)
        raise e


@app.route('/drinks/<int:_id>', methods=['PATCH'])
def patch_drinks(_id):
    try:
        request_body = request.get_json()
        response = service.patch_drinks(_id, request_body)
        return get_response(200, response)
    except Exception as e:
        if e.__class__.__name__ == 'AuthError':
            raise AuthError(e.status_code, e.error)



@app.route('/drinks/<int:_id>', methods=['DELETE'])
def delete_drinks(_id):
    try:
        service.delete_drinks(_id)
        return get_response(200, {})
    except Exception as e:
        if e.__class__.__name__ == 'AuthError':
            raise AuthError(e.status_code, e.error)
        raise e

@app.errorhandler(BadRequestException)
def resource_bad_request(e):
    return get_response_json_error(e)


@app.errorhandler(NotFoundException)
def resource_not_found(e):
    return get_response_json_error(e)


@app.errorhandler(AuthError)
def resource_authorized(e):
    return get_response_json_error(e)


if __name__ == "__main__":
    app.debug = True
    app.run()
