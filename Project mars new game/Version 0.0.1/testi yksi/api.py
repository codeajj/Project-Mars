from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests (important for different ports)

@app.route("/task", methods=["GET"])
def task():
    return jsonify(message="Task started successfully.")

@app.route("/quit", methods=["GET"])
def quit():
    return jsonify(message="Game has been quit.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)