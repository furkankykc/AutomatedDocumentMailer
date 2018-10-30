import datetime
import time
import urllib.request
import xmltodict
import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as rsaCry
import base64
from Product.createsubscribtion import updateFile,saveXmlDataSource
url = 'https://raw.githubusercontent.com/furkankykc/EmailAccounts/master/Product/'
email = 'email'
password = 'password'
validationDate = 'validationDate'
limit = 'limit'


class Product():
    globals()

    def __init__(self, compName):
        self.name = compName
        self.password = None
        self.validationDate = None
        self.mailLimitationValue = None
        try:
            self.getInformation()
        except Exception as e:
            raise e
    def getInformation(self):
        data = xmltodict.parse(self.getCompanyDataFromUrl('details'))[self.name]
        self.password= data[password]
        self.validationDate = data[validationDate]
        print("valid =",self.validationDate)
        self.mailLimitationValue = data[limit]
        print(self.mailLimitationValue)


    def getCompanyDataFromUrl(self,dir,secure=True):
        baseUrl = url + self.name+"/"+dir
        print(baseUrl)
        with urllib.request.urlopen(baseUrl) as data:
            if secure:
                return self.decrypt_message(data.read())
            return (data.read())

    def updateLimit(self, limit):
        detailsPath = '/Product/' + self.name + '/details'
        commit = "Used {} emails".format(limit)
        updateFile(detailsPath, commit, content=saveXmlDataSource(self.name,self.password,self.validationDate,int(self.mailLimitationValue)-limit))
        print(commit)
    def getEmail(self):
        data= self.getCompanyDataFromUrl('emails',secure=False)
        print(data)
        return data.decode("utf8")[:-1].replace("\r","").split("\n")# todo burası \r\n olacak


    def decrypt_message(self, encodedMessage):
        print(encodedMessage)
        # encodedMessage = encodedMessage('utf8')
        with open('private.pem') as data:
            privatekey = RSA.importKey(data.read())
            privatekey = rsaCry.new(privatekey)
        decoded_encrypted_msg = base64.b64decode(encodedMessage)
        decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
        return decoded_decrypted_msg

    def expDate(self,day):
        return (datetime.datetime.now() + datetime.timedelta(day)).timestamp()
    def isValid(self):
        today = datetime.datetime.now()
        t = datetime.datetime.strptime(self.validationDate,"%Y-%m-%d %H:%M:%S.%f")

        if t > today:
            print(t)
            return True
        return False

    def isLimit(self):
        result = self.mailLimitationValue
        if int(result) <= 0:
            return False
        return True

