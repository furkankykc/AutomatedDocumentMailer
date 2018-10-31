
from xml.dom import minidom
from Utils.cryption import *
password = 'password'
validationDate = 'validationDate'
limit = 'limit'


def upgradeLimits(name, pw, vd, l):
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