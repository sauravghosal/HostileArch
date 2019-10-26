import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header
import base64

def sendEmail(receiver_email, message):

    sender_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "99!!!!!!!"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
      <head></head>
      <body>
        <img src="cid:image1">
        <p>99<br>
           NINEINEEEEE<br>
           WE LOVE BROOKLYN NINENINEEEE WATCH THIS PLEASE <a href="https://www.youtube.com/watch?v=zE5sEbEehNo">link</a>!!!!
        </p>
      </body>
    </html>
    """

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msg.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(html, 'html')
    msg.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('bench.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)


    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
    print ("success")
    return;
def decodeAndSaveLocally(encoded_string):
    with open("bench.jpg", "wb") as fh:
        fh.write(base64.decodebytes(encoded_string))

def main():
    # with open("brooklyn-nine-nine.jpg", "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())
    decodeAndSaveLocally(encoded_string)
    sendEmail("sruthisudhakar81@gmail.com", "asdf")

if __name__ == "__main__": main()
