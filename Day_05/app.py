from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    name = request.form.get("name")
    return render_template("confirmation.html", email=email, name=name)

@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        return render_template("confirmation.html", email=email, name=name, password=password)
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name == "admin" and password == "admin":
            session["user"] = name
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user" not in session:
        return redirect(url_for("login"))
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" in session:
        search_query = None
        if request.method == "POST":
             search_query = request.form.get("search")
        return render_template("dashboard.html", user=session["user"], search_query=search_query)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)




