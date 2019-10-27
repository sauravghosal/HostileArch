from flask import Flask , request
import smtplib, ssl
from arcgis.gis import GIS
from arcgis import geometry
from arcgis import features
import requests
import googlemaps
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image     import MIMEImage
from email.header         import Header
import base64
from representatives import dict_of_contacts

app = Flask(__name__)

@app.route("/posting_email_info", methods=['POST'])
def hello():
    msg_body = request.get_json()
    text = msg_body['text']

    loc_x = float(msg_body['x'])
    loc_y = float(msg_body['y'])
    pic_string = bytearray(msg_body['picture_base_64'].encode())
    pic = decodeAndSaveLocally(pic_string)
    sender_email = msg_body['sender_email']
    tup = getRepresentative(loc_x, loc_y)
    if tup is None:
        return "Representative not found"
    else:
        state, district, name = tup
        address = reverseGeocode((loc_y,loc_x))
        if address is None:
            return "Unable to find address using reverse geocoding"
        else:
            send = text + "\n:) it works!\nYour representative is: Representative " + name + " from " + state+ "'s district number " +  district + ".\nYour address is " + address
            sendEmail("amanj120@gmail.com", send)
            return "Success" + str(sender_email.find('@') != -1)

@app.route("/")
def first():
    return "Hello World"

def getRepresentative(x, y):
    dist_id = '952b820452f545adb76ecd679981d3ae'
    gis = GIS()
    item = gis.content.get(dist_id)
    feature_layer = item.layers[0]
    pt = geometry.Point({"x": x, "y": y, "spatialReference" :{"wkid":4326}})
    dist_filter = geometry.filters.intersects(pt)
    q = feature_layer.query(where='1=1', geometry_filter=dist_filter)
    if len(q.features) == 0:
        return None
    else:
        district = q.features[0].attributes['DISTRICT']

        return ret_tup

def sendEmail(receiver_email, message):

    sender_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Help The Hobos " + str(datetime.datetime.now())
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
        <p>""" + message +  """
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
            sender_email, receiver_email, msg.as_string()
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
    print(len(dict_of_contacts))
    app.run(debug=True)
