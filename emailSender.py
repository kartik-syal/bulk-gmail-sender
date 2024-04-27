import os
import csv
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# Configure logging
logging.basicConfig(filename='email_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CSV_FILE_PATH = 'recipients.csv'  # Update with your CSV file path
EMAIL_SUBJECT = """Shamora's Exclusive Premium Top Collection!"""
EMAIL_BODY = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shamora Exclusive Top</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #354159;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      margin: 20px auto;
      padding: 20px;
      background-color: #E9E7CD;
      border-radius: 10px;
      position: relative;
    }
    .promo-text {
      text-align: center;
      font-size: 18px;
      margin-bottom: 20px;
      color: #354159;
    }
    .product-img-container {
      position: relative;
    }
    .brand-logo {
      position: absolute;
      top: 10px;
      left: 10px;
      max-width: 100px;
      height: auto;
    }
    .product-img {
      display: block;
      margin: 0 auto;
      max-width: 100%;
      height: auto;
      border-radius: 10px;
    }
    .coupon-code {
      text-align: center;
      font-size: 20px;
      color: #e74c3c;
      margin-top: 20px;
      margin-bottom: 10px;
    }
    .coupon-code strong {
      background-color: #f2dede;
      padding: 2px 5px;
      border-radius: 5px;
    }
    .cta-btn {
      display: block;
      width: 50%;
      margin: 20px auto;
      padding: 10px 20px;
      background-color: #e74c3c;
      color: #fff;
      text-align: center;
      text-decoration: none;
      border-radius: 5px;
      font-size: 16px;
    }
    .social-icons {
      text-align: center;
      margin-top: 20px;
    }
    .social-icons a {
      display: inline-block;
      /* margin-right: 10px; */
    }
    .social-icons p {
      margin-top: 5px;
      font-size: 14px;
      color: #354159;
      display: inline-block;
      vertical-align: middle;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="promo-text">
      <p>Introducing Shamora's Exclusive Top Collection!</p>
      <p>Get your hands on our latest top designs - perfect for any occasion!</p>
    </div>
    <div class="product-img-container">
      <a href="https://www.whatsapp.com/product/8096531453695250/919578399000/?app_absent=0" target="_blank">
        <img class="product-img" src="https://lh3.googleusercontent.com/pw/AP1GczMg06H6sEtSOYEE3EGnaCzludCZMlu1v24gle-sHCgCFTXqPHRIl1HAXp22-dw3gWnpSNlRPWIFBgBxXnxyfV1wsIGN6YiobON38YfjUgWdByjb8iFq2uUwdNTpZSeMuuyQ85AgwD6yTTlt5I2QceU=w693-h923-s-no-gm?authuser=0" alt="Shamora Top">
      </a>
    </div>
    <div class="coupon-code">
      <p>Check out our collection now!</p>
    </div>
    <div class="cta-btn">
      <a href="https://www.whatsapp.com/product/8096531453695250/919578399000/?app_absent=0" target="_blank" style="text-decoration: none; color: #fff;">Shop on WhatsApp</a>
    </div>
    <div class="social-icons">
      <p style="font-size: 20px; padding-top: 5px;">Also available on Amazon</p>
      <a href="https://amzn.in/d/8iQwrhE" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/15466/15466027.png" alt="Amazon" style="width: 40px; height: 40px; vertical-align: middle; padding: 5px;">
      </a>
    </div>
    <div class="social-icons">
      <p style="margin-right: 10px;">
        <a href="https://instagram.com/shamoraclothing?igshid=OGQ5ZDc2ODk2ZA==" target="_blank">
          <img src="https://cdn-icons-png.flaticon.com/512/174/174855.png" alt="Instagram" style="width: 30px; height: 30px; vertical-align: middle;">
        </a>
        <a href="https://instagram.com/shamoraclothing?igshid=OGQ5ZDc2ODk2ZA==" target="_blank">@shamoraclothing</a>
      </p>
      <p>
        <a href="https://wa.me/message/34VBRAOC3HPJO1" target="_blank">
          <img src="https://cdn-icons-png.flaticon.com/512/4423/4423697.png" alt="WhatsApp" style="width: 30px; height: 30px; vertical-align: middle;">
        </a>
        <a href="https://wa.me/message/34VBRAOC3HPJO1" target="_blank">+91-95783-99000</a>
      </p>
    </div>
  </div>
</body>
</html>
"""
CREDENTIALS_FILE = 'credentials.json'  # Update with your credentials file path
SENDER_EMAIL = 'shamoraclothing@gmail.com'  # Update with your email address

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=4800)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text, 'html')
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    raw_message = raw_message.decode()
    return {'raw': raw_message}

def send_message(service, user_id, message,recipient_email):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        logging.info('Message Id: %s - Sent to: %s - Message response: %s' % (message.get('id', 'Unknown'), recipient_email, message))
        return True
    except Exception as e:
        logging.error('An error occurred: %s - Failed to send email to: %s' % (e, recipient_email))
        return False

def main():
    # Authenticate and create the Gmail service
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    # Read CSV file and send emails
    with open(CSV_FILE_PATH, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipient_email = row['email']
            message = create_message(SENDER_EMAIL, recipient_email, EMAIL_SUBJECT, EMAIL_BODY)
            if send_message(service, 'me', message, recipient_email):
                print(f"Email sent successfully to: {recipient_email}")
            else:
                print(f"Failed to send email to: {recipient_email}")

if __name__ == '__main__':
    main()
