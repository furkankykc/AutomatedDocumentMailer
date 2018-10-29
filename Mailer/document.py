import smtplib
import pandas
import pandas.errors
import os
from Mailer.myMail import Mail
from tkinter import messagebox
class ismeOzelDavetiye:



    check = []
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self,taslak,liste,username,password,konu,mesaj,dosyaIsmi,smtp,progressbar,interval=-1,startPoint=0,ssl=False):

        self.smtp = smtp
        self.liste = liste
        self.username = username
        self.password = password
        self.interval =interval
        self.ssl =ssl
        try:
           self.serverInit()
        except smtplib.SMTPAuthenticationError as e:
            print(e)
            messagebox.showerror("Hata", "Email veya sifrenizi yanlış girdiniz")
            return
        except smtplib.SMTPConnectError:
            messagebox.showerror("Hata", "Smtp ayarlarını düzgün yaptığınızdan emin olunuz")
        except smtplib.SMTPSenderRefused as e:
            messagebox.showerror("Hata", "Bu mailin email gönderim limiti dolmustur")
            raise smtplib.SMTPSenderRefused
        except smtplib.SMTPServerDisconnected as e:
            print(e)
            messagebox.showerror("Hata", "Email veya sifrenizi yanlış girdiniz")
            return
        except smtplib.SMTPDataError as e:
            messagebox.showerror("Hata", "Bu mailin email gönderim limiti dolmustur")

        try:
            self.refrence = pandas.read_excel(liste,encoding="utf8")
            self.email = self.refrence['EMAİL']
        except FileNotFoundError:
            messagebox.showerror("Hata","Liste Dosyası Bulunamadı")
            raise FileNotFoundError
        except KeyError:
            messagebox.showerror("Hata","EMAİL adlı kolon bulunamadı")
            raise KeyError
        try:
            if startPoint.get()>=0 and startPoint.get()!=None:
                if startPoint.get()>=len(self.email):
                    messagebox.showerror("Hata","Başlangıç değeri epostalardan fazla olamaz")
                    return

        except:
            startPoint.set(0)
            self.email.drop(self.email.index[:startPoint.get()], inplace=True)
        self.email = self.email.tolist()
        # self.email = ['totobet100@outlook.com']
        self.startPoint = startPoint
        self.mailYolla(progressbar,konu=konu,message=mesaj)

    def serverInit(self):
        self.mailci = Mail(self.username[0], self.password,self.username[0], smtp=self.smtp,ssl=self.ssl)

    def mailYolla(self,progressbar,konu="",message=""):
        if progressbar != None:
            progressbar["maximum"] = len(self.email)


        for j in range(len(self.email)):
            emailQueue = int(j / self.interval) % len(self.username)
            try:
                if self.interval !=-1:
                    print("int serl interval : ",(self.interval))
                    if j%int(self.interval)==0:
                        print("interval:{0}/{1}".format(j,self.interval))
                        print("account:{0}".format(self.username[emailQueue]))
                        self.mailci.login(self.username[emailQueue], self.password)

                self.mailci.send(str(self.email[j]), subject=konu, message=message)
                self.startPoint.set(self.startPoint.get()+1)
            except smtplib.SMTPAuthenticationError:
                print(self.password)
                messagebox.showerror("Hata", "Email veya sifrenizi yanlış girdiniz")
                return
            except smtplib.SMTPConnectError:
                messagebox.showerror("Hata","Smtp ayarlarını düzgün yaptığınızdan emin olunuz")
            except smtplib.SMTPSenderRefused as e:
                if self.interval==-1:
                    messagebox.showerror("Hata", "Email gönderim limiti dolmustur")
                    return
                j-=1
                print(e)
                print(self.username.pop(emailQueue)," popped")
                self.serverInit()
                self.mailci.login(self.username[emailQueue], self.password)
                if len(self.username)==0:
                    messagebox.showerror("Hata","Tüm postalarınızın limiti dolmustur")

                continue
            except smtplib.SMTPRecipientsRefused as e:
                print(e)
                #logla burayi
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
                messagebox.showerror("Hata", "Server bu mesaj spam olabileceği için reddetti")
                # self.serverInit()
                print(e)
                return
            print("KALAN : ", j+1,'/',len(self.email))
            if progressbar is not None:

                progressbar.start()
                progressbar["value"] = j
                progressbar.update()
        if progressbar is not None:
            progressbar.stop()
        messagebox.showinfo("Bitti",str(len(self.email))+" tane email başarı ile yollandı.")
