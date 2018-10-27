import mimetypes
import smtplib  # smtplib modulunu projemize ekledik
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Mailer.Logger import Logger
class Mail:

    def __init__(self, username, password,who='',smtp='smtp.gmail.com:587',ssl=False):
        self.who=who
        self.ssl=ssl
        self.smtp=smtp
        self.headers = [
            # ['Precedence', 'bulk'],
            ['List-Unsubscribe', 'http://hilbet.com/unsubscribe'],
            ['Content-Location','tr-Turkey'],
            ['Content-Language','tr-Tr'],
            ['Accept-Language','tr-Tr'],
            # ["X-Priority","5 (Low)"],
            # ['Reply-To','Gaming Bulten<bulten@hilbet.com>']

        ]
        self.serverInit()
        self.login(username, password)

    def serverInit(self):
        try:
            if self.ssl:
                self.server = smtplib.SMTP_SSL(self.smtp)
                # self.server.starttls()
                self.server.ehlo()
            else:
                self.server = smtplib.SMTP(self.smtp)
                self.server.starttls()
                self.server.ehlo()
        except smtplib.SMTPConnectError as e:
            raise smtplib.SMTPConnectError

    def login(self, username, password):
        try:
            self.server.login(username, password)
            self.who=username
            print(username," login olundu")
        except smtplib.SMTPAuthenticationError as e:
            raise e

    def serverQuit(self):
        self.server.close()

    def send(self, recipent, filename='', subject="", message=""):
        outer = MIMEMultipart()
        outer['From'] = self.who
        outer['To'] = recipent
        outer['Subject'] = subject
        outer.attach(MIMEText(message, 'html'))
        print(self.who)
        for header in self.headers:
            outer.add_header(*header)

        if filename is not  '':
            path = filename
            # dosyanın türünü tahmin edip ona göre type belirliyoruz
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()

            elif maintype == 'image':
                fp = open(path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()

            elif maintype == 'audio':
                fp = open(path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()

            else:
                fp = open(path, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                """eğer yukarıdakilerden biri değilse mesajı base64 olarak encoded
                texte çevirip mesaja ekliyoruz"""
                # encoders.encode_base64(msg)

            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            outer.attach(msg)

        # oluşturduğumuz text, html ve file datasını string olarak alıyoruz

        composed = outer.as_string()
        try:

            self.server.sendmail(self.who,[recipent], composed)
            self.server.set_debuglevel(1)
            Logger("Sender:{0} | Recipent:{1}, OK".format(self.who,recipent))

            return True


        except smtplib.SMTPAuthenticationError as hata:
            print("e-posta veya şifrenizi yanlış girdiniz.",
                  "orjinal hata iletisi: ", hata)
            raise smtplib.SMTPAuthenticationError(44, "444")
        except smtplib.SMTPConnectError as e:
            raise e
        except smtplib.SMTPSenderRefused as e:
            raise e
