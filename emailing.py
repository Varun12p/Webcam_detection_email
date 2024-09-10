import smtplib
import imghdr
from email.message import EmailMessage
from threading import Thread

PASSWORD = "ghqfysqartnzjeqz"
SENDER = "panjwanivarun12@gmail.com"
RECEIVER = "panjwanivarun12@gmail.com"


def send_email(image_path):
    email_msg = EmailMessage()
    email_msg["Subject"] = "New Object detected."
    email_msg.set_content("Hey, check the activity.")

    with open(image_path,'rb') as file:
        content = file.read()
    email_msg.add_attachment(content, maintype="image", subtype=imghdr.what(None,content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER, email_msg.as_string())

    gmail.quit()

if __name__ == "__main__":
    send_email("images/image10.png")


