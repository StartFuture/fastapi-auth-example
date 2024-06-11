import smtplib
import email.message
from email.mime.text import MIMEText
import logging

from passlib.context import CryptContext

from app import parameters


crypt = CryptContext(schemes=['bcrypt'], deprecated="auto")


def create_hash(password: str):
    return crypt.hash(password)


def check_pwd_hash(password_hash: str, password: str):
    return crypt.verify(password, password_hash)


def send_email(client_email: str, layout_email: str, context: str):

    try:

        msg = email.message.Message()
        msg['Subject'] = context
        msg['From'] = parameters.EMAIL_NAME
        msg['To'] = client_email
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(layout_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], parameters.EMAIL_PASSWORD)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    
    except Exception as error:

        logging.warning(error)
        return False

    else:

        return True
