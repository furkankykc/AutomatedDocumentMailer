import urllib.request
import urllib.error

from tkinter import *
from tkinter import messagebox
from Mailer.gui import Gui
from Product.product import Product

listeAdi = ""
taslakAdi = ""
mesaj = ""
selected = ""
data = None


class LoginGui():
    def __init__(self):
        self.root = Tk()
        self.root.title('Automated Mailer System')
        self.prepareLabels()
        self.prepareTextBoxs()
        self.prepareButtons()
        self.root.mainloop()

    def login(self):

        username = self.e1.get()
        password = self.e2.get()
        try:
            p = Product(username)
        except Exception as e:
            print(e)
            messagebox.showerror("Hata", "Kullanıcı adınıza dair bir hesap bulunamadı lütfen abone olunuz.")
            return
        if p.password == password:
            if p.isValid():
                if p.isLimit():
                    self.quit()
                    Gui(username)
                else:
                    messagebox.showinfo("Limit","Aboneliğinize tanımlanmış mail limitiniz dolmuştur.")
            else:
                messagebox.showinfo("Validation","Aboneliğinize tanımlanmış süreniz dolmuştur.")
        else:
            messagebox.showerror("Hata","Sifreniz yanlıştır.")

    def getData(self):
        global data
        try:
            target_url = 'https://raw.githubusercontent.com/furkankykc/EmailAccounts/master/' + self.e1.get()
            data = urllib.request.urlopen(target_url)
            email = data.read().decode("utf8")
            data.close()
            # data = data.split("\n")  # then split it into lines
            return True
        except urllib.error.HTTPError as e:
            print(e.reason)
            messagebox.showerror("Hata", "Kullanıcı adınızı kontrol ediniz")
        except urllib.error.URLError as e:
            print(e.reason)
            messagebox.showerror("Hata", "İnternet Bağlantınızı kontrol ediniz")
        return False
        # data = urllib.request.urlopen(target_url)  # it's a file like object and works just like a file

    def prepareButtons(self):
        # Button(self.root, text='Liste Seç', command=self.browse_list).grid(row=1, column=3, sticky=W, pady=4)
        # Button(self.root, text='Taslak Seç', command=self.browse_list_task).grid(row=5, column=2, sticky=W, pady=4)
        Button(self.root, text='Login', command=self.login).grid(row=3, column=3, sticky=W, pady=4)

    def prepareLabels(self):
        self.userLabel = Label(self.root, text="Username").grid(row=0, sticky=W+E+S+N,padx=4,pady=4)
        self.passLabel = Label(self.root, text="Password").grid(row=1, sticky=W+S+N+E,padx=4,pady=4)


    def prepareTextBoxs(self):
        self.emailText = StringVar()
        self.sifreText = StringVar()
        self.e1 = Entry(self.root, textvariable=self.emailText)
        self.e2 = Entry(self.root, textvariable=self.sifreText)
        self.e2.config(show='*')
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

    def quit(self):
        self.root.destroy()
