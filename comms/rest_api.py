# comms/rest_api.py
from flask import Flask, request, jsonify

class RestAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self._state = None

        @self.app.route("/state", methods=["GET"])
        def get_state():
            return jsonify(self._state or {})

        @self.app.route("/state", methods=["POST"])
        def post_state():
            self._state = request.json
            return jsonify({"status": "ok"})

    def set_state(self, snapshot):
        self._state = snapshot

    def run(self, host="0.0.0.0", port=8000):
        self.app.run(host=host, port=port)
