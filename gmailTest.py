from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import pickle
import os.path
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def create_html_email(date, database):
    html_content = f'''
    <html>
    <head>
        <style>
            /* Inline CSS styles */
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
            }}
            /* Add more styles as needed */
        </style>
    </head>
    <body>
        <div class="container">
            <p>Powerpoint selections for this Sunday are ready for review.</p>
            <p><a href="https://stmark-service.web.app/vespers?date={date}">St. Mark PowerPoint Editor</a></p>
            <p>Vespers Doxologies:<br>
            {",<br>".join(database[date]['vespers']['seasonVespersDoxologies'])}</p>
            <p>Matins Doxologies:<br>
            {",<br>".join(database[date]['matins']['seasonmatinsDoxologies'])}</p>
        </div>
    </body>
    </html>
    '''
    return html_content

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
        with open("/root/Dropbox/PowerPoints/configs/emails.json", "r") as json_file:
            recipients = json.load(json_file)
        message = MIMEMultipart()
        message['To'] = ", ".join(recipients)
        message['From'] = 'Mina Hanna'
        message['Subject'] = 'Powerpoint For Sunday ' + str(date)
        
        html_content = create_html_email(date, database)
        message.attach(MIMEText(html_content, 'html'))  # Attach HTML content
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_message = {
            'raw': raw_message
        }
        
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':

    gmail_send_message()
