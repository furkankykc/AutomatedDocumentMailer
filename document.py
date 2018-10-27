import copy
import smtplib
import pandas
import xmltodict
import os
from myMail import Mail
import numpy
from tkinter import messagebox
class ismeOzelDavetiye:



    check = []
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self,taslak,liste,username,password,konu,mesaj,dosyaIsmi,smtp,progressbar,interval=-1,startPoint=0):
        # if taslak!='':
        #     self.document = docx.Document(taslak)
        try:
            self.mailci = Mail(username[0], password,who=username[0],smtp=smtp)
        except smtplib.SMTPAuthenticationError:
            messagebox.showerror("Hata", "Email veya sifrenizi yanlış girdiniz")
            raise smtplib.SMTPAuthenticationError
        except smtplib.SMTPConnectError:
            messagebox.showerror("Hata", "Smtp ayarlarını düzgün yaptığınızdan emin olunuz")
        except smtplib.SMTPSenderRefused as e:
            messagebox.showerror("Hata", "Email gönderim limiti dolmustur")
            raise smtplib.SMTPSenderRefused
        except smtplib.SMTPServerDisconnected:
            messagebox.showerror("Hata", "Email veya sifrenizi yanlış girdiniz")
            raise smtplib.SMTPServerDisconnected
        self.interval =interval
        self.password=password
        self.smtp=smtp

        try:
            self.refrence = pandas.read_excel(liste,encoding="utf8")
        except FileNotFoundError:
            messagebox.showerror("Hata","Liste Dosyası Bulunamadı")
            raise FileNotFoundError

        self.liste = liste
        self.username = username
        self.dic = xmltodict.parse("""<?xml version="1.0" ?>
        <properties>
          <var>yeni</var>
          <var>test</var>
        </properties>""")
        #self.adi = self.refrence['ADI']
        #self.bildiri  =self.refrence['BILDIRI']
        # self.smtp = smtp
        self.email = self.refrence['EMAİL']
        if startPoint.get()!=0 and startPoint.get()!=None:
            self.email.drop(self.email.index[:startPoint.get()], inplace=True)
        self.email = self.email.tolist()
        self.startPoint = startPoint

        print(len(self.email)," len self email")
        # self.email = ['cagataykuzgunlu@hotmail.com']
        if dosyaIsmi!='':
            self.dosyaIsmi = dosyaIsmi+'.pdf'
        #self.hazirla(progressbar,konu=konu,message=mesaj)
        self.mailYolla(progressbar,konu=konu,message=mesaj)
        # self.writeChecks()
    # 152+204
    # def export_to_pdf(self):
    #     string ='libreoffice', '--convert-to', 'pdf' ,self.ROOT_DIR+'test.docx '
    #     #print(string)
    #     output = subprocess.check_output(['libreoffice --convert-to pdf test.docx'],shell=True)
    #     subprocess.check_output(['mv test.pdf '+self.dosyaIsmi],shell=True)
    #
    #     # todo burayı yap
    #     #print(subprocess.check_output(string,shell=False))
    #     #print (output)




    def mailYolla(self,progressbar,konu="",message=""):
        if progressbar != None:
            progressbar["maximum"] = len(self.email)
        for j in range(len(self.email)):
            emailQueue = int(j / self.interval) % len(self.username)
            try:
                if self.interval !=-1:
                    print("int serl interval : ",(self.interval))
                    if j%int(self.interval)==0:

                        self.mailci.login(self.username[emailQueue],self.password)
                        print("interval:{0}/{1}".format(j,self.interval))
                        print("account:{0}".format(self.username[emailQueue]))
                self.mailci.send(str(self.email[j]), subject=konu, message=message)
                self.startPoint.set(self.startPoint.get()+1)
            except smtplib.SMTPAuthenticationError:
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
                self.mailci.serverInit(self.smtp)
                self.mailci.login(self.username[emailQueue], self.password)
                if len(self.username)==0:
                    messagebox.showerror("Hata","Tüm postalarınızın limiti dolmustur")

                continue
            except smtplib.SMTPRecipientsRefused as e:
                print(e)
                continue
            except smtplib.SMTPServerDisconnected as e:
                messagebox.showerror("Hata","Bu IP den 24 saatlik gönderim hakkınız dolmuştur")

            print("KALAN : ", j,'/',len(self.email))
            # if(j%self.interval):
            #     messagebox.showinfo("Gönderim Bildirimi","{0} tane mesaj yollandı.\n İşleminiz devam ediyor.\n Kalan : {1}".format(j,len(self.email)-j))
            if progressbar is not None:

                progressbar.start()
                progressbar["value"] = j
                progressbar.update()
        if progressbar is not None:
            progressbar.stop()
        messagebox.showinfo("Bitti",str(len(self.email))+" tane email başarı ile yollandı.")


    def hazirla(self,progressbar,konu="",message=""):
        for j in range(len(self.refrence[self.dic['properties']['var'][0]])):
            print("KALAN : ", len(self.liste) - j,self.refrence[self.dic['properties']['var'][0]][j])
            tempDoc = copy.deepcopy(self.document)
            for i in  tempDoc.paragraphs:
                for d in self.dic['properties']['var']:
                    if d in i.text:
                        temp = i.text
                        i.text= temp.replace(str("{"+d+"}"),str(self.refrence[d][j]))

            print('Dosya Kaydedildi.')
            tempDoc.save('test.docx')
            self.export_to_pdf()
            print('E-mail yollanıyor.')
            self.check.append(self.mailci.send(str(self.email[j]), filename=self.dosyaIsmi, subject=konu, message=message))


    def writeChecks(self):
        writer = pandas.ExcelWriter(self.liste)

        # Convert the dataframe to an XlsxWriter Excel object.
        if len(self.check) == len(self.refrence):
            self.refrence['check'] = self.check
            self.refrence.to_excel(writer, sheet_name='check')
            writer.save()

