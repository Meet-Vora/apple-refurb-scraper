from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

###############

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from googleapiclient import errors

import data_wrapper

# If modifying these scopes, delete the file token_emailer.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.send']
PERS_EMAIL = data_wrapper.get_email()


def send_email(email_subject, msg_txt, email):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    Args:
        email_subject: subject of email
        msg_txt: String message to send to each email ID
        email: email ID to send email to
    """
    creds = None
    # The file token_emailer.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token_emailer.pickle'):
        with open('token_emailer.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token_emailer.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    message = CreateMessage(PERS_EMAIL, email, email_subject, msg_txt)
    SendMessage(service, "me", message)


def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
                 can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        # pass
        print('An error occurred: ', error)


def CreateMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
    # return {'raw': base64.urlsafe_b64encode(message.as_string())}

    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])


##############################################################################################

# from gmail_api_wrapper.crud.write import GmailAPIWriteWrapper

# class Test:
#     def set_store(self, yeet):
#         print(vars(yeet))
#         return 'lol'

#     invalid = 'beast'

# class EmailClass:
#     def from_json(self):
#         return Test()

# def send_email():

#     api = GmailAPIWriteWrapper()

#     body = """
#            # body of the email goes here. And send them a link based on their email account using the comaparer file
#            """

#     # get email from comparer here
#     emails = "projectbitfix@gmail.com"

#     # compose new mail
#     api.compose_mail(subject='Your Daily BitFix Project Issues!', body=body, to=emails)
# send_email("subject", "hellooooo testing", PERS_EMAIL)
