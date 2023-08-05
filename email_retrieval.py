import os
import datetime
import csv
import binascii
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_gmail_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:/Users/aless/Desktop/big_data_proj/client_secret_988561347664-o3ds4lv2m2pcp6aklargpn2s8umi6hr7.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def hash_email(email, email_mapping):
    # If the email is already in the mapping, return its identifier
    if email in email_mapping:
        return email_mapping[email]

    # If the email is not in the mapping, assign a new identifier and add it to the mapping
    identifier = len(email_mapping) + 1
    email_mapping[email] = identifier
    return identifier

def retrieve_emails(query, start_date=None, end_date=None):
    service = get_gmail_service()

    if start_date:
        query += f" after:{start_date.strftime('%Y/%m/%d')}"
    if end_date:
        query += f" before:{end_date.strftime('%Y/%m/%d')}"

    results = service.users().messages().list(userId='me', q=query).execute()
    messages = []
    if 'messages' in results:
        messages.extend(results['messages'])
    while 'nextPageToken' in results:
        page_token = results['nextPageToken']
        results = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        if 'messages' in results:
            messages.extend(results['messages'])
    return messages


if __name__ == "__main__":
    start_date_str = "2023-07-01"
    end_date_str = "2023-07-31"

    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    query_inbox = "is:inbox category:primary"  
    query_sent = "is:sent"

    # Create an empty dictionary to store the email-to-identifier mapping
    email_mapping = {}

    owner_identifier = None

    # Create and open the CSV file for writing
    with open('emails_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow(['Sender', 'Receiver', 'Date'])

        # Process 'is inbox' results
        inbox_emails = retrieve_emails(query_inbox, start_date, end_date)
        for email in inbox_emails:
            message = get_gmail_service().users().messages().get(userId='me', id=email['id']).execute()
            headers = message['payload']['headers']

            sender = None
            receiver = None
            date = ''

            for header in headers:
                if header['name'] == 'From':
                    sender = hash_email(header['value'], email_mapping)
                elif header['name'] == 'To':
                    receiver = hash_email(header['value'], email_mapping)
                elif header['name'] == 'Date':
                    date_str = header['value']

                    # Try multiple date formats until we find a match
                    date_formats = ["%d %b %Y %H:%M:%S", "%a, %d %b %Y %H:%M:%S %z"]
                    for date_format in date_formats:
                        try:
                            parsed_date = datetime.datetime.strptime(date_str, date_format)
                            date = parsed_date.strftime("%Y-%m-%d")
                            break
                        except ValueError:
                            continue

            # Set the email log owner's identifier for 'is inbox' results
            if owner_identifier is None:
                owner_identifier = receiver

            # Write the email data to the CSV file
            csvwriter.writerow([sender, receiver, date])

        # Process 'is sent' results
        sent_emails = retrieve_emails(query_sent, start_date, end_date)
        for email in sent_emails:
            message = get_gmail_service().users().messages().get(userId='me', id=email['id']).execute()
            headers = message['payload']['headers']

            sender = None
            receiver = None
            date = ''

            for header in headers:
                if header['name'] == 'From':
                    sender = hash_email(header['value'], email_mapping)
                elif header['name'] == 'To':
                    receiver = hash_email(header['value'], email_mapping)
                elif header['name'] == 'Date':
                    date_str = header['value']

                    # Try multiple date formats until we find a match
                    date_formats = ["%d %b %Y %H:%M:%S", "%a, %d %b %Y %H:%M:%S %z"]
                    for date_format in date_formats:
                        try:
                            parsed_date = datetime.datetime.strptime(date_str, date_format)
                            date = parsed_date.strftime("%Y-%m-%d")
                            break
                        except ValueError:
                            continue

            # Set the email log owner's identifier for 'is sent' results
            sender = owner_identifier

            # Write the email data to the CSV file
            csvwriter.writerow([sender, receiver, date])

    print("Data has been successfully written to 'emails_data.csv'.")
