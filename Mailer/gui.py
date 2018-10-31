import urllib.request
from tkinter.filedialog import askopenfile
import xmltodict

from Mailer.document import ismeOzelDavetiye
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Product.product import Product
from Utils.xmlOperations import *

listeAdi = ""
taslakAdi = ""
# hilbet encoding='iso-8859-9'
email = "email"
password = "password"
subject = "subject"
list = "list"
message = "message"
task = "task"
smtp = "smtp"
properties = "properties"
xmlFile = 'properties.xml'
startPoint = 'start'
defaultEmail = "example@mail.com"
defaulPassword = ''
defaultList = ''
defaultSubject = "Örnek Konu"
defaultSmtp = ["smtpout.europe.secureserver.net:465", "smtp.gmail.com:587", "smtp-mail.outlook.com:587",
               "mail.x-news.site:465"]
defaultTask = ''
defaultMessage = ''
defaultStartPoint = 0
encoding = ['utf-8', 'iso-8859-9']
SSL = 'ssl'
defaultSSL = False


# url = 'https://raw.githubusercontent.com/furkankykc/EmailAccounts/master/xbet'

# def getCompanyDataFromUrl(name,dir=''):
#     baseUrl = url
#     print(baseUrl)
#     with urllib.request.urlopen(baseUrl) as data:
#         return (data.read().decode("utf8")[:-1].split("\n"))

class Gui():
    globals()

    def __init__(self, username):
        self.root = Tk()
        self.root.title('Automated Mailer System')
        try:
            self.product = Product(username)
            self.email = (self.product.getEmail())
            print(self.email)
            # self.email = getCompanyDataFromUrl(username)
            # print(self.email)
        except Exception as e:
            messagebox.showerror("Hata", "Hesabınızla ilişkili mail adresi bulunamadı")
            print(e)
            self.root.quit()
            return
        self.prepareTextBoxs()
        self.getXmlDataSource()
        self.prepareLabels()
        self.prepareButtons()
        self.prepareProgressBar()
        self.prepareMenu()
        self.updateMailInterval()
        self.root.mainloop()
        self.saveXmlDataSource()

    def browse_list(self):
        file = askopenfile(filetypes=(("Exel files", "*.xls")
                                      , ("Exel files", "*.xlsx")),
                           parent=self.root, mode='rb', title='Choose a file')
        if file != None:
            data = file.read()
            file.close()
            self.listFileLocation = file.name
            self.listText.set((file).name.split('/')[-1])

    def browse_message(self):
        file = askopenfile(filetypes=(("Html Files", "*.html"),
                                      ("Text Files", "*.txt")
                                      ),
                           parent=self.root, mode='rb', title='Choose a file')
        if file is not None:
            # data = file.read()
            self.messageFileLocation = file.name
            self.messageText.set((file).name.split('/')[-1])
            file.close()

    def browse_list_task(self):
        file = askopenfile(
            filetypes=(("Odx files", "*.odx")
                       , ("Docx files", "*.docx")),
            parent=self.root, mode='rb', title='Choose sa file')
        if file is not None:
            self.taskFileLocation = file.name
            self.taskText.set((file).name.split('/')[-1])
            print(taslakAdi)
            file.close()

    def send(self):
        self.sendButton.configure(state='disabled')
        email = [self.emailText.get()]
        password = self.passwordTextBox.get()
        print("password:", password)
        subject = self.subjectTextBox.get()
        list = self.listFileLocation
        print(taslakAdi)
        try:
            with open(self.messageFileLocation, 'r', encoding=encoding[0]) as fd:
                messageData = fd.read()
                # print(messageData)
                if self.checkVar.get() == 1:
                    interval = int(self.mailInterval.get())
                    email = self.email

                else:
                    interval = -1
            try:

                self.startText.configure(state='disabled')
                subLimit = self.startPoint.get()
                if int(self.startPoint.get()) < 0:
                    self.startPoint.set(0)
                ismeOzelDavetiye(taslakAdi, str(list), (email), str(password), str(subject), messageData, "",
                                 self.smtpValue.get(),
                                 progressbar=self.progressBar,
                                 interval=interval,
                                 startPoint=self.startPoint,
                                 ssl=self.ssl.get()
                                 )
                self.product.updateLimit(int(self.startPoint.get()) - int(subLimit))
                self.startText.configure(state='normal')
                self.sendButton.configure(state='normal')

            except Exception as e:
                print(e)

                messagebox.showerror("Hata",
                                     "Bilinmeyen bir hata yüzünden program duraklatıldı lütfen tekrar başlatınız\n{0}".format(
                                         e))
                self.sendButton.configure(state='normal')
                self.startText.configure(state='normal')
        except FileNotFoundError as e:
            print(e)
            messagebox.showerror("Hata", "Mesaj Dosyası Bulunamadı")
            self.startText.configure(state='normal')
            self.sendButton.configure(state='normal')

    def prepareLabels(self):
        self.emailLabel = Label(self.root, text="E-mail").grid(row=0)
        self.passLabel = Label(self.root, text="Password").grid(row=1)
        self.subLabel = Label(self.root, text="Subject").grid(row=2)
        self.messageLabel = Label(self.root, text="Message").grid(row=3)
        self.listLabel = Label(self.root, text="List").grid(row=4)
        self.startLabel = Label(self.root, text="Start of List").grid(row=5)
        # self.taskLabel = Label(self.root, text="Taslak").grid(row=5)

    def prepareTextBoxs(self):
        self.sendMessage = ""
        # local variable definations
        self.listText = StringVar()
        self.taskText = StringVar()
        self.emailText = StringVar()
        self.passwordText = StringVar()
        self.subjectText = StringVar()
        self.messageText = StringVar()
        self.taskText = StringVar()
        self.smtpValue = StringVar()

        # self.e1.configure(state='disabled')
        self.passwordTextBox = Entry(self.root, textvariable=self.passwordText)
        self.subjectTextBox = Entry(self.root, textvariable=self.subjectText)
        self.messageSelect = Entry(self.root, textvariable=self.messageText)
        self.listSelect = Entry(self.root, textvariable=self.listText)
        self.checkVar = IntVar()
        self.ssl = BooleanVar()
        self.mailVar = IntVar()
        self.startPoint = IntVar()

        self.checkBox = Checkbutton(self.root, text="Enable Queue", variable=self.checkVar,
                                    command=self.updateMailInterval)

        self.sslButton = Checkbutton(self.root, text="Enable SSL", variable=self.ssl)
        # self.sslButton.select()
        self.mailInterval = Entry(self.root, textvariable=self.mailVar)
        self.startText = Entry(self.root, textvariable=self.startPoint)
        # self.taskTextBox = Entry(self.root, textvariable=self.taskText)
        self.mailVar.set(100)
        self.passwordTextBox.configure(show='*')
        self.passwordTextBox.grid(row=1, column=1)
        self.subjectTextBox.grid(row=2, column=1)
        self.messageSelect.grid(row=3, column=1)
        self.listSelect.grid(row=4, column=1)
        self.checkBox.grid(row=8, column=0)
        self.mailInterval.grid(row=8, column=1)
        self.startText.grid(row=5, column=1)
        self.sslButton.grid(row=9, column=0)
        # self.taskTextBox.grid(row=5, column=1)

    def prepareProgressBar(self):
        self.progressBar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="determinate")
        self.progressBar.grid(row=9, column=1)
        self.progressBar["maximum"] = 100
        self.progressBar["value"] = 0

    def prepareMenu(self):
        self.emailMenu = OptionMenu(self.root, self.emailText, *self.email)
        self.smtpMenu = OptionMenu(self.root, self.smtpValue, *self.smtp)
        self.emailMenu.grid(row=0, column=1)
        self.smtpMenu.grid(row=6, column=1)

    def prepareButtons(self):
        self.listSelect.bind("<Double-1>", self.OnDoubleClick)
        # self.taskTextBox.bind("<Double-1>", self.OnDoubleClickTask)
        self.messageSelect.bind("<Double-1>", self.OnDoubleClickMessage)
        # Button(self.root, text='Liste Seç', command=self.browse_list).grid(row=1, column=3, sticky=W, pady=4)
        # Button(self.root, text='Taslak Seç', command=self.browse_list_task).grid(row=5, column=2, sticky=W, pady=4)
        self.sendButton = Button(self.root, text='Send', command=self.send)
        self.sendButton.grid(row=9, column=3, sticky=W, pady=4)

    def updateMailInterval(self):
        if self.checkVar.get():
            self.mailInterval.configure(state='normal')
            self.emailMenu.configure(state='disabled')
        else:
            self.mailInterval.configure(state='disabled')
            self.emailMenu.configure(state='normal')

    def OnDoubleClick(self, event):
        self.browse_list()

    def OnDoubleClickMessage(self, event):
        self.browse_message()

    def OnDoubleClickTask(self, event):
        self.browse_list_task()

    def getXmlDataSource(self):
        # self.emailText.set(self.email)
        try:
            with open(xmlFile, "r") as fd:
                fd = xmltodict.parse(fd.read())[properties]
            # self.emailText.set(doc[email])
            self.passwordText.set(fd[password])
            self.subjectText.set(fd[subject])
            self.messageFileLocation = fd[message]
            self.ssl.set(fd[SSL])
            self.startPoint.set(fd[startPoint])
            if self.messageFileLocation is not None:
                self.messageText.set(self.messageFileLocation.split('/')[-1])
            self.listFileLocation = fd[list]
            if self.listFileLocation is not None:
                self.listText.set(self.listFileLocation.split('/')[-1])
            self.smtp = fd[smtp]
            self.emailText.set(self.email[0])
            self.smtpValue.set(self.smtp[1])

        except:
            self.createDefaultXml()
            self.getXmlDataSource()

    def saveXmlDataSource(self):
        with open("properties.xml", "w") as fd:
            fd.write(
                prettify(
                    xmlConverter(properties,
                                 xmlConverter(email, self.emailText.get()),
                                 xmlConverter(password, self.passwordText.get()),
                                 xmlConverter(message, self.messageFileLocation),
                                 xmlConverter(subject, self.subjectText.get()),
                                 xmlConverter(list, self.listFileLocation),
                                 xmlConverter(startPoint, self.startPoint.get()),
                                 xmlConverter(task, self.taskText.get()),
                                 xmlConverter(SSL, self.ssl.get()),
                                 *[xmlConverter(smtp, itrSmtp) for itrSmtp in self.smtp]
                                 )
                )

            )

    def createDefaultXml(self):
        with open(xmlFile, "w+") as fd:
            fd.write(
                prettify(
                    xmlConverter(properties,
                                 xmlConverter(email, defaultEmail),
                                 xmlConverter(password, defaulPassword),
                                 xmlConverter(message, defaultMessage),
                                 xmlConverter(subject, defaultSubject),
                                 xmlConverter(list, defaultList),
                                 xmlConverter(task, defaultTask),
                                 xmlConverter(startPoint, defaultStartPoint),
                                 xmlConverter(SSL, defaultSSL),
                                 *[xmlConverter(smtp, itrSmtp) for itrSmtp in defaultSmtp]
                                 )
                )
            )
