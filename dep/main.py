from flask import Flask , request
import smtplib, ssl

app = Flask(__name__)

@app.route("/poster", methods=['POST'])
def hello():
    msg_body = request.get_json()
    text = msg_body['text']
    send = text + "\n:) it works!\n" + text
    sendEmail("amanj120@gmail.com", send)
    return "Success"


@app.route("/")
def first():
    return "Hello World"

def sendEmail(receiver_email, message):
    sender_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message
        )
    print ("success")
    return;

if __name__ == '__main__':
    app.run(debug=True)
