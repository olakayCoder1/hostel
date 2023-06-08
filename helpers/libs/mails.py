import smtplib
import asyncio 
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import  urlsafe_base64_encode   


class environ():
    class Env():
        class read_env():
            pass 


env = environ.Env() 
environ.Env.read_env()

# sender_email = env('EMAIL_SENDER')
# password = env('EMAIL_PASSWORD')

sender_email = 'kkkk'
password = 'kkkkk'


class MailServices:

    sender_email = 'kkkk'
    password = 'kkkkk'

    @staticmethod
    def forget_password_mail(user):
        """
        This method sends a mail to the user to reset his/her password
        """
        receiver_email = user.email
        token = PasswordResetTokenGenerator().make_token(user)
        uuidb64 = urlsafe_base64_encode(force_bytes(user.id))
        message = MIMEMultipart("alternative")
        message["Subject"] = "Password Reset Request"
        message["From"] = sender_email
        message["To"] = receiver_email
        reset_link = f'http://127.0.0.1:3000/password/{token}/{uuidb64}/reset'
        print('***'*100)
        print(reset_link)
        print('***'*100)
        html = render_to_string('accounts/password-reset-mail.html', {'reset_link': reset_link})
        part = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        message.attach(part)
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )







