from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv()

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_USERNAME'] = "omanand.gskill@gmail.com"
app.config['MAIL_PASSWORD'] = "udxuardwduzjtikk"
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
app.config['MAIL_DEFAULT_SENDER'] = "omanand.gskill@gmail.com"

@app.route("/mail")
def email():
    mail = Mail(app)
    msg = Message(subject="Hello", recipients=["omanand.gskill@gmail.com"], body="This is a test email")
    mail.send(msg)
    return "Email sent"
    
if __name__ == "__main__":
    app.run(debug=True)