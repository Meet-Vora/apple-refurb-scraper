import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from data_wrapper import get_from_email, get_to_email


def send_email(content):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(content)
        message['To'] = get_to_email()
        message['From'] = get_from_email()
        message['Subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        # create and send message
        create_message = { 'raw': encoded_message }
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print('Message Id: {send_message["id"]}')
    except HttpError as error:
        print('An error occurred: {error}')
        send_message = None

    return send_message
