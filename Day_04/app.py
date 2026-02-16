from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)    

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    role = db.Column(db.String(20))
    email = db.Column(db.String(20),unique = True, nullable = False)
    status = db.Column(db.Boolean, default = True, nullable = False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow, onupdate = datetime.utcnow)

@app.route('/')
def home():
    return "<p>hello world</p>"

@app.route("/add")
def add():
    admin = User(name = "om", role = "student", email = "com@yahoo.com")
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"Email already exists {e}"
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

@app.route("/showall_desc")
def show_all_desc(): 
    users = User.query.order_by(User.id.desc()).all()
    # users = User.query.all()
    # users.reverse()
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

@app.route("/count")
def count():
    users = User.query.count()
    return f"<p>count {users}</p>"


@app.route("/searchby_name")
def searchby_name():
    users = User.query.filter(User.name.like("%om")).all()
    return render_template("index.html", users = users)



##### new table

@app.route("/post")
def post():
    user = User(name = "shyaam", email = "shyaam@gmail.com",role = "editor")
    db.session.add(user)
    db.session.commit()
    post = Post(title = "Paneer Bhurji", content = "Paneer Bhurji is a popular Indian dish", userid = user.id)
    db.session.add(post)
    db.session.commit()

    return render_template("index2.html", posts = db.session.query(User, Post).join(Post, User.id == Post.userid).all(), users = User.query.all())


@app.route("/post_by/<name>")
def postby_name(name):
    user = User.query.filter(User.name == name).first()
    if user:
        post = Post.query.filter(Post.userid == user.id).all()
        return render_template("index2.html", posts = post, users = User.query.all())
    else:
        return "<p>no post found</p>"

@app.route("/show_post")
def show_post():
    page = request.args.get('page', 1, type=int)
    posts = db.session.query(User,Post).join(Post, User.id == Post.userid).paginate(per_page = 2, page = page)
    # print(posts)
    for user, post in posts:
        print(f"{post.title} by {user.name}")
    return render_template("index2.html", posts = posts)    

# @app.route("/test")``
# def test(): 
#     users = User.query.all()
#     return render_template("test.html", users = users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)       