import datetime
import time
import urllib.request
import xmltodict
import datetime
from Crypto.PublicKey import RSA
import base64
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


    def getCompanyDataFromUrl(self,dir):
        baseUrl = url + self.name+"/"+dir
        print(baseUrl)
        with urllib.request.urlopen(baseUrl) as data:
            return self.decrypt_message(data.read())
    def getEmail(self):
        data= self.getCompanyDataFromUrl('emails')
        print(data)
        return data.decode("utf8")[:-1].split("\r\n")


    def decrypt_message(self, encodedMessage):
        print(encodedMessage)
        # encodedMessage = encodedMessage('utf8')
        with open('private.pem') as data:
            privatekey = RSA.importKey(data.read())
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

