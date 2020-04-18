import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import ssl

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

## Functions
def drinks_all(data_type):
    ret_drinks = []
    drinks = Drink.query.order_by(Drink.id).all()
    for drink in drinks:
        if data_type == 'short':
            ret_drinks.append(drink.short())
        elif data_type == 'long':
            ret_drinks.append(drink.long())
    return ret_drinks

def recipe_valid(recipe):
    try:
        if not recipe:
            return True
        # must json list type
        if not isinstance(recipe, (list, tuple)):
            return False
        # must inlcude all key
        for item in recipe:
            if not 'name' in item or not 'color' in item or not 'parts' in item:
                return False

        return True
    except:
        return False

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def drinks():
    
    result = {
        'success': True,
        'drinks': drinks_all('short')
    }

    return jsonify(result)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(jwt):
    
    result = {
        'success': True,
        'drinks': drinks_all('long')
    }

    return jsonify(result)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def drinks_create(jwt):

    try:
        req_title = request.get_json().get('title', '')
        req_recipe = request.get_json().get('recipe', '')

        if not recipe_valid(req_recipe):
            abort(422)
        #db_recipe = []
        #db_recipe.append(req_recipe)
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
        drink.insert()
        
        result = {
            'success': True,
            'drinks': drinks_all('long')
        }
        return jsonify(result)
    except:
        abort(422)


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
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def drinks_update(jwt, drink_id):

    req_title = request.get_json().get('title', '')
    req_recipe = request.get_json().get('recipe', '')
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    if drink is None:
        abort(404)
    if not recipe_valid(req_recipe):
        abort(422)

    try:
        # PATCH, only modify partial data --- valid data
        if not req_title and not req_recipe:
            abort(422)
        if req_title:
            drink.title = req_title
        if req_recipe:
            drink.recipe = json.dumps(req_recipe)
        drink.update()
        
        result = {
            'success': True,
            'drinks': drinks_all('long')
        }
        return jsonify(result)
    except:
        abort(422)


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
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def drinks_delete(jwt, id):

    drink = Drink.query.filter(Drink.id == id).one_or_none()
    if drink is None:
        abort(404)

    try:
        drink.delete()
        
        result = {
            'success': True,
            'delete': id
        }
        return jsonify(result)
    except:
        abort(422)


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def handle_AuthError(error):
    return jsonify({
        "success": False, 
        "error": error.status_code,
        "message": error.error,
        }), error.status_code


#if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=8080, debug=True, ssl_context='adhoc')
    #app.run(host='127.0.0.1', port=8080, debug=True)
