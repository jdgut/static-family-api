"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def show_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET', 'DELETE'])
def show_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify("Not found"), 404
    else:
        return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    if jackson_family.delete_member(id):
        return jsonify('ok'), 200
    else:
        return jsonify("Not found"), 404

@app.route('/member', methods=['POST'])
def add_member():
    member = request.get_json()
    #or
    #member = json.loads(request.data)

    if 'first_name' not in member:
        return "Missing first_name", 400
    elif 'last_name' not in member:
        return "Missing last_name", 400
    elif 'lucky_numbers' not in member:
        return "Missing lucky_numbers", 400
    elif 'age' not in member:
        return "Missing age", 400
    elif isinstance(member['lucky_numbers'], list) == False:
        return "lucky numbers must be a valid list"

    jackson_family.add_member(member)
    return jsonify('ok'), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
