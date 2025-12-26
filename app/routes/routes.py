from flask import request, jsonify, Flask
import app.models

@app.route('/request/forward', methods=['POST'])
def request_forward():
    """Forward a request"""
    data = request.get_json()
    # TODO: get parameters from the request and forward the corresponding request
    # if rescuee_id and rescuer_id are not None, forward the request to the rescuer
    return jsonify({'message': 'Request forwarded successfully', 'data': data}), 200


@app.route('/request/accept', methods=['POST'])
def request_accept():
    """Accept a request"""
    data = request.get_json()
    # TODO: get parameters from the request and accept the corresponding request
    # if rescuee_id and rescuer_id are not None, accept the request from the rescuee
    # then send a notification to the rescuer
    return jsonify({'message': 'Request accepted successfully', 'data': data}), 200


@app.route('/request/update', methods=['POST'])
def request_update():
    """Update a request"""
    data = request.get_json()
    # TODO: get parameters from the request and update the corresponding request
    # if rescuee_id and rescuer_id are not None, update the request on the db and forward it to the rescuer
    return jsonify({'message': 'Request updated successfully', 'data': data}), 200


@app.route('/request/delete', methods=['POST'])
def request_delete():
    """Delete a request"""
    data = request.get_json()
    # TODO: get parameters from the request and delete the corresponding request
    return jsonify({'message': 'Request deleted successfully', 'data': data}), 200
