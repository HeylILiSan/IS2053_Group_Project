"""EMAIL CLIENT FOR TESTING"""

import smtplib
from email.message import EmailMessage

msg = EmailMessage() # creates a message object
msg.set_content("Hello World!") # sets body content of email
msg['Subject'] = 'Testing connection' # sets the subject line
msg['From'] = 'sender@example.com' # sets the sender
msg['To'] = 'recipient@example.com' # sets the recipient

with smtplib.SMTP('127.0.0.1', 8025) as client: # initializes email client
    client.send_message(msg)
    print("Email sent")