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
                /* Bold titles and increase text size */
                .container h1 {{
                    font-weight: bold;
                    font-size: 16px;
                }}
                .container h2 {{
                    font-weight: bold;
                    font-size: 14px;
                }}
                /* Add more styles as needed */
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Powerpoint selections for this Sunday are ready for review.</h1>
                <h1><a href="https://stmark-service.web.app/vespers?date={date}">Vespers</a></h1>
                <h2>Vespers Doxologies:<br></h2><p>
                {"  ,<br>     ".join(database[date]['vespers']['seasonVespersDoxologies'])}</p>
                <h2>Vespers Litany of the Gospel:<br></h2>
                <p>{database[date]['vespers']['vespersLitanyofTheGospel']}</p>
                <h2>Vespers 5 Short Litanies:<br></h2>
                <p>{database[date]['vespers']['vespers5ShortLitanies']}</p>

                <h1><a href="https://stmark-service.web.app/matins?date={date}">Matins</a></h1>
                <h2>Matins Doxologies:<br></h2><p>
                {"  ,<br>     ".join(database[date]['matins']['seasonmatinsDoxologies'])}</p>
                <h2>Matins Litany of the Gospel:<br></h2>
                <p>{database[date]['matins']['matinsLitanyofTheGospel']}</p>
                <h2>Matins 5 Short Litanies:<br></h2>
                <p>{database[date]['matins']['matins5ShortLitanies']}</p>
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
        #with open("/root/Dropbox/PowerPoints/configs/emails.json", "r") as json_file:
            #recipients = json.load(json_file)
            
        message = MIMEMultipart()
        message['To'] = "mina.h.hanna@gmail.com"
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
