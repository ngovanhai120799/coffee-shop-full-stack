import os
from flask import Flask, request, abort
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
import json
from flask_cors import CORS

from database import db_drop_and_create_all, setup_db, Drink
from auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
app.route('/drinks', methods=['GET'])
def get_drinks():
   try:
        drinks = Drink.query.all()
        return json.dumps({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })
   except SQLAlchemyError as err:
       abort(400, f'Get ALL drinks fail: {err}')


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail():
   try:
        drinks = Drink.query.all()
        return json.dumps({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
        })
   except SQLAlchemyError as err:
       abort(400, f'Get ALL drinks detail fail: {err}')

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
app.route('/drinks-detail', methods=['POST'])
def post_drinks():
   try:
        request_body = request.get_json()
        title = request_body.get("title")
        recipe = request_body.get("recipe")
        drink = Drink(title, recipe)
        drink.insert()
        
        return json.dumps({
            "success": True,
            "drinks": [drink.long()]
        })
   except SQLAlchemyError as err:
       abort(400, f'POST drink fail: {err}')

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
app.route('/drinks/<int: id>', methods=['PATCH'])
def patch_drinks(id):
   try:
        request_body = request.get_json()
        title = request_body.get("title", None)
        recipe = request_body.get("recipe", None)
        drink = Drink.query.get_or_404(id)
        if title is not None:
            drink.title = title
        if recipe is not None:
            drink.recipe = recipe
        
        drink.update()
        return json.dumps({
            "success": True,
            "drinks": [drink.long()]
        })
   except SQLAlchemyError as err:
       abort(400, f'PATCH drink fail: {err}')
   except NoResultFound as ne:
       abort(404, f'NOT FOUND drink: {ne}')

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
app.route('/drinks/<int: id>', methods=['DELETE'])
def delete_drinks(id):
   try:
        drink = Drink.query.get_or_404(id)
        drink.delete()
        return json.dumps({
            "success": True,
            "delete": id
        })
   except SQLAlchemyError as err:
       abort(400, f'PATCH drink fail: {err}')
   except NoResultFound as ne:
       abort(404, f'NOT FOUND drink: {ne}')


# Error Handling
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             json.loads({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def resource_bad_request(e):
    return get_response_json_error(400, f'Bad Request: {str(e)}')


@app.errorhandler(404)
def resource_not_found(e):
    return get_response_json_error(404, f'Resource not found: {str(e)}')


@app.errorhandler(422)
def resource_unprocessable(e):
    return get_response_json_error(422, f'Unprocessable Exception: {str(e)}')


@app.errorhandler(500)
def resource_internal_server_error(e):
    return get_response_json_error(500, f'Internal Server Error Exception: {str(e)}')


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
def get_response_json_error(status_code: int, message: str):
    return json.loads({
        'success': False,
        'error': status_code,
        'message': message
    }), status_code


if __name__ == "__main__":
    app.debug = True
    app.run()