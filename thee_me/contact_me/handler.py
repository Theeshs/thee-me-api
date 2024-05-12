import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from thee_me.contact_me.types import MessageRequest
from thee_me.models.user import Emails


async def send_email(
    from_addr, to_addr=None, subject=None, body=None, password=None, cc=None
):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        if cc:
            msg["CC"] = cc
            msg["BCC"] = cc

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


async def save_email_data(db: Session, email_request: MessageRequest) -> Emails:
    """Save email data to database"""
    new_email = Emails(**email_request.dict())
    db.add(new_email)
    await db.commit()
    await db.refresh(new_email)
    return new_email
