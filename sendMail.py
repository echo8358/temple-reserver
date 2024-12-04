# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def sendEmail(email: str, subject: str, text: str):
    msg = MIMEText(text)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = 'root@echobase.org'
    msg['To'] = email

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('192.168.1.5')
    s.sendmail('temples@echobase.org', [email], msg.as_string())
    s.quit()
