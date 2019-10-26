import smtplib, ssl

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

def main():
    sendEmail("sruthisudhakar81@gmail.com", "yo")
    reverseGeocode()

if __name__ == "__main__": main()
