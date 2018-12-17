import re
import smtplib
import socket

import chardet
import pandas as pd
import dns.resolver
import csv
import xlrd

class MailVertifyer:
    def __init__(self,list,progressbar =None):
        self.new= []
            # for i in self.new:
            #     employee_writer.writerow([i])
        with open(list,"rb") as f:
            result = chardet.detect(f.read())  # or readline if the file is large
        print(result)
        refrence = pd.read_excel(list, encoding='utf-8')
        self.orjList = refrence['EMAİL'].tolist()
        if progressbar is not None:
            progressbar["maximum"] = len(self.orjList)
            progressbar["value"] =0
            progressbar.start()
        for mail in self.orjList:
            if vertify(mail):
                self.new.append(mail)
                if progressbar is not None:
                    progressbar["value"] = progressbar["value"]+1
                    progressbar.update()
                print(mail)

        ref = pd.DataFrame()
        ref['EMAİL']=self.new
        pd.DataFrame(ref).to_excel(list,index=False)
        if progressbar is not None:
            progressbar.stop()

    def getInfo(self):
        return "Value of Broken Mails \nRemoved : {} From:{} address".format(str(len(self.orjList)-len(self.new)),str(len(self.orjList)))

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
def fixEncodingList(list):
    refrence = pd.read_excel(list, encoding='utf-8')
    soyad = refrence['SOYAD'].tolist()
    ad = refrence['AD'].tolist()
    for i in range(len(ad)):
        try:
            ad[i]=fixStr(ad[i].encode("utf8"))
            soyad[i]=fixStr(soyad[i].encode("utf8"))
        except:
            continue
    refrence['AD'] = ad
    refrence['SOYAD']= soyad
    pd.DataFrame(refrence).to_excel(list, index=False)


def fixStr(string):
    name = ""
    try:
        name=string.decode('utf-8-sig').encode('latin1').decode('utf8')
        print(string ,":",name)
    except:
        return name
    return(name.title())



#list = "/home/furkankykc/Downloads/data1.xlsx"
# ad =['furkan','fatih']
# soyad =['kıyıkcı','kıyıkcı']
# email =['test@gmail.com','test']
# ref =pd.DataFrame()
# ref['AD']=ad
# ref['SOYAD']= soyad
# ref['EMAİL']=email
# pd.DataFrame(ref).to_excel(list, index=False)
# fixEncodingList(list)
# with open(list, "rb") as f:
#     result = chardet.detect(f.read())  # or readline if the file is large
# print(result)
# refrence = pd.read_excel(list, encoding='utf-8')
# for i in refrence['EMAİL']:
#     print(i)
#     # print(i['AD'])
#MailVertifyer(list)