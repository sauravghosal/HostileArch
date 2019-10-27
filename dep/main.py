from email.mime.multipart import MIMEMultipart
from representatives import dict_of_contacts
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from datetime import datetime as dt
from flask import Flask , request
from email.header import Header
from datetime import datetime
from arcgis import geometry
from arcgis import features
from arcgis.gis import GIS
import smtplib, ssl
import googlemaps
import requests
import base64

app = Flask(__name__)

dist_id = '952b820452f545adb76ecd679981d3ae'
gis = GIS()
item = gis.content.get(dist_id)
feature_layer = item.layers[0]

@app.route("/")
def first():
    return "Hello World"

@app.route("/posting_email_info", methods=['POST'])
def hello():
    msg_body = request.get_json()
    loc_x = float(msg_body['x'])
    loc_y = float(msg_body['y'])
    district = getDistrict(loc_x, loc_y)
    if district is None:
        return "Representative not found"
    else:
        caption = msg_body['text']
        pic_string = bytearray(msg_body['picture_base_64'].encode())
        pic = decodeAndSaveLocally(pic_string)
        sender_email = msg_body['sender_email']
        address = reverseGeocode((loc_y,loc_x))
        representative_last_name = dict_of_contacts[district][1]
        rep_emails = list(dict_of_contacts[district][2:])
        if address is None:
            return "Unable to find address using reverse geocoding"
        else:
            email_body = generate_body(pic, address, representative_last_name, caption)
            sendEmail(list("amanj120@gmail.com"), email_body)
            return "Success" + str(sender_email.find('@') != -1)

def generate_body(pic, address, representative_last_name, caption):
    html = '''
    <html>
      <head>
        <link href="https://fonts.googleapis.com/css?family=Josefin+Sans:300&display=swap" rel="stylesheet">
        <style>
          body {
            font-family: 'Josefin Sans', sans-serif;
            font-size: 24px;
          }
        </style>
      </head>
      <body>
        <br>
        <p>Dear Representative ______rep______, </p>
        <p>We commonly find ourselves using rhetoric like "the homeless epidemic", and other
        phrases that dehumanize the homeless. However, people wiothout homes are still people,
        and we believe that they deserve the basic right to have a place to sleep.</p>
        <p>However, we find ourselves in a saddening situation, where people believe it is alright
        to create structures in public places that cause discomfort and humiliation. We believe these
        "Hostile Structures" serve no positive purpose to society and need to be removed and replaced
        with kinder, more considerate things.</p>
        <p>A citizen that you represent looked at this space and understood that it is something that is unfair and needs fixing.
        They found this piece of hostile architecture at ______adr______
        We at fixthis.space are simply deliverers of their message, and this is what they have to say:</p>
        <p>______msg______</p>
        <p>______pic______</p>
        <p>We are all human, and we all deserve respect</p>
        <p>Sincerely,</p>
        <p>A group of concerned citizens</p>
      </body>
    </html>
    '''
    html.replace('______rep______', representative_last_name)
    html.replace('______msg______', caption)
    html.replace('______adr______', address)
    return html


def getDistrict(x, y):
    pt = geometry.Point({"x": x, "y": y, "spatialReference" :{"wkid":4326}})
    dist_filter = geometry.filters.intersects(pt)
    q = feature_layer.query(where='1=1', geometry_filter=dist_filter)
    if len(q.features) == 0:
        return None
    else:
        return int(q.features[0].attributes['DISTRICT'])

def sendEmail(receiver_emails : list, message):

    sender_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    subject_line = "A citizen wants your help to fix this space: " + dt.now().strftime("%A %B %d, %Y %I:%M %p")
    msg['Subject'] = subject_line
    msg['From'] = sender_email
    msg['To'] = receiver_emails

    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"


    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msg.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(message, 'html')
    msg.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open('bench.png', 'rb')
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
            sender_email, receiver_emails, msg.as_string()
        )
    print ("success")
    return;

def reverseGeocode(coordinates):
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")
    # Look up an address with reverse geocoding
    result = gmaps.reverse_geocode(coordinates)
    ans = result[0]["formatted_address"]
    return ans

def decodeAndSaveLocally(encoded_string):
    with open("bench.png", "wb") as fh:
        fh.write(base64.decodebytes(encoded_string))

if __name__ == '__main__':
    app.run(debug=True)
