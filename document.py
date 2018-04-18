import copy
import docx
import pandas
import myMail
import os
import subprocess

class ismeOzelDavetiye:



    check = []
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self,taslak,liste,username,password,konu,mesaj,dosyaIsmi):
        self.document = docx.Document(taslak)
        self.mailci = myMail.mail(username, password)
        self.refrence = pandas.read_excel(liste)
        self.liste = liste
        self.adi = self.refrence['ADI']
        self.bildiri  =self.refrence['BILDIRI']
        self.email = self.refrence['EMAİL']
        self.dosyaIsmi = dosyaIsmi+'.pdf'
        self.hazirla(konu=konu,message=mesaj)

        self.writeChecks()

    def export_to_pdf(self):
        string ='libreoffice', '--convert-to', 'pdf' ,self.ROOT_DIR+'test.docx '
        #print(string)
        output = subprocess.check_output(['libreoffice --convert-to pdf test.docx'],shell=True)
        subprocess.check_output(['mv test.pdf '+self.dosyaIsmi],shell=True)

        # todo burayı yap
        #print(subprocess.check_output(string,shell=False))
        #print (output)






    # print (adi)
    # print(refrence['ADI'][0])
    def hazirla(self,konu="",message=""):
        for j in range(len(self.adi)):
            print("KALAN : ", len(self.liste) - j,self.adi[j])
            bul = "{isim}"
            bul2 = "{bildiri}"
            tempDoc = copy.deepcopy(self.document)
            for i in  tempDoc.paragraphs:
                if bul in i.text:
                    temp = i.text
                    i.text= temp.replace(bul,str(self.adi[j]))
                if bul2 in i.text:
                    temp2 = i.text
                    i.text= temp2.replace(bul2,str(self.bildiri[j]))
            print('Dosya Kaydedildi.')
            tempDoc.save('test.docx')
            self.export_to_pdf()
            print('E-mail yollanıyor.')
            self.check.append(self.mailci.yolla(str(self.email[j]),filename=self.dosyaIsmi,konu=konu,message=message))


    def writeChecks(self):
        writer = pandas.ExcelWriter(self.liste)

        # Convert the dataframe to an XlsxWriter Excel object.
        if len(self.check) == len(self.refrence):
            self.refrence['check'] = self.check
            self.refrence.to_excel(writer, sheet_name='check')
            writer.save()

