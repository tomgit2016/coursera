from email.message import EmailMessage
import os.path
import mimetypes

message = EmailMessage()
sender = "me@example.com"
recipient = "you@example.com"
message['From'] = sender
message['To'] = recipient
message['Subject'] = 'Greetings from {} to {}!'.format(sender, recipient)
body = """Hey there!

I'm learning to send emails using Python!"""
message.set_content(body)
attachment_path = "/tmp/example.png"
attachment_filename = os.path.basename(attachment_path)
mime_type, _ = mimetypes.guess_type(attachment_path)
mime_type, mime_subtype = mime_type.split('/', 1)
print(mime_subtype)

