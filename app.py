from flask import Flask , request
import smtplib, ssl
from arcgis.gis import GIS
from arcgis import geometry
from arcgis import features
import requests
import googlemaps
from datetime import datetime

app = Flask(__name__)

@app.route("/posting_email_info", methods=['POST'])
def hello():
    msg_body = request.get_json()
    text = msg_body['text']
    loc_x = float(msg_body['x'])
    loc_y = float(msg_body['y'])
    pic = msg_body['picture_base_64']
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
            return "Success"

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

def reverseGeocode(coordinates):
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")
    # Look up an address with reverse geocoding
    result = gmaps.reverse_geocode(coordinates)
    ans = result[0]["formatted_address"]
    return ans

if __name__ == '__main__':
    dist_id = 'cc6a869374434bee9fefad45e291b779'
    gis = GIS()
    item = gis.content.get(dist_id)
    feature_layer = item.layers[0]
    app.run(debug=True)
