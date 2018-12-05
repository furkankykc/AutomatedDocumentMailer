import sys
import sys, getopt

from Mailer.document import ismeOzelDavetiye


def readConfs():
    return dict("")


def send(confs):
    ismeOzelDavetiye(confs['taslakAdi'], str(confs['list']), confs['email'], str(confs['password']), str(['subject']),
                     confs['messageData'], "",
                     confs['smtpValue'],
                     None,
                     startPoint=confs['startPoint'],
                     ssl=confs['ssl']
                     )


if __name__ == '__main__':
    if sys.argv[-1] == '-help':
        print("-e:email\n-t:taslak\n-l:list\n-b:subject\n-d:message\n-f:smtp\n-i:start\n-c:ssl")
    elif sys.argv[-1] == '-resume':
        print("resume")
    myopts, args = getopt.getopt(sys.argv[1:], "t:l:e:h:d:r:f:i:c:b:")
    confs = {}
    for o, a in myopts:
        if o == '-t':
            confs['taslak'] = a
        elif o == '-l':
            confs['list'] = a
        elif o == '-e':
            confs['email'] = a
        elif o == '-b':
            confs['subject'] = a
        elif o == '-d':
            confs['messageData'] = a
        elif o == '-f':
            confs['smtpValue'] = a
        elif o == '-i':
            confs['startPoint'] = a
        elif o == '-c':
            confs['ssl'] = a
        else:
            confs = readConfs()
    print("Usage: %s -i input -o output" % sys.argv)
    # Display input and output file name passed as the args
    # send(confs)
