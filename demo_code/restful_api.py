import os
import datetime
import binascii
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import psycopg2

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
                './client_secret_988561347664-o3ds4lv2m2pcp6aklargpn2s8umi6hr7.apps.googleusercontent.com.json', SCOPES)
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


# Create and open the database for writing

def create_table():
# Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="saimasharleen",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table with two columns (column1, column2 and column3) to store the data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nope (
            sender TEXT,
            receiver TEXT,
            date TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def start_api_service():
    if __name__ == "__main__":
        start_date_str = "2023-08-01"
        end_date_str = "2023-08-24"

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        query_inbox = "is:inbox category:primary"  
        query_sent = "is:sent"

        # Create an empty dictionary to store the email-to-identifier mapping
        email_mapping = {}

        owner_identifier = None

        email_data = []

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

            email_data.append((sender, owner_identifier, date))

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
            email_data.append((owner_identifier, receiver, date))
        return email_data


# INSERT DATA INTO TABLE

def insert_data(data_list):
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        database="saimasharleen",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Insert the data into the table
    for data in data_list:
        # Assuming data is a tuple with two elements (data for sender and receiver)
        cursor.execute('INSERT INTO nope (sender, receiver, date) VALUES (%s, %s, %s)', data)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Data to be inserted into the database
email_data = start_api_service()
data_to_insert = email_data

create_table()

# Insert the data into the table
insert_data(data_to_insert)


import csv

# Sample data as a list of tuples (FromNodeId, ToNodeId, Date)
data = email_data

# Define the name of the CSV file
csv_file = "data.csv"

def write_data(data):
    # Write data to the CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header
        writer.writerow(["from_node_id", "to_node_id", "Date"])
        
        # Write the data rows
        for row in data:
            writer.writerow(row)
