import mimetypes
import smtplib  # smtplib modulunu projemize ekledik
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
from smtpd import COMMASPACE



class mail:

    def __init__(self,username,password):
        self.kullanıcı = username
        self.kullanıcı_sifresi = password


    def yolla(self,alici,filename = 'Kabul Mektubu.pdf',konu="",message=""):
        outer = MIMEMultipart()
        outer['From'] = "adassad"
        outer['To'] = alici
        outer['Subject'] =konu
        outer.attach(MIMEText(message, 'plain'))
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
            encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        outer.attach(msg)

        # oluşturduğumuz text, html ve file datasını string olarak alıyoruz

        composed = outer.as_string()
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.kullanıcı, self.kullanıcı_sifresi)
            server.sendmail(self.kullanıcı,alici, composed)
            return ("E-mail başarıyla gönderildi")


        except smtplib.SMTPAuthenticationError as hata:
            print("e-posta veya şifrenizi yanlış girdiniz.",
                  "orjinal hata iletisi: ", hata)
            return ("Bir hata oluştu. E-mail gönderilemedi.")
        except:
            return ("Bir hata oluştu. E-mail gönderilemedi.")
        finally:
            server.quit()