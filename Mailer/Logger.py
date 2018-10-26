



from datetime import datetime



class Logger:
    def __init__(self,log):
        self.file = "log.txt"
        # log = "{1}{0}{1}\n".format(datetime.now().__str__(), '-' * 20)
        self.log(log)

    # .split(' ')[1].split('.')[0]
    def log(self,log):
        log = "{0}{1}{2}\n".format(datetime.now().__str__(),'-->',log)
        self.write(log)

    def write(self,log):
        with open(self.file,'a') as file:
            file.write(log)

