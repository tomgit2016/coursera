from email.message import EmailMessage
import os.path
import mimetypes
import smtplib


def generate_email(sender, recipient, subject, body, attachment):
    message = EmailMessage()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.set_content(body)
    attachment_path = attachment
    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    # print(mime_subtype)
    with open(attachment_path, 'rb') as ap:
        message.add_attachment(ap.read(),
                               maintype=mime_type,
                               subtype=mime_subtype,
                               filename=os.path.basename(attachment_path))
    return message


def send_email():
    mail_server = smtplib.SMTP('localhost')
    mail_server.login("user", "pass")
    subject_line = "Upload Completed - Online Fruit Store"
    email_body = 'All fruits are uploaded to our website successfully. A detailed list is attached to this email.'
    attachment_file = "/tmp/processed.pdf"
    message = generate_email("automation@example.com", "to", subject_line, email_body, attachment_file)
    mail_server.send_message(message)

