from __future__ import print_function

import base64
from email.message import EmailMessage
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
def gmail_send_message(date):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    USETOKEN= 'tokenMina.pickle'
    USECRED = 'credentials.json'
    creds = None
    if os.path.exists(USETOKEN):
        with open(USETOKEN, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                USECRED, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(USETOKEN, 'wb') as token:
            pickle.dump(creds, token)


    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('Powerpoint selections for this Sunday is ready for review.\n'+
                            'https://stmark-service.web.app/vespers?date=' + date)

        message['To'] = ['mina.h.hanna@gmail.com',"tonyislame67@gmail.com","msorail98@gmail.com"]
        message['From'] = 'Mina Hanna'
        message['Subject'] = 'Powerpoint For Sunday '+ str(date)

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


if __name__ == '__main__':
    gmail_send_message()