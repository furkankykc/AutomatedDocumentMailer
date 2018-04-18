from tkinter.filedialog import askopenfile
from document import ismeOzelDavetiye
from tkinter import *
listeAdi = ""
taslakAdi = ""


class Gui():
    #root = Tk()
    #root.title = 'Automated Mailer System'
    def __init__(self):
        self.root = Tk()
        self.prepareLabels()
        self.prepareTextBoxs()
        self.prepareButtons()
        self.root.mainloop()

    def browse_list(self):
        file = askopenfile(filetypes=(("Exel files", "*.xls")
                       , ("Exel files", "*.xlsx")),
                                   parent=self.root,mode='rb',title='Choose a file')
        if file != None:
            data = file.read()
            file.close()
            listeAdi= ((file).name)
            self.listText.set((file).name.split('/')[-1])


    def browse_list_task(self):
        file = askopenfile(
            filetypes=(("Odx files", "*.odx")
                       , ("Docx files", "*.docx")),
                         parent=self.root,mode='rb',title='Choose sa file')
        if file != None:
            data = file.read()
            file.close()
            taslakAdi= ((file).name)
            self.taskText.set((file).name.split('/')[-1])
            print(taslakAdi)
    def yolla(self):
        global taslakAdi,listeAdi
        email = self.e1.get()
        password = self.e2.get()
        konu = self.e3.get()
        mesaj = self.e4.get()
        print(taslakAdi)
        ismeOzelDavetiye(taslakAdi,str('örnek.xls'),str(email),str(password),str(konu),str(mesaj))

    def prepareLabels(self):
        self.emailLabel = Label(self.root, text="E-mail").grid(row=0)
        self.passLabel = Label(self.root, text="Şifre").grid(row=1)
        self.subLabel = Label(self.root, text="Konu").grid(row=2)
        self.msgLabel = Label(self.root, text="Mesaj").grid(row=3)
        self.listLabel = Label(self.root, text="Liste").grid(row=4)
        self.taskLabel = Label(self.root, text="Taslak").grid(row=5)

    def prepareTextBoxs(self):
        self.listText = StringVar()
        self.taskText = StringVar()
        self.e1 = Entry(self.root)
        self.e2 = Entry(self.root)
        self.e3 = Entry(self.root)
        self.e4 = Entry(self.root)
        self.e5 = Entry(self.root, textvariable=self.listText)
        self.e6 = Entry(self.root, textvariable=self.taskText)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)

    def prepareButtons(self):
        self.e5.bind("<Double-1>", self.OnDoubleClick)
        self.e6.bind("<Double-1>", self.OnDoubleClickTask)
        #Button(self.root, text='Liste Seç', command=self.browse_list).grid(row=1, column=3, sticky=W, pady=4)
        #Button(self.root, text='Taslak Seç', command=self.browse_list_task).grid(row=5, column=2, sticky=W, pady=4)
        Button(self.root, text='Gönder', command=self.yolla).grid(row=5, column=3, sticky=W, pady=4)
    def OnDoubleClick(self, event):
        self.browse_list()
    def OnDoubleClickTask(self, event):
        self.browse_list_task()
    #root.title = 'Automated Mailer System'
    #
    # root.mainloop()
    #
    
