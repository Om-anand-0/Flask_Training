from flask import Blueprint, request
from app.models import User
from app import bcrypt, db, login_manager
from identicons import generate, save
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return 'Invalid username or password'
        login_user(user)
        return redirect(url_for('chat.dashboard'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        image_file = request.files.get('image')
        file_name = f"{username}.png"
        if image_file:
            image_file.save(os.path.join("app/static/images", file_name))
        else:
            img =generate(username)
            save(img,os.path.join("app/static/images", file_name), 500, 500)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.query.filter_by(username=username).first()
        if user:
            return 'User already exists'
        user = User(username=username, email=email, password_hash=hashed_password, avatar_url=f'{username}.png')
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))