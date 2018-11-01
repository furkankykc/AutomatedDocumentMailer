import smtplib
import pandas
import pandas.errors
import os
from Mailer.myMail import Mail
from tkinter import messagebox
from Utils.strings import *
from Utils.Logger import Logger
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
        except smtplib.SMTPAuthenticationError as e:
            print(e)
            messagebox.showerror(errors[language]['error'], errors[language]['authError'])
            return
        except smtplib.SMTPConnectError:
            messagebox.showerror(errors[language]['error'], errors[language]['smtpError'])
        except smtplib.SMTPSenderRefused as e:
            messagebox.showerror(errors[language]['error'], errors[language]['senderRefused'])
            raise smtplib.SMTPSenderRefused
        except smtplib.SMTPServerDisconnected as e:
            print(e)
            messagebox.showerror(errors[language]['error'], errors[language]['serverDisconnect'])
            return
        except smtplib.SMTPDataError as e:
            messagebox.showerror(errors[language]['error'], errors[language]['senderRefused'])

        try:
            self.refrence = pandas.read_excel(liste, encoding="utf8")
            self.email = self.refrence['EMAİL']
        except FileNotFoundError:
            messagebox.showerror(errors[language]['error'], errors[language]['listError'])
            raise FileNotFoundError
        except KeyError:
            messagebox.showerror(errors[language]['error'], errors[language]['keyError'])
            raise KeyError
        try:
            if startPoint.get() >= 0 and startPoint.get() != None:
                if startPoint.get() >= len(self.email):
                    messagebox.showerror(errors[language]['error'], errors[language]['startError'])
                    return

        except:
            startPoint.set(0)
            self.email.drop(self.email.index[:startPoint.get()], inplace=True)
        self.email = self.email.tolist()
        # self.email = ['totobet100@houtlook.com','hasan_bayraktar@hotmail.com']
        self.email = ['st-3-afyagk5c1@glockapps.com']
        self.startPoint = startPoint
        self.mailYolla(progressbar, konu=konu, message=mesaj)


    def serverInit(self):
        self.mailci = Mail(self.username[0], self.password, self.username[0], smtp=self.smtp, ssl=self.ssl)


    def mailYolla(self, progressbar, konu="", message=""):
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

                self.mailci.send(str(self.email[j]), subject=konu, message=message)
                self.startPoint.set(self.startPoint.get() + 1)
            except smtplib.SMTPAuthenticationError:
                print(self.password)
                messagebox.showerror(errors[language]['error'], errors[language]['authError'])
                return
            except smtplib.SMTPConnectError:
                messagebox.showerror(errors[language]['error'], errors[language]['smtpError'])
            except smtplib.SMTPSenderRefused as e:
                if self.interval == -1:
                    messagebox.showerror(errors[language]['error'], errors[language]['senderRefused'])
                    return

                print(e)
                print(self.username.pop(emailQueue), " popped")
                self.serverInit()
                self.mailci.login(self.username[emailQueue], self.password)
                j -= 1
                if len(self.username) == 0:
                    messagebox.showerror(errors[language]['error'], errors[language]['limitError'])

                continue
            except smtplib.SMTPRecipientsRefused as e:
                print(e)
                Logger("Sender:{0} | Recipent:{1}, DENY :{2}".format(self.username[emailQueue],self.email[j],e))
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
                messagebox.showerror(errors[language]['error'], errors[language]['spamError'])

                # self.serverInit()
                print(e)
                return
            sentMails =  j + 1
            print("Yolanan : ",str(sentMails), '/', len(self.email))
            if progressbar is not None:
                progressbar.start()
                progressbar["value"] = j
                progressbar.update()
        if progressbar is not None:
            progressbar.stop()
        messagebox.showinfo("Bitti", str(sentMails) + " tane email başarı ile yollandı.")
