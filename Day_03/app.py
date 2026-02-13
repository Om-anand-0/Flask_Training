from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)    

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(20))


@app.route('/')
def home():
    return "<p>hello world</p>"

@app.route("/add")
def add():
    admin = User(name = "om", role = "student", email = "com@yahoo.com")
    db.session.add(admin)
    db.session.commit()
    return f"<p>added {admin.name} with id {admin.id}</p>"

@app.route("/show")
def show():
    users = User.query.get(1)
    print(f"{users.name} {users.role} {users.email}")
    return "<p>show</p>"    

# @app.route("/update")
# def update():
#     user = User.query.get(1)
#     user.name = "shyam"
#     db.session.commit()
#     return "<p>updated</p>"

@app.route("/update/<int:id>")
def update(id):
    user = User.query.get(id)
    user.name = "shyam"
    db.session.commit()
    return f"<p>updated {user.name} with id {user.id}</p>"

@app.route("/update/<name>")
def update_name(name):
    user = User.query.get(3)
    user.name = name
    db.session.commit()
    return f"<p>updated {user.name} with id {user.id}</p>"


@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return f"<p>deleted {user.name} with id {user.id}</p>"

@app.route("/show_all")
def show_all(): 
    users = User.query.all()
    return render_template("index.html", users = users)    

@app.route("/update/email/<email>")
def update_email(email):
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return f"<p>{e}</p>"
    user = User.query.get(4)
    user.email = email
    db.session.commit()
    return f"<p>updated {user.email} with id {user.id}</p>"

@app.route("/show_f")
def show_f():
    users = User.query.filter(User.email.like("%gmail%")).all()
    return render_template("index.html", users = users)


@app.route("/test")
def test(): 
    users = User.query.all()
    return render_template("test.html", users = users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)