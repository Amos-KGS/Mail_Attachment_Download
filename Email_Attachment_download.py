import imaplib # Install by running pip install imaplib
import email
import os

EMAIL = 'recipient@gmail.com' # Recipient's Email Address
PASSWORD = 'cixgmzrmjipyigoi' # App password: generated when 2-factor authentication is enabled (not email password)
SERVER = 'imap.gmail.com' # Mail server

SAVE_FOLDER = r"C:\Maildownloads" # Local/network folder to dump the attachments


SENDER_EMAIL = 'Sender@gmail.com' # Sender email address

mail = imaplib.IMAP4_SSL(SERVER) # Establishing connection to mail account

# print(f"Email: {EMAIL}, Password: {PASSWORD}") - /* For debugging purposes */

mail.login(EMAIL, PASSWORD) # Login to email address

mail.select('Inbox') # Specify the mail destination tab

status, messages = mail.search(None, f'(FROM "{SENDER_EMAIL}")', '(UNSEEN)') # Search for emails with attachments from the specific sender

for msg_id in messages[0].split():

    # Get the email message
    _, data = mail.fetch(msg_id, '(RFC822)')
    email_message = email.message_from_bytes(data[0][1])

    # Download the attachment
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            filepath = os.path.join(SAVE_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(part.get_payload(decode=True))
                print(f'Downloaded {filename} to {SAVE_FOLDER}')