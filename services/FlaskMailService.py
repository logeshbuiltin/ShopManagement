from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "razerockztech@gmail.com",
    "MAIL_PASSWORD": "Scooby@77G"
}
app.config.update(mail_settings)
mail = Mail(app)

class SendEmail:

    def send_mail():
        try:
            msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=["<logeshbuiltin@gmail.com>"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")         
            mail.send(msg)
            print ('Mail sent!')

        except Exception as error:
            print (error) 