import sys
import sys, getopt
import configparser
from Mailer.document import ismeOzelDavetiye


def readConfs():
    try:
        ssl = ConfigSectionMap("Config")['ssl']
        smtp = ConfigSectionMap("Config")['smtp']
        start = ConfigSectionMap("Message")['start']
        email = ConfigSectionMap("Auth")['email']
        password = ConfigSectionMap("Auth")['password']
        subject = ConfigSectionMap("Message")['subject']
        list = ConfigSectionMap("Files")['list']
        message = ConfigSectionMap("Files")['message']
    except:
        createDefault()
    return locals()


def send(confs):
    ismeOzelDavetiye("",str(confs['list']), confs['email'], str(confs['password']), str(['subject']),
                     confs['message'], "",
                     confs['smtp'],
                     None,
                     startPoint=confs['start'],
                     ssl=confs['ssl']
                     )


def ConfigSectionMap(section):
    Config = configparser.ConfigParser()
    Config.read("conf.ini")
    return Config[section]

def createDefault():
    confs = {}
    confs['password'] = "examplePass"
    confs['list'] = "list.xlsx"
    confs['email'] = "example@domain.com"
    confs['subject'] = "Example"
    confs['message'] = "message.html"
    confs['smtp'] = "mail.example.domain.com"
    confs['start'] = "0"
    confs['ssl'] = "No"
    createConfig(confs)

def createConfig(confs):
    cfgfile = open("conf.ini", 'w+')
    Config = configparser.ConfigParser()


    # add the settings to the structure of the file, and lets write it out...
    Config.add_section('Auth')
    Config.add_section('Files')
    Config.add_section('Message')
    Config.add_section('Config')
    Config.set('Config', 'ssl', confs['ssl'])
    Config.set('Config', 'smtp', confs['smtp'])
    Config.set('Message', 'start', confs['start'])
    Config.set('Message', 'subject', confs['subject'])
    Config.set('Auth', 'email', confs['email'])
    Config.set('Auth', 'password', confs['password'])
    Config.set('Files', 'list', confs['list'])
    Config.set('Files', 'message', confs['message'])
    Config.write(cfgfile)
    cfgfile.close()


if __name__ == '__main__':
    if sys.argv[-1] == '-help':
        print("-e:email\n-t:taslak\n-l:list\n-b:subject\n-d:message\n-f:smtp\n-i:start\n-c:ssl")
    elif sys.argv[-1] == '-resume':
        print("resume")
    myopts, args = getopt.getopt(sys.argv[1:], "t:l:e:h:d:r:f:i:c:b:")

    confs = readConfs()
    #createConfig(confs)
    #     confs = readConfs()
    print("Usage: %s -i input -o output" % sys.argv)
    # Display input and output file name passed as the args
    send(confs)
# python3 commandline.py -e bonus@wikybet.com -d wikybet/wikybet.html -l wikybet/wiky2.xlsx -b Wikybet\ Geliyor!!! -f mail.wikybetbonus.com:587 -i 0 -ssl False -t s
