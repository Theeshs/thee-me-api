import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


async def send_email(from_addr, to_addr=None, subject=None, body=None, password=None):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject

        # Turn these into plain MIMEText objects
        part1 = MIMEText(body, "plain")

        # Add the plain-text parts to the MIMEMultipart message
        # The email client will try to render the last part first
        msg.attach(part1)

        # Connect to the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_addr, password)

        # Send the email
        server.sendmail(from_addr, to_addr, msg.as_string())

        # Close the SMTP server connection
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False
