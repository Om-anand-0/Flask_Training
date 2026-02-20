from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager,create_access_token

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "testtttt"

jwt = JWTManager(app)

@app.route("/login",methods=["POST"])
def login():
    username = request.json.get("username",None)
    password = request.json.get("password",None)
    access_token = create_access_token(identity=username)
    if username == "test" and password == "test":
        return jsonify(message="login success", access_token=access_token), 200
    else:
        return jsonify("message", "login failed"),401


@app.route("/dashboard",methods=["GET"])
def dashboard():
    return jsonify({"message" : "dashboard access granted"}),200

if __name__ == "__main__":
    app.run(debug=True)