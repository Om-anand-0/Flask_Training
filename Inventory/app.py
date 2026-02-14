from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


@app.route('/')
def home():
    return "<p>Inventory Page</p>"

@app.route("/add")
def add():
    admin = Product(name = "Laptop", price = 100000, quantity = 10)
    db.session.add(admin)
    db.session.commit()
    return "<p>added</p>" 

@app.route("/update/<id>")
def update(id):
    product = Product.query.get(id)
    product.name = "Mobile"
    product.price = "30000"
    product.quantity = "20"
    db.session.commit()
    return "<p>updated</p>"



@app.route("/show_all")
def show_all(): 
    products = Product.query.all()
    return render_template("index.html", products = products)   


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)       