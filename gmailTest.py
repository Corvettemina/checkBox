import base64
from email.message import EmailMessage
import pickle
import os.path
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

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
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()
        
        message.add_header('Content-Type', 'text/html')  # Set the content type to HTML
        
        message.set_content(
            f'<html>'
            f'<body>'
            f'<p>Powerpoint selections for this Sunday are ready for review.</p>'
            f'<p><a href="https://stmark-service.web.app/vespers?date={date}">Vespers Link</a></p>'
            f'<p>Vespers Doxologies:<br>'
            f'{",<br>".join(database[date]["vespers"]["seasonVespersDoxologies"])}</p>'
            f'<p>Matins Doxologies:<br>'
            f'{",<br>".join(database[date]["matins"]["seasonmatinsDoxologies"])}</p>'
            f'</body>'
            f'</html>'
        )
        
        with open("/root/Dropbox/PowerPoints/configs/emails.json", "r") as json_file:
            recipients = json.load(json_file)
        
        message['To'] = ", ".join(recipients)  # Join recipients as a comma-separated string
        message['From'] = 'Mina Hanna'
        message['Subject'] = 'Powerpoint For Sunday ' + str(date)
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {
            'raw': encoded_message
        }
        
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')
        send_message = None
    return send_message

if __name__ == '__main__':

    gmail_send_message()
