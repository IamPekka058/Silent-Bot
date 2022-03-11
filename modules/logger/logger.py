import datetime
from os import path

types = {
    1:"[WARNUNG] ",
    2:"[INFO] ",
    3:"[DISCORD] "
    }
def log(type, msg):
    time = datetime.datetime.now()
    with open(path.join(__file__, "..", "..","..", "logs", "log"+str(time.strftime("%m%d%Y")+".txt")), "a+") as file:
        file.write("["+time.strftime("%H:%M:%S")+"] "+types[type]+msg+"\n")
        file.flush()
        file.close()
