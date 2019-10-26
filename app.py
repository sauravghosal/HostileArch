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
import tweepy

app = Flask(__name__)

@app.route("/posting_email_info", methods=['POST'])
def hello():
    #Get JSON information from request
    msg_body = request.get_json()
    text = msg_body['text']
    loc_x = float(msg_body['x'])
    loc_y = float(msg_body['y'])
    pic_string = bytearray(msg_body['picture_base_64'].encode())
    pic = decodeAndSaveLocally(pic_string)
    filer_email = msg_body['filer_email']
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
            sendEmail("amanj120@gmail.com", filer_email, send)
            return "Success" + str(filer_email.find('@') != -1)

@app.route("/")
def first():
    return "Hello World"

def getRepresentative(x, y):
    pt = geometry.Point({"x": x, "y": y, "spatialReference" :{"wkid":4326}})
    dist_filter = geometry.filters.intersects(pt)
    q = feature_layer.query(where='1=1', geometry_filter=dist_filter)
    if len(q.features) == 0:
        return None
    else:
        attributes = q.features[0].attributes
        name = attributes['LAST_NAME']
        state = attributes['STATE_ABBR']
        district = attributes['CDFIPS']
        ret_tup = (state, district, name)
        return ret_tup

def sendEmail(filer_email, receiver_email, message):

    sender_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Raising Hostile Architecture Awarness"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    if filer_email is not None:
        msg['Bcc'] = filer_email

    html = """\
    <html>
      <head></head>
      <body>
        <img src="cid:image1">
        <p>Hello,<br>
           This is the hostile architecture group sending you an email on behalf of a citizen.<br>
           There has been a report of hostile architecture identified by a citizen. Please read what they had to say below.
        </p>
        <p>""" + message +  """
      </body>
    </html>
    """

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    msgText = MIMEText('This is the picture they identified. There is an error loading the picture.')
    msg.attach(msgText)

    msgText = MIMEText(html, 'html')
    msg.attach(msgText)

    fp = open('temp.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        if filer_email is None:
            server.sendmail(
                sender_email, receiver_email, msg.as_string()
            )
        else
            server.sendmail(
                sender_email, [receiver_email, filer_email], msg.as_string()
            )
    print ("success")
    return;

def reverseGeocode(coordinates):
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")
    result = gmaps.reverse_geocode(coordinates)
    ans = result[0]["formatted_address"]
    return ans

def decodeAndSaveLocally(encoded_string):
    with open("temp.png", "wb") as fh:
        fh.write(base64.decodebytes(encoded_string))
def postTweet():
    twitter_auth_keys = {
        "consumer_key"        : "REPLACE_THIS_WITH_YOUR_CONSUMER_KEY",
        "consumer_secret"     : "REPLACE_THIS_WITH_YOUR_CONSUMER_SECRET",
        "access_token"        : "REPLACE_THIS_WITH_YOUR_ACCESS_TOKEN",
        "access_token_secret" : "REPLACE_THIS_WITH_YOUR_ACCESS_TOKEN_SECRET"
    }

    auth = tweepy.OAuthHandler(
            twitter_auth_keys['consumer_key'],
            twitter_auth_keys['consumer_secret']
            )
    auth.set_access_token(
            twitter_auth_keys['access_token'],
            twitter_auth_keys['access_token_secret']
            )
    api = tweepy.API(auth)

    tweet = "Another day, another #scifi #book and a cup of #coffee"
    status = api.update_status(status=tweet)

if __name__ == '__main__':
    dist_id = 'cc6a869374434bee9fefad45e291b779'
    gis = GIS()
    item = gis.content.get(dist_id)
    feature_layer = item.layers[0]
    app.run(debug=True)
