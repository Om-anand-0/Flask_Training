from flask import jsonify, request, render_template
from .import app
from .database import db
from .models import User

@app.route('/')
def index():
    users = User.query.all()
    return render_template('user.html', users=users)

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify([u.to_dict() for u in User.query.all()])
