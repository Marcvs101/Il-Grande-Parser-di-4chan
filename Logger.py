from datetime import datetime

class Logger:
    def __init__(self, filename):
        self.filename = filename

        # create or reset file
        f = open(filename, "w")
        f.close()

    def write(self, s):
        f = open(self.filename, "a")
        timestamp = str(datetime.now())
        f.write(s+" ["+timestamp[0:timestamp.rfind(".")]+"]"+"\n")
        f.close()
