#############################################
# IMPORTS
#############################################
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from flask_bcrypt import Bcrypt

#############################################
# 
#############################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.secret_key = 'tillu'

bcrypt = Bcrypt(app)
#############################################
# MODELS
#############################################

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))
    


#############################################
# DECORATORS
#############################################
def validate_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        user = User.query.filter_by(username=session['username']).first()
        if user.role != 'admin':
            return 'Unauthorized'
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return redirect(url_for('tasks'))
        return f(*args, **kwargs)
    return decorated_function
#############################################
# ROUTES
#############################################

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
@redirect_if_logged_in
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        Hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User.query.filter_by(email=email).first()
        if user:
            return 'User already exists'

        role = 'admin' if username == 'admin' else 'user'
        new_user = User(username=username, email=email, password=Hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('tasks'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@redirect_if_logged_in
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return 'Invalid email or password'

        session['username'] = user.username
        return redirect(url_for('tasks'))
    return render_template('login.html')


@app.route('/tasks')
@validate_user
def tasks():
    user = User.query.filter_by(username=session['username']).first()
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks, user=user)

@app.route('/admin')
@is_admin
def admin():
    user = User.query.filter_by(username=session['username']).first()
    all_tasks = Task.query.all()
    return render_template('tasks.html', tasks=all_tasks, user=user, is_admin_view=True)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_admin', methods=['POST'])
@is_admin
def add_admin():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    role = 'admin'
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/add_user', methods=['POST'])
@is_admin
def add_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    role = 'user'
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/add_task', methods=['POST'])
@validate_user
def add_task():
    title = request.form['title']
    description = request.form['description']
    user = User.query.filter_by(username=session['username']).first()
    new_task = Task(title=title, description=description, user_id=user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@validate_user
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    current_user = User.query.filter_by(username=session['username']).first()
    
    if current_user.role != 'admin' and task.user_id != current_user.id:
        return 'Unauthorized'
        
    db.session.delete(task)
    db.session.commit()

    if current_user.role == 'admin' and request.referrer and 'admin' in request.referrer:
         return redirect(url_for('admin'))
    return redirect(url_for('tasks'))   



@app.route('/show_user_tasks/<int:user_id>')
@validate_user
def show_user_tasks(user_id):
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks, user=user)   

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 