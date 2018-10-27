import urllib.request
from tkinter.filedialog import askopenfile
from xml.etree import ElementTree
from xml.dom import minidom
import xmltodict

from document import ismeOzelDavetiye
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

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
startPoint= 'start'
defaultEmail = "example@mail.com"
defaulPassword = ''
defaultList = ''
defaultSubject = "Örnek Konu"
defaultSmtp = ["smtpout.europe.secureserver.net:465", "smtp.gmail.com:587", "smtp-mail.outlook.com:587","smtp.x-news.online:587"]
defaultTask = ''
defaultMessage = ''
defaultStartPoint = 0
encoding = ['utf-8','iso-8859-9']

class Gui():
    globals()

    def __init__(self, username):
        self.root = Tk()
        self.root.title('Automated Mailer System')
        self.getEmail(username)
        self.prepareTextBoxs()
        self.getXmlDataSource()
        self.prepareLabels()
        self.prepareButtons()
        self.prepareProgressBar()
        self.prepareMenu()
        self.updateMailInterval()
        self.root.mainloop()
        self.saveXmlDataSource()

    def getEmail(self, username):
        target_url = 'https://raw.githubusercontent.com/furkankykc/EmailAccounts/master/' + username
        data = urllib.request.urlopen(target_url)
        self.email = data.read().decode("utf8")[:-1].split("\n")
        print(self.email)
        data.close()

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
                progress = ismeOzelDavetiye(taslakAdi, str(list), (email), str(password), str(subject), messageData, "",
                                 self.smtpValue.get(),
                                 progressbar=self.progressBar,
                                 interval=interval,
                                 startPoint=self.startPoint
                                 )
                self.sendButton.configure(state='normal')

            except Exception as e:
                print(e)

                messagebox.showerror("Hata","Bilinmeyen bir hata yüzünden program duraklatıldı lütfen tekrar başlatınız\n{0}".format(e))
                self.sendButton.configure(state='normal')
        except FileNotFoundError as e:
            print(e)
            messagebox.showerror("Hata", "Mesaj Dosyası Bulunamadı")
            self.sendButton.configure(state='normal')

    def prepareLabels(self):
        self.emailLabel = Label(self.root, text="E-mail").grid(row=0)
        self.passLabel = Label(self.root, text="Şifre").grid(row=1)
        self.subLabel = Label(self.root, text="Konu").grid(row=2)
        self.messageLabel = Label(self.root, text="Mesaj").grid(row=3)
        self.listLabel = Label(self.root, text="Liste").grid(row=4)
        self.startLabel = Label(self.root, text="Liste Başlangıcı").grid(row=8)
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
        self.mailVar = IntVar()
        self.startPoint = IntVar()

        self.checkBox = Checkbutton(self.root, text="Enable Queue", variable=self.checkVar,
                                    command=self.updateMailInterval)
        self.mailInterval = Entry(self.root, textvariable=self.mailVar)
        self.startText = Entry(self.root, textvariable=self.startPoint)
        # self.taskTextBox = Entry(self.root, textvariable=self.taskText)
        self.mailVar.set(100)
        self.passwordTextBox.configure(show='*')
        self.passwordTextBox.grid(row=1, column=1)
        self.subjectTextBox.grid(row=2, column=1)
        self.messageSelect.grid(row=3, column=1)
        self.listSelect.grid(row=4, column=1)
        self.checkBox.grid(row=7, column=0)
        self.mailInterval.grid(row=7, column=1)
        self.startText.grid(row=8, column=1)
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
        self.smtpMenu.grid(row=5, column=1)

    def prepareButtons(self):
        self.listSelect.bind("<Double-1>", self.OnDoubleClick)
        # self.taskTextBox.bind("<Double-1>", self.OnDoubleClickTask)
        self.messageSelect.bind("<Double-1>", self.OnDoubleClickMessage)
        # Button(self.root, text='Liste Seç', command=self.browse_list).grid(row=1, column=3, sticky=W, pady=4)
        # Button(self.root, text='Taslak Seç', command=self.browse_list_task).grid(row=5, column=2, sticky=W, pady=4)
        self.sendButton = Button(self.root, text='Gönder', command=self.send)
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
                self.prettify(
                    self.xmlConverter(properties,
                                      self.xmlConverter(email, self.emailText.get()),
                                      self.xmlConverter(password, self.passwordText.get()),
                                      self.xmlConverter(message, self.messageFileLocation),
                                      self.xmlConverter(subject, self.subjectText.get()),
                                      self.xmlConverter(list, self.listFileLocation),
                                      self.xmlConverter(startPoint, self.startPoint.get()),
                                      self.xmlConverter(task, self.taskText.get()),
                                      *[self.xmlConverter(smtp, itrSmtp) for itrSmtp in self.smtp]
                                      )
                )

            )

    def xmlConverter(self, xmlColon, *variable):
        return ("<{0}>" + (('%s' * len(variable)).lstrip() % variable) + "</{0}>").format(xmlColon)

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        reparsed = minidom.parseString(elem)
        var = reparsed.toprettyxml(indent="\t")
        print(var)
        return var

    def createDefaultXml(self):
        with open(xmlFile, "w+") as fd:
            fd.write(
                self.prettify(
                    self.xmlConverter(properties,
                                      self.xmlConverter(email, defaultEmail),
                                      self.xmlConverter(password, defaulPassword),
                                      self.xmlConverter(message, defaultMessage),
                                      self.xmlConverter(subject, defaultSubject),
                                      self.xmlConverter(list, defaultList),
                                      self.xmlConverter(task, defaultTask),
                                      self.xmlConverter(startPoint, defaultStartPoint),
                                      *[self.xmlConverter(smtp, itrSmtp) for itrSmtp in defaultSmtp]
                                      )
                )
            )
