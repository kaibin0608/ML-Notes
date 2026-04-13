# Give access to third part apps in gmail security settings

import smtplib

def setup_server():
    # Port 587 is the standard port for sending email securely
    server = smtplib.SMTP(host = 'smtp.gmail.com', port = 587) # is like a post office, connect to Gmail's post office
    # Without this, your password and email content would be sent as plain text — anyone could intercept it.
    server.starttls() # Encrypt the connection (required before login)
    return server

def login(server): 
    address = input("Sender Email: ").strip()
    password = input("Password: ").strip()
    server.login(address, password) # Authenticate
    return address

def create_email(address):
    from email.mime.multipart import MIMEMultipart # MIMEMultipart — creates an email that can hold multiple parts (text + attachments).
    from email.mime.text import MIMEText # MIMEText — represents a plain text body. Imported here but not actually used yet (incomplete code).

    recipient_email = input("Enter recipient email: ").strip()

    msg = MIMEMultipart()

    # setup parameters
    msg['From'] = address
    msg['To'] = recipient_email
    msg['Subject'] = input("Enter subject of the message: ").strip()

    message = input("Enter message: ").strip()
    msg.attach(MIMEText(message, 'plain'))
    attach = input("Would you like to send an attachment? (y/n): ").strip().lower()
    num_attach = int(input("Enter number of attachments: "))

    i=0
    while i<num_attach:
        if attach =='y':
            # add an attachment
            i += 1
        elif attach == 'n':
            # no attachment
            i += 1
    return msg

def send(server,msg):
    from email import message
    server.send_message(msg) # Send a MIMEText/MIMEMultipart message, handover the email - Gmail does the rest
    del msg
    print("Email sent successfully")

def add_attachment(msg):
    from email.mime.base import MIMEBase
    from email import encoders

    filename = input("Enter path of the attachment file: ").strip() #absolute
    file = open(filename, 'rb') # Open the file in Binary read mode

    attachment = MIMEBase('application', 'octet-stream') # Creates a generic binary attachment container. octet-stream means "raw binary file of any type".

    attachment.set_payload(file.read()) # Puts the file's contents into the attachment.

    encoders.encode_base64(attachment) # Converts the binary file to Base64 — email was designed for text, so binary files must be encoded to text-safe format before sending.
    attachment.add_header(
        'Content-Disposition', #  tells the email client how to display this part (as a downloadable attachment, not inline)
        'attachment', # confirms it's an attachment
        filename=filename # tells the recipient's email client what to name the file when they download it
        )

    msg.attach(attachment)
    print("Attachment has been added") 

# Execute
server = setup_server()
address = login(server)
msg = create_email(address)
send(server,msg)
