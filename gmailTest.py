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
import requests

def create_html_email(date, database):
    response = requests.get(
                'https://stmarkapi.com:8080/home/?date=' + date , verify=False)
            
    y = json.loads(response.text)

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
                background-image: url('background.jpg');
                background-size: cover; /* Adjust as needed */
                background-position: center center; /* Adjust as needed */
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
            .grid-container {{
                display: inline-block;
                flex-direction: column;
                align-items: center; /* Center horizontally */
                gap: 20px;
                margin:0 auto;
            }}
            .grid-item {{
                flex: 0 0 calc(50% - 20px); /* Two items per row, accounting for gap */
                background-color: #ffffff;
                padding: 10px;
                border: 1px solid #e0e0e0;
            }}

                /* Add more styles as needed */
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Powerpoint selections for this Sunday, {date} are ready for review.</h1>
                <div class="grid-container">
                    <div class="grid-item"><h2>{y["copticDate"]}</h2><h2>{y["sunday"]}</h2></div>
                    <div class="grid-item"><h2>{y["ocassion"]}</h2><h2>{y["season"]}</h2></div>
                </div>
                <h1><a href="https://stmark-service.web.app/vespers?date={date}">Vespers</a></h1>
                <h2>Vespers Doxologies:</h2>
                '''
    for i in database[date]['vespers']['seasonVespersDoxologies']:
        doxo = i.split("/")[-1]
        html_content += f'''
        <br>{doxo}</br>
        '''
               
    
    if database[date]['vespers']['vespersLitanyofTheGospel'] == "alternate":
        alternate_content = f'''
         <h2>Vespers Litany of the Gospel:</h2>
        <p>{database[date]['vespers']['vespersLitanyofTheGospel']}</p>
        '''
        html_content += alternate_content
    
    if database[date]['vespers']['vespers5ShortLitanies'] == "yes":
        alternate_content = f'''
        <h2>Vespers 5 Short Litanies:</h2>
        <p>{database[date]['vespers']['vespers5ShortLitanies']}</p>
        '''
        html_content += alternate_content
          
    html_content += f'''    
                
                <h1><a href="https://stmark-service.web.app/matins?date={date}">Matins</a></h1>
                <h2>Matins Doxologies:</h2>
                '''
    for i in database[date]['matins']['seasonmatinsDoxologies']:
        doxo = i.split("/")[-1]
        html_content += f'''
        <br>{doxo}</br>
        '''
               
    if database[date]['matins']['matinsLitanyofTheGospel'] == "alternate":
        alternate_content = f'''
                <h2>Matins Litany of the Gospel:</h2>
                <p>{database[date]['matins']['matinsLitanyofTheGospel']}</p>
        '''
        html_content += alternate_content
    
    if database[date]['matins']['matins5ShortLitanies'] == "yes":
        alternate_content = f'''
            <h2>Matins 5 Short Litanies:</h2>
            <p>{database[date]['matins']['matins5ShortLitanies']}</p>
        '''
        html_content += alternate_content

    if ("paralexHymns" in database[date]['liturgyOfWord']):
        alternate_content = f'''
        <h1><a href="https://stmark-service.web.app/liturgyOfWord?date={date}">Liturgy Of the Word</a></h1>
        <h2>Paralex Hymns:<br><p>
        '''
        html_content += alternate_content
        for i in database[date]['liturgyOfWord']['paralexHymns']:
            doxo = i.split("/")[-1]
            html_content += f'''
            <br>{doxo}</br>
            '''

    toRender = database[date]['liturgyOfFaithful']['prayerOfReconcilation'][0].split("/")[-1]
    html_content += f'''
    <h1><a href="https://stmark-service.web.app/liturgyOfFaithful?date={date}">Liturgy Of the Faithful</a></h1>
    <h2>Reconcilation Prayer:</h2>
    <p>{toRender}</p>
    '''

    if database[date]['liturgyOfFaithful']['rejoiceOMary'] == "yes":
        alternate_content = f'''
            <h2>Rejoice O Mary:</h2>
            <p>{database[date]['liturgyOfFaithful']['rejoiceOMary']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['anaphora'] == "gregory":
        alternate_content = f'''
            <h2>Anaphora:</h2>
            <p>{database[date]['liturgyOfFaithful']['anaphora']}</p>
        '''
        html_content += alternate_content
        
    if database[date]['liturgyOfFaithful']['OLordofHosts'] == "yes":
        alternate_content = f'''
            <h2>O Lord of Hosts:</h2>
            <p>{database[date]['liturgyOfFaithful']['OLordofHosts']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['agiosLiturgy'] == "gregory":
        alternate_content = f'''
        <h2>Agios:</h2>
        <p>{database[date]['liturgyOfFaithful']['agiosLiturgy']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['instiution'] == "gregory":
        alternate_content = f'''
        <h2>Instiution Narrative:</h2>
        <p>{database[date]['liturgyOfFaithful']['instiution']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['yeahWeAskYou'] == "yes":
        alternate_content = f'''
        <h2>Yes We Ask You...:</h2>
        <p>{database[date]['liturgyOfFaithful']['yeahWeAskYou']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['jeNaiNan'] == "yes":
        alternate_content = f'''
        <h2>Je Nai Nan:</h2>
        <p>{database[date]['liturgyOfFaithful']['jeNaiNan']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['healingToThesick'] == "yes":
        alternate_content = f'''
        <h2>Healing To The Sick...:</h2>
        <p>{database[date]['liturgyOfFaithful']['healingToThesick']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['Commemoration'] == "gregory":
        alternate_content = f'''
        <h2>Commemoration:</h2>
        <p>{database[date]['liturgyOfFaithful']['Commemoration']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['postCommemoration'] == "gregory":
        alternate_content = f'''
        <h2>Post Commemoration:</h2>
        <p>{database[date]['liturgyOfFaithful']['postCommemoration']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['prefaceToTheFraction'] == "gregory":
        alternate_content = f'''
        <h2>Preface to The Fraction:</h2>
        <p>{database[date]['liturgyOfFaithful']['prefaceToTheFraction']}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['seasonalFraction'][0] != "":
        toRender = database[date]['liturgyOfFaithful']['seasonalFraction'][0].split("/")[-1]
        alternate_content = f'''
        <h2>Fraction:</h2>
        <p>{toRender}</p>
        '''
        html_content += alternate_content

    if database[date]['liturgyOfFaithful']['fractionIndex'][0] != "":
        toRender = database[date]['liturgyOfFaithful']['fractionIndex'][0].split("/")[-1]
        alternate_content = f'''
        <h2>Fraction:</h2>
        <p>{toRender}</p>
        '''
        html_content += alternate_content

    html_content += f'''
    <h1><a href="https://stmark-service.web.app/communion?date={date}">Communion</a></h1>
    <h2>Communion Hymns:</h2>
    '''

    for i in database[date]['communion']['communionHymns']:
        doxo = i.split("/")[-1]
        html_content += f'''
        <br>{doxo}</br>
        '''
    for i in database[date]['communion']['AllCommunionHymns']:
        doxo = i.split("/")[-1]
        html_content += f'''
        <br>{doxo}</br>
        '''

    html_content += f'''
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
        message['To'] = ",".join(recipients)
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
