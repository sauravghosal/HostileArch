import smtplib, ssl

# Python3 program for reverse geocoding.

# importing necessary libraries
import reverse_geocoder as rg
import pprint

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
    result = rg.search(coordinates)

    # result is a list containing ordered dictionary.
    pprint.pprint(result)

def main():
    sendEmail("sruthisudhakar81@gmail.com", "yo")
    coordinates =(28.613939, 77.209023)

    reverseGeocode(coordinates)

if __name__ == "__main__": main()
