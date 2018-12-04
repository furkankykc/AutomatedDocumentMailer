import re
import smtplib
import socket

import chardet
import pandas as pd
import dns.resolver
import csv
import xlrd

class MailVertifyer:
    def __init__(self,list):
        self.new= []
            # for i in self.new:
            #     employee_writer.writerow([i])
        with open(list,"rb") as f:
            result = chardet.detect(f.read())  # or readline if the file is large
        print(result)
        refrence = pd.read_excel(list, encoding='utf-8')
        self.orjList = refrence['EMAİL'].tolist()
        for mail in self.orjList:
            if vertify(mail):
                self.new.append(mail)
                print(mail)

        pd.DataFrame(self.new, columns=["EMAİL"]).to_excel(list,index=False)



    def getInfo(self):
        return "Value of Broken Mails \nRemoved : {}".format(str(len(self.orjList)-len(self.new)))

    def list(self):
        return self.new
def vertify(address):
    regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
    addressToVerify = str(address)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.lifetime = 1

    # Syntax check
    match = re.match(regex, addressToVerify)
    if match != None:
        try:
            # Get domain for DNS lookup
            splitAddress = addressToVerify.split('@')
            domain = str(splitAddress[1])
            # print('Domain:', domain)
            records = resolver.query(domain, 'MX')
            mxRecord = records[0].exchange
            mxRecord = str(mxRecord)
            # print(mxRecord)
            # # SMTP Conversation
            # server.connect(mxRecord, 587)
            # server.helo(server.local_hostname)  ### server.local_hostname(Get local server hostname)
            return True
        except Exception as e:
            return False
    # MX record lookup
    return False
