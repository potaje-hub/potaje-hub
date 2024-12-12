import uuid
from flask import jsonify, make_response
from app.modules.fakenodo import fakenodo_bp
import json


@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['GET'])
def get_all():
    with open('app/modules/fakenodo/depositions.json') as f:
        data = json.load(f)
    return jsonify(data)


@fakenodo_bp.route('/fakenodo/deposit/depositions', methods=['POST'])
def create():
    response = make_response(jsonify({"message": "Deposition created", "id": 1, "conceptrecid": 1}))
    response.status_code = 201
    return response


@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/files', methods=['POST'])
def upload(id):
    response = make_response(jsonify({"message": f"File uploaded to deposition {id}"}))
    response.status_code = 201
    return response


@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>/actions/publish', methods=['POST'])
def publish(id):
    response = make_response(jsonify({"message": f"File uploaded to deposition {id}"}))
    response.status_code = 202
    return response


@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['DELETE'])
def delete(id):
    return jsonify({"message": f"Deposition {id} deleted"})


@fakenodo_bp.route('/fakenodo/deposit/depositions/<int:id>', methods=['GET'])
def get_deposition(id):
    with open('app/modules/fakenodo/deposition.json') as f:
        data = json.load(f)
        # randomize doi with uuid

        data['doi'] = str(uuid.uuid4())

    return jsonify(data)
