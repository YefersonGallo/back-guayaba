from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from main import Queue_Guava

app = Flask(__name__)
CORS(app, support_credentials=True)

# Petición para comprobar la conexión del servidor
@app.route('/ping', methods=['GET'])
@cross_origin(supports_credentials=True)
def ping():
    return jsonify({'response': 'pong!'})


@app.route('/init_production', methods=['POST'])
@cross_origin(supports_credentials=True)
def init_production():
    nBoxPerDay = request.json["nBoxPerDay"]
    muState1 = request.json["muState1"]
    muState2 = request.json["muState2"]
    muState3 = request.json["muState3"]
    muState4 = request.json["muState4"]
    muState42 = request.json["muState42"]
    sigma = request.json["sigma"]
    muState5 = request.json["muState5"]
    days = request.json["days"]
    queue = Queue_Guava(nBoxPerDay, muState1, muState2, muState3, muState4, muState42, sigma, muState5)
    queue.start(days)
    return jsonify(queue.send_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)