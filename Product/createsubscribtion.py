from xml.dom import minidom

from github import Github
import datetime

limit = 'limit'
validationDate = 'validationDate'
password = 'password'
subType = {
    "bronze":[20000,1],#169
    "silver":[100000,1],#289
    "platinium":[500000,1],#699
    "gold":[500000,6],#1499
    "diamond":[9999999999,12]#3699
}
def getGitRepo():
    g = Github("furkankykc", "8989323846q")
    return g.get_user().get_repo('EmailAccounts')


def subscribtion(name, password, subType):
    filePath = '/Product/' + name + '/details'
    try:
        getGitRepo().create_file(filePath, "Creating {0} 's {1} months subscription with {2} limit.".format(name,subType[1],subType[0]), saveXmlDataSource(name,password,expDate(subType[1]*30),subType[0]))
        print("Creating {0} 's {1} months subscription with {2} limit.".format(name,subType[1],subType[0]))
    except:
        file = getGitRepo().get_file_contents(filePath)
        getGitRepo().update_file(filePath, "Updating {0} 's {1} months subscription with {2} limit.".format(name,subType[1],subType[0]),saveXmlDataSource(name,password,expDate(subType[1]*30),subType[0]), file.sha)
        print( "Updating {0} 's {1} months subscription with {2} limit.".format(name,subType[1],subType[0]))
def expDate(day):
    return (datetime.datetime.now() + datetime.timedelta(day))
def saveXmlDataSource(name, pw,vd,l):
    return prettify(
        xmlConverter(name,
                          xmlConverter(password, pw),
                          xmlConverter(validationDate, vd),
                          xmlConverter(limit,l),
                          )
    )

def xmlConverter(xmlColon, *variable):
        return ("<{0}>" + (('%s' * len(variable)).lstrip() % variable) + "</{0}>").format(xmlColon)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    reparsed = minidom.parseString(elem)
    var = reparsed.toprettyxml(indent="\t")
    print(var)
    return var
subscribtion("deneme","8989", subType["diamond"])
# print(subType["gold"][0])