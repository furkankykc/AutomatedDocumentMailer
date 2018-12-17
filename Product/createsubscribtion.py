
from github import Github
import datetime
from Utils.xmlOperations import *
from Utils.github import *

limit = 'limit'
validationDate = 'validationDate'
password = 'password'
subType = {
    "bronze": [20000, 1],  # 169
    "silver": [100000, 1],  # 289
    "platinium": [500000, 1],  # 699
    "gold": [500000, 6],  # 1499
    "diamond": [9999999999, 1],  # 3699
    "special": [100000, 3] , # 3699
    "admin": [100000, 12]  # 3699
}


def subscribtion(name, password, subType):
    basePath = '/Product/' + name
    detailsPath = '/Product/' + name + '/details'
    emailPath = '/Product/' + name + '/emails'
    updateFile(detailsPath,
               "Creating {0} 's {1} months subscription with {2} limit.".format(name, subType[1], subType[0]),
               upgradeLimits(name, password, expDate(subType[1] * 30), subType[0]))

    updateFile(emailPath, "Creating {0} 's email directory".format(name), "")


def updateEmails(name, emails):
    temp = ''
    basePath = '/Product/' + name
    emailPath = basePath + '/emails'
    for i in emails:
        temp += i + '\r\n'
    updateFile(emailPath, "Updating emails for {}".format(name), temp)
    print("Updating emails for {}".format(name))


def expDate(day):
    return (datetime.datetime.now() + datetime.timedelta(day))

#subscribtion("wikybet", "wikybet8989", subType["diamond"])
# # print(subType["gold"][0])
# # updateEmails("xbet",["x-bet@x-'news.site",'x-bet-co@x-'news.site'])
# # subscribtion("hilbet", "123@Marketing", subType["special"])
emails= [
'root@wikybetbonus.com',
'bonus@wikybetbonus.com',
]
subscribtion('wikybet','wikybet8989',subType["diamond"])
updateEmails('wikybet',emails)
