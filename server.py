from flask import Flask, request, jsonify

app = Flask(__name__)

VALID_USERS = ["quyet"]

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")

    if username in VALID_USERS:
        return jsonify({"status": "success"})
    return jsonify({"status": "fail"}), 401


@app.route("/")
def home():
    return "Server running"


if __name__ == "__main__":
    app.run()