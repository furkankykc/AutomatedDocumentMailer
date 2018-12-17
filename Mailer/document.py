import smtplib
import pandas
import pandas.errors
import os
from Mailer.myMail import Mail
#from tkinter import messagebox
from Utils.strings import *
from Utils.Logger import Logger
from Utils.reading import seperatedListSummoner
from Utils.errors import *
language = 'en'


class ismeOzelDavetiye():
    globals()

    check = []
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, taslak, liste, username, password, konu, mesaj, dosyaIsmi, smtp, progressbar, interval=-1,
                 startPoint=0, ssl=False):
        self.smtp = smtp
        self.liste = liste
        self.username = username
        self.password = password
        self.interval = interval
        self.ssl = ssl
        try:
            self.serverInit()
        except Exception as e:
            raise e
        try:
            self.refrence = pandas.read_excel(liste, encoding="utf8")
            self.email = self.refrence['EMAİL']
            # self.ad = self.refrence['AD']
            print(self.email)
        except Exception:
            raise Exception
        start =0
        try:
            if startPoint.get() >= 0 and startPoint.get() != None:
                start = startPoint.get()
                if startPoint.get() >= len(self.email):
                    print(len(self.email))
                    raise StartError

        except:
            start = startPoint
        self.email.drop(self.email.index[:start], inplace=True)
        self.email = self.email.tolist()
        # self.ad = self.ad.tolist()
        # self.email = ['totobet100@houtlook.com','hasan_bayraktar@hotmail.com']
        # self.email = ['furkanfbr@gmail.com']*100

        # self.email = ['test-2wq0k@mail-tester.com','furkanfbr@gmail.com']
        self.startPoint = startPoint
        self.sendSeperatedMails(progressbar,konu,mesaj)
        # self.mailYolla(progressbar, konu=konu, message=mesaj)

    def serverInit(self):
        self.mailci = Mail(self.username[0], self.password, self.username[0], smtp=self.smtp, ssl=self.ssl)

    def mailYolla(self, progressbar, konu="", message=""):
        self.mailci.login(self.username[0], self.password)
        sentMails = 0
        if progressbar != None:
            progressbar["maximum"] = len(self.email)

        for j in range(len(self.email)):
            emailQueue = int(j / self.interval) % len(self.username)
            try:
                if self.interval != -1:
                    print("int serl interval : ", (self.interval))
                    if j % int(self.interval) == 0:
                        print("interval:{0}/{1}".format(j, self.interval))
                        print("account:{0}".format(self.username[emailQueue]))
                        self.mailci.serverQuit()
                        self.serverInit()
                        self.mailci.login(self.username[emailQueue], self.password)
                try:
                    ad=str(self.ad[j])
                except:
                    ad =""

                self.mailci.send(str(self.email[j]), subject=konu, message=message)
                # self.mailci.send(str(self.email[j]), subject="Merhaba"+ad+" "+konu, message=message)
                try:
                    self.startPoint.set(self.startPoint.get() + 1)
                except:
                    continue
            except smtplib.SMTPAuthenticationError as e:
                if self.interval == -1:
                    print(self.password)
                    #messagebox.showerror(errors[language]['error'], errors[language]['authError'])
                    self.mailci.serverQuit()
                    raise e

                print(e)
                print(self.username.pop(emailQueue), " popped")
                self.serverInit()
                self.mailci.login(self.username[emailQueue], self.password)
                j -= 1
                if len(self.username) == 0:
                    # messagebox.showerror(errors[language]['error'], errors[language]['limitError'])
                    raise LimitError
            except smtplib.SMTPConnectError as e:
                # messagebox.showerror(errors[language]['error'], errors[language]['smtpError'])
                raise e
            except smtplib.SMTPSenderRefused as e:
                if self.interval == -1:
                    # messagebox.showerror(errors[language]['error'], errors[language]['senderRefused'])
                    raise e

                print(e)
                print(self.username.pop(emailQueue), " popped")
                self.serverInit()
                self.mailci.login(self.username[emailQueue], self.password)
                j -= 1
                if len(self.username) == 0:
                    # messagebox.showerror(errors[language]['error'], errors[language]['limitError'])
                    raise LimitError
                continue
            except smtplib.SMTPRecipientsRefused as e:
                # for key in e.args[0]:
                #     print(key,e.args[0][key])
                errorDict = e.args[0]
                keylist = []
                keylist.extend(iter(errorDict.keys()))
                error_code = errorDict[keylist[0]][1]
                print(error_code)
                Logger("Sender:{0} | Recipent:{1}, DENY :{2}".format(self.username[emailQueue], self.email[j], e))
                # if error_code == 550:
                #     continue
                if self.interval == -1:
                    # messagebox.showerror(errors[language]['error'], errors[language]['limitError'])
                    raise LimitError
                continue
            except smtplib.SMTPDataError as e:
                # if self.interval!=-1:
                #     self.mailci.serverInit()
                #     j -= 1
                #     print(self.username.pop(emailQueue), " popped")
                #     print(e)
                #
                #     continue
                # else:
                # messagebox.showerror(errors[language]['error'], errors[language]['spamError'])

                # self.serverInit()
                print(e)
                raise e
            sentMails = j + 1
            print("Yolanan : ", str(sentMails), '/', len(self.email))
            if progressbar is not None:
                progressbar.start()
                progressbar["value"] = j
                progressbar.update()

        if progressbar is not None:
            progressbar.stop()
        # messagebox.showinfo("Bitti", str(sentMails) + " tane email başarı ile yollandı.")



    def sendSeperatedMails(self,progressbar,konu,mesaj):
        refrence = pandas.read_excel(self.liste, encoding="utf8")
        try:
            email = refrence['EMAİL']
        except KeyError:
        # messagebox.showerror(errors[language]['error'], errors[language]['keyError'])
            raise KeyError
        self.email  = email.tolist()
        self.mailYolla(progressbar, konu=konu, message=mesaj)
        self.liste = seperatedListSummoner(self.liste)
        if(self.liste is not None):
            self.sendSeperatedMails(progressbar,konu,mesaj)