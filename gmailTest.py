from __future__ import print_function

import base64
from email.message import EmailMessage
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
def gmail_send_message(date, database):
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    USETOKEN = 'tokenMina.pickle'
    USECRED = 'credentials.json'
    creds = None
    
    if os.path.exists(USETOKEN):
        with open(USETOKEN, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(USECRED, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(USETOKEN, 'wb') as token:
            pickle.dump(creds, token)

    try:
        with open("/root/Dropbox/PowerPoints/configs/emails.json", "r") as json_file:
            recipients = json.load(json_file)
        
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        message['To'] = ", ".join(recipients)
        message['From'] = 'Mina Hanna'
        message['Subject'] = 'Powerpoint For Sunday ' + str(date)

        # Create the HTML content
        html_content = f'''
        <html>
        <head></head>
        <body>
            <p>Powerpoint selections for this Sunday are ready for review.</p>
            <p><a href="https://stmark-service.web.app/vespers?date={date}">Vespers Link</a></p>
            <p>Vespers Doxologies:</p>
            <ul>
                {"".join([f"<li>{doxology}</li>" for doxology in database[date]['vespers']['seasonVespersDoxologies']])}
            </ul>
            <p>Matins Doxologies:</p>
            <ul>
                {"".join([f"<li>{doxology}</li>" for doxology in database[date]['matins']['seasonmatinsDoxologies']])}
            </ul>
        </body>
        </html>
        '''

        message.set_content(html_content, subtype='html')

        # Encode the message as base64
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'raw': encoded_message
        }

        # Send the message using Gmail API
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    gmail_send_message()