import datetime
import time
import urllib.request
import xmltodict
import datetime

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
        except:
            raise Exception
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
            return self.decrypt(data.read())
    def getEmail(self):
        return self.getCompanyDataFromUrl('email').read().decode("utf8")[:-1].split("\n")

    def encrypt(self, data):
        return data

    def decrypt(self, data):
        return data

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

m = Product("deneme")
print(m.isLimit())
print(m.isValid())