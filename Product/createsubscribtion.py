import base64
from xml.dom import minidom

from Crypto.PublicKey import RSA
from github import Github
import datetime

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


def getGitRepo():
    g = Github("furkankykc", "8989323846q")
    return g.get_user().get_repo('EmailAccounts')


def encrypt_message(message):
    message = message.encode("utf8")
    with open('private.pem') as data:
        privatekey = RSA.importKey(data.read())

    encrypted_msg = privatekey.publickey().encrypt(message, 32)[0]
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def updateFile(file, commitMessage, content):
    try:
        sha = getGitRepo().get_file_contents(file).sha
        getGitRepo().update_file(file, commitMessage,
                                 content,
                                 sha)

    except Exception as e:
        print(e)
        getGitRepo().create_file(file,
                                 commitMessage,
                                 content
                                 )


def subscribtion(name, password, subType):
    basePath = '/Product/' + name
    detailsPath = '/Product/' + name + '/details'
    emailPath = '/Product/' + name + '/emails'
    updateFile(detailsPath,
               "Creating {0} 's {1} months subscription with {2} limit.".format(name, subType[1], subType[0]),
               saveXmlDataSource(name, password, expDate(subType[1] * 30), subType[0]))

    updateFile(emailPath, "Creating {0} 's email directory".format(name), "")

def updateEmails(name,emails):
    k = ''
    basePath = '/Product/'+name
    emailPath = basePath+'/emails'
    for i in emails:
        k+= i+'\n'
    updateFile(emailPath,"Updating emails for {}".format(name),k)
    print("Updating emails for {}".format(name))
def expDate(day):
    return (datetime.datetime.now() + datetime.timedelta(day))


def saveXmlDataSource(name, pw, vd, l):
    return encrypt_message(prettify(
        xmlConverter(name,
                     xmlConverter(password, pw),
                     xmlConverter(validationDate, vd),
                     xmlConverter(limit, l)
                     )
    ))


def xmlConverter(xmlColon, *variable):
    return ("<{0}>" + (('%s' * len(variable)).lstrip() % variable) + "</{0}>").format(xmlColon)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    reparsed = minidom.parseString(elem)
    var = reparsed.toprettyxml(indent="\t")
    print(var)
    return var


# subscribtion("sad", "8989", subType["special"])
# print(subType["gold"][0])
updateEmails("deneme",["furkanfbr@gmail.com",'furkankykc@furkankykc.xyz'])