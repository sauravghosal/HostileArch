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
import time
import os

#Necessary for flask app
app = Flask(__name__)

#simply reads a file and returns it as a list
def get_list_of_bad_words():
    file = open('bad-words.txt','r')
    reading = file.read()
    list_of_bad_words = reading.split('\n')
    file.close()
    return list_of_bad_words

#Necessary for ESRI API, makes this variable
dist_id = '952b820452f545adb76ecd679981d3ae'
gis = GIS()
item = gis.content.get(dist_id)
feature_layer = item.layers[0]

#makes this list global so it's faster
list_of_bad_words = get_list_of_bad_words()

@app.route("/")
def homepage():
    return "Hello World"

#Big Daddy function that does EVERYTHING
@app.route("/posting_email_info", methods=['POST'])
def mainfunction():
    #extract the location from JSON, use it to get District
    request_body = request.get_json()
    loc_x = float(request_body['x'])
    loc_y = float(request_body['y'])
    district = getDistrict(loc_x, loc_y)

    if district is None:
        return "Representative not found"

    caption = request_body['text']
    checked_caption = checkMessage(caption); #checks for profanity
    if checked_caption is not None:
        return checked_caption

    pic_string = bytearray(request_body['picture_base_64'].encode())
    millis = int(round(time.time() * 1000)) #to have unique image names
    image_filename = "user_image_" + str(millis) + ".png"
    decodeAndSaveLocally(pic_string, image_filename) #saves the image locally

    #Extract more JSON fields
    citizen_email = request_body['sender_email']
    citizen_name = request_body['name']
    timestamp = request_body['timestamp']

    #Use Google Maps API to get an address from the location
    address = reverseGeocode((loc_y,loc_x))
    if address is None:
        return "Unable to find address using reverse geocoding"

    #get the relevant representative properties
    representative_last_name = dict_of_contacts[district][1]
    rep_emails_str = (', ').join(list(dict_of_contacts[district][2:]))
    rep_emails_list = list(dict_of_contacts[district][2:])

    #generate the main text of the email
    email_body = generate_body(representative_last_name, address, caption, citizen_name, rep_emails_str)

    #for debugging purposes, we are not sending emails to actual representatives
    test_emails_str = (', ').join(list(("aman.jain@gatech.edu", "jgdss81@gmail.com")))
    test_emails_list = list(("aman.jain@gatech.edu", "jgdss81@gmail.com"))

    email_error_code = sendEmail(test_emails_str, test_emails_list, citizen_email, image_filename, email_body, address, timestamp)

    if email_error_code is None:
        return "Thank you for being a good citizen."

    return email_error_code

def sendEmail(rep_emails_str, rep_emails_list, citizen_email, image_filename, message, address, timestamp):

    #the account of the central email that we are sending all the mails through
    central_email = "helpTheHomelessFixThisSpace@gmail.com"
    password = "fixin123smtp!!!"
    '''
    central_email = "hostilearchitectureawareness@gmail.com"
    password = "hostilearch123"
    '''
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    subject_line = "A citizen wants your help to fix this space: " + address + " | " + timestamp
    msg['Subject'] = subject_line
    msg['From'] = central_email
    msg['To'] = rep_emails_str
    #if citizen email is valid, then we Bcc to citizen
    if citizen_email.find('@') != -1:
        msg['Cc'] = citizen_email

    #alternative message incase it doesn't work
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    msgText = MIMEText('Message could not be loaded. Please ignore this message.')
    msg.attach(msgText)

    # We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(message, 'html')
    msg.attach(msgText)

    # This example assumes the image is in the current directory
    fp = open(image_filename, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    # Create secure connection with server and send email
 #   try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(central_email, password)
        if citizen_email.find('@') != -1:
            rep_emails_list.append(citizen_email)
        server.sendmail(central_email, rep_emails_list, msg.as_string())

    #get rid of the image once we are done
    if os.path.exists(image_filename):
        os.remove(image_filename)

    return None
#    except:
#        return "SMTP Server Failed. Please try again later."

#goes through the words in the message and sees if it's in the list of bad words
def checkMessage(caption):
    for word in caption.split(' '):
        if word in list_of_bad_words:
            return "You cannot use the word " + word + ". Please be respectful."
    return None

#constructs an html text to send
def generate_body(representative_last_name, address, caption, citizen_name, rep_emails):
    html = '''
    <html>
      <head></head>
      <body>
        <p>Actual emails to send it to ______rem______</p>
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
        They found this piece of hostile architecture at ______adr______.</p>
        <p>We at fixthis.space are simply deliverers of their message, and this is what they have to say:</p>
        <p>______msg______</p>
        <img src="cid:image1">
        <p>We are all human, and we all deserve respect</p>
        <p>Sincerely,</p>
        <p>A group of concerned citizens______cit______</p>
      </body>
    </html>
    '''
    rep = html.replace('______rep______', representative_last_name).replace('______msg______', caption).replace('______adr______', address)
    rep = rep.replace('______rem______',rep_emails)
    if len(citizen_name) > 1:
        rep = rep.replace('______cit______', (' on behalf of ' + citizen_name + '.'))
    else:
        rep = rep.replace('______cit______', '.')
    return rep

#Use ESRI API to get Georgia Representative District number
def getDistrict(x, y):
    pt = geometry.Point({"x": x, "y": y, "spatialReference" :{"wkid":4326}})
    dist_filter = geometry.filters.intersects(pt)
    q = feature_layer.query(where='1=1', geometry_filter=dist_filter)
    if len(q.features) == 0:
        return None #if the area is not in georgia, return None
    else:
        return int(q.features[0].attributes['DISTRICT']) #district number

#Look up an address with reverse geocoding and Google Maps API
def reverseGeocode(coordinates):
    gmaps = googlemaps.Client(key="AIzaSyACXhXaxtZ3mw7-2d2vjIckekoE4lQbY48")
    result = gmaps.reverse_geocode(coordinates)
    ans = result[0]["formatted_address"]
    return ans

#saves a byte array as an image
def decodeAndSaveLocally(encoded_string, image_filename):
    with open(image_filename, "wb") as fh:
        fh.write(base64.decodebytes(encoded_string))

if __name__ == '__main__':
    app.run(debug=True)
