
import sys
from Mailer.document import ismeOzelDavetiye
from Mailer.loginform import LoginGui
from Mailer.gui import Gui

def start(*args):
    while len(sys.argv)!=7:
        print("mail,password,taslak,liste,konu,mesaj")
        print(len(sys.argv))
        return 0

    mail = sys.argv[1]
    password = sys.argv[2]
    taslak = sys.argv[3]
    liste = sys.argv[4]
    konu=sys.argv[5]
    mesaj = sys.argv[6]
    print([a for a in sys.argv])
    ismeOzelDavetiye(taslak,liste,mail,password,konu,mesaj)




if __name__ == "__main__":
    LoginGui()
    # Gui("xbet")
    #start(sys.argv)




