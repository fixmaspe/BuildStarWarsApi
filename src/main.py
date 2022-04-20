"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Vehicle#, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#NOTA
#puedo copiar todo esto pero literalmente puedo crear una nueva ruta
@app.route('/user', methods=['GET'])
def get_usert():
    query_user = User.query.all()
    query_user = list(map(lambda x: x.serialize(), query_user))
    print(query_user)
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "people": query_user
    }
    return jsonify(response_body), 200
#codigo original de USER
#def handle_hello():
#
    #response_body = {
        #"msg": "Hello, this is your GET /user response "
    #}
#
    #return jsonify(response_body), 200

@app.route('/people', methods=['GET', 'POST'])
def methods_people():
    if request.method == 'POST':
        body = request.get_json()
        print(body)
        response_body = {
            "msg": "Hello, this is your POST /people response"
        }
        return jsonify(response_body), 200
    else:
        query_people = People.query.all()
        query_people = list(map(lambda x: x.serialize(), query_people))
        print(query_people)
        response_body = {
            "msg": "Hello, this is your GET /People response ",
            "People": query_people
        }
        return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
def get_planet():
    query_planet = Planet.query.all()
    query_planet = list(map(lambda x: x.serialize(), query_planet))
    print(query_planet)
    response_body = {
        "msg": "Hello, this is your GET /planet response ",
        "planet": query_planet
    }
    return jsonify(response_body), 200

@app.route('/vehicle', methods=['GET'])
def get_vehicle():
    query_vehicle = Vehicle.query.all()
    query_vehicle = list(map(lambda x: x.serialize(), query_vehicle))
    print(query_vehicle)
    response_body = {
        "msg": "Hello, this is your GET /vehicle response ",
        "vehicle": query_vehicle
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
