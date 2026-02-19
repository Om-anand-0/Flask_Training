from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "email": self.email
        }


@app.route('/')
def index():
    users = User.query.all()
    return render_template('user.html',users=users)

@app.route("/add_users", methods=["POST"])
def create_user():
    data = request.get_json()

    user = User(
        name=data["name"],
        role=data["role"],
        email=data["email"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": user.to_dict()
    }), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()

    return jsonify([
        user.to_dict() for user in users
    ])



@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)

    return jsonify(user.to_dict())



@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    if "name" in data:
        user.name = data["name"]

    if "role" in data:
        user.role = data["role"]

    if "email" in data:
        user.email = data["email"]

    db.session.commit()

    return jsonify({
        "message": "User updated",
        "user": user.to_dict()
    })



@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted"
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
