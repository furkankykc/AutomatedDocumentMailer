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
    "diamond": [9999999999, 12],  # 3699
    "special": [100000, 3]  # 3699
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

# subscribtion("xbet", "8989", subType["special"])
# print(subType["gold"][0])
# updateEmails("xbet",["x-bet@x-'news.site",'x-bet-co@x-'news.site'])
# subscribtion("hilbet", "123@Marketing", subType["special"])
emails= [
'news@topbookmakerlist.com',
'news1@topbookmakerlist.com', 
'news2@topbookmakerlist.com', 
'news3@topbookmakerlist.com', 
'news4@topbookmakerlist.com', 
'news5@topbookmakerlist.com', 
'news6@topbookmakerlist.com', 
'news7@topbookmakerlist.com', 
'news8@topbookmakerlist.com', 
'news9@topbookmakerlist.com', 
'news10@topbookmakerlist.com', 
'news11@topbookmakerlist.com', 
'news12@topbookmakerlist.com', 
'news13@topbookmakerlist.com', 
'news14@topbookmakerlist.com', 
'news15@topbookmakerlist.com', 
'news16@topbookmakerlist.com', 
'news17@topbookmakerlist.com', 
'news18@topbookmakerlist.com', 
'news19@topbookmakerlist.com', 
'news20@topbookmakerlist.com', 
'news21@topbookmakerlist.com', 
'news22@topbookmakerlist.com', 
'news23@topbookmakerlist.com', 
'news24@topbookmakerlist.com', 
'news25@topbookmakerlist.com', 
'news26@topbookmakerlist.com', 
'news27@topbookmakerlist.com', 
'news28@topbookmakerlist.com', 
'news29@topbookmakerlist.com', 
'news30@topbookmakerlist.com',
'news31@topbookmakerlist.com', 
'news32@topbookmakerlist.com', 
'news33@topbookmakerlist.com', 
'news34@topbookmakerlist.com', 
'news35@topbookmakerlist.com', 
'news36@topbookmakerlist.com', 
'news37@topbookmakerlist.com', 
'news38@topbookmakerlist.com', 
'news39@topbookmakerlist.com', 
'news40@topbookmakerlist.com', 
'news41@topbookmakerlist.com', 
'news42@topbookmakerlist.com', 
'news43@topbookmakerlist.com', 
'news44@topbookmakerlist.com', 
'news45@topbookmakerlist.com', 
'news46@topbookmakerlist.com', 
'news48@topbookmakerlist.com',
'news49@topbookmakerlist.com',
'news50@topbookmakerlist.com',
]
updateEmails('hilbet',emails)