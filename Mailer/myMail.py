import mimetypes
import smtplib  # smtplib modulunu projemize ekledik
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Utils.Logger import Logger
from email.utils import formatdate


class Mail:

    def __init__(self, username, password, who='', smtp='smtp.gmail.com:587', ssl=False):
        self.who = who
        self.ssl = ssl
        self.smtp = smtp
        self.headers = [
            ['Precedence', 'bulk'],
            # ['List-Unsubscribe', ''],
            ['List-Unsubscribe', '<mailto:{}>'],
            ['Content-Location', 'tr-Turkey'],
            ['Content-Language', 'tr-Tr'],
            ['Accept-Language', 'tr-Tr'],
            ['Date', formatdate()],
            # ["X-Priority","1 (High)"],

            ['Reply-To', 'Destek<{}>']

        ]
        self.serverInit()
        # self.login(username, password)

    def serverInit(self):
        try:
            if self.ssl:
                self.server = smtplib.SMTP_SSL(self.smtp)
                # self.server.starttls()
                self.server.ehlo()
            else:
                self.server = smtplib.SMTP(self.smtp)
                #self.server.set_debuglevel(1)
                self.server.ehlo()
                self.server.starttls()
        except smtplib.SMTPConnectError as e:
            raise smtplib.SMTPConnectError

    def login(self, username, password):
        try:
            # self.server.set_debuglevel(1)
            print(username," ",password)
            self.server.login(username, password)
            self.who = username
            self.setHeaders()
            print(username, " login olundu")
        except smtplib.SMTPAuthenticationError as e:
            raise e

    def serverQuit(self):
        self.server.close()
    def setHeaders(self):
        self.headers = [
            ['Precedence', 'bulk'],
            # ['List-Unsubscribe', ''],
            ['List-Unsubscribe', '<mailto:unsubscribe@{}>'.format(self.who.split('@')[-1])],
            ['Content-Location', 'tr-Turkey'],
            ['Content-Language', 'tr-Tr'],
            ['Accept-Language', 'tr-Tr'],
            ['Date', formatdate()],
            ['From', '{} <{}>'.format(self.smtp.split('.')[1].title(),self.who)],
            # ["X-Priority","1 (High)"],
            ['Reply-To', 'Destek<support@{}>'.format(self.who.split('@')[-1])]

        ]
    def send(self, recipent, filename='', subject="", message=""):
        # self.server.set_debuglevel(1)
        outer = MIMEMultipart('alternative')
        # outer['From'] = '<'+self.who+'>'
        outer['To'] = recipent
        outer['Subject'] = subject
        #outer['List-Unsubscribe'] = 'mailto:<unsubscribe@wikybetbonus>'
        print(outer.get('List-Unsubscribe'))
        msgAlternative = MIMEMultipart('alternative')
        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)
        outer.attach(msgAlternative)
        outer.attach(MIMEText(message, 'html'))


        print(self.who," ",recipent)
        for header in self.headers:
            outer.add_header(*header)
        if filename is not '':
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

            self.server.sendmail(self.who, [recipent], composed)
            Logger("Sender:{0} | Recipent:{1}, OK".format(self.who, recipent))

            return True


        except smtplib.SMTPAuthenticationError as hata:
            print("e-posta veya şifrenizi yanlış girdiniz.",
                  "orjinal hata iletisi: ", hata)
            raise smtplib.SMTPAuthenticationError(44, "444")
        except smtplib.SMTPConnectError as e:
            raise e
        except smtplib.SMTPSenderRefused as e:
            raise e
