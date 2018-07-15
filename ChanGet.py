from urllib.request import Request
import urllib.error
import threading
import time
import os
import re

#pip install bs4
from bs4 import BeautifulSoup

# Note sul programma
# Simpatico coso che pesca dal cestino dell'umido del web
# Per ora può essere usato per pescare il testo nella prima pagina di una qualsiasi board
# per poi farci riconoscimento di parole chiave o altro

# Nota sull'uso dei demoni
# Instanziare un demone ChanBoardWatchdog per ogni board che si vuole controllare
# Instanziare un demone ChanThreadWatchdog per ogni thread che si vuole controllare
# Usare la funzione .start() per lanciare i demoni
# Recuperare informazioni utili attraverso le funzioni get

# In futuro il demone guarderà a tutte e 10 le pagine di immondizia della board
# In futuro saranno implementati eventi


# Classe filtro
class Filter:
    # Costruttore
    def __init__(self, name, words):
        self.name = name.lower()
        self.words = set()
        for i in words:
            self.words.add(i.lower())

    # Funzione di valutazione
    def evaluate(self, s):
        for word in self.words:
            if (re.search(word,str(s).lower()) == None):
                return False
        return True


# Demone di una Board
class ChanBoardWatchdog (threading.Thread):
    # Costruttore
    def __init__(self,board,filters = set()):
        threading.Thread.__init__(self)
        # Variabili di istanza
        self.board = board
        self.deepFilter = False
        self.notify = False
        # Strutture interne
        self.parsed_threads_html = {}
        self.parsed_threads_text = {}
        self.filters = filters
        # Strutture aux
        self.thread_monitorati = set()
        self.monitor_attivi = set()
        # Variabili per il threading
        self.frequenza = 10
        self.Attivo = False
    
    # Metodo Run
    def run(self):
        self.Attivo = True
        while(self.Attivo):
            self.__Fetch__()
            accepted = self.__Condizioni__(self.deepFilter)
            for thread in accepted:
                monitor = self.SpawnThreadWatchdog(thread)
                self.monitor_attivi.add(monitor)
                monitor.start()
                self.thread_monitorati.add(thread)
            time.sleep(self.frequenza)

    # Ferma il demone
    def stop(self):
        self.Attivo = False
        for monitor in self.monitor_attivi:
            monitor.stop()

    # Getter
    def getHTMLRawDict(self):
        return self.parsed_threads_html

    def getTextDict(self):
        return self.parsed_threads_text

    def getFilterSet():
        return self.filters

    # Setter
    def setFilterSet(self,filters = set()):
        self.filters = filters

    def setDeepFilterMode(self,mode = False):
        self.deepFilter = mode

    def setNotificationsMode(self, mode = False):
        self.notify = mode

    # Add set of words to be evaluated in AND
    def addFilterToSet(self,new_filter):
        self.filters.add(new_filter)

    # Remove set of words from filter
    def removeFilterToSet(self,target_filter):
        self.filters.remove(target_filter)

    # Ascolta un thread
    def SpawnThreadWatchdog(self,thread):
        watchdog = ChanThreadWatchdog(self.board,thread)
        return watchdog

    # Controllo condizioni
    def __Condizioni__(self,profondo = False):
        ret = set()
        
        for thread in self.parsed_threads_text:
            if (thread in self.thread_monitorati):
                continue
            # Controllo profondo, le chiamate http sono bloccanti
            if (profondo):
                scanner = self.SpawnThreadWatchdog(thread)
                scanner.__Fetch__()
                threads_text = scanner.getTextDict()
            # Controllo superficiale
            else:
                threads_text = self.parsed_threads_text[thread]

            for fil in self.filters:
                accept = False
                if (fil.evaluate(threads_text["OP_Post"])):
                    accept = True
                for reply in threads_text["Replies"]:
                    if (fil.evaluate(threads_text["Replies"][reply])):
                        accept = True
                if (accept):
                    if (self.notify):
                        print("thread matched condition: "+str(thread))
                    ret.add(thread)
        return ret

    # Locatore di testo
    def __ExtractText__(self):
        self.parsed_threads_text = {}
        for thread in self.parsed_threads_html:
            self.parsed_threads_text[thread] = {}
            self.parsed_threads_text[thread]["OP_Post"] = None
            self.parsed_threads_text[thread]["Replies"] = {}

            txt_c = self.parsed_threads_html[thread]["OP_Post"].find_all(class_="postMessage")
            for txt in txt_c:
                if (not(txt==None)):
                    self.parsed_threads_text[thread]["OP_Post"] = txt.getText()

            for i in self.parsed_threads_html[thread]["Replies"]:
                txt_c = self.parsed_threads_html[thread]["Replies"][i].find_all(class_="postMessage")
                for txt in txt_c:
                    if (not(txt==None)):
                        self.parsed_threads_text[thread]["Replies"][i] = txt.getText()

    # Parser
    def __Parse__(self,pageSoup):
        Threads = pageSoup.find_all(class_="thread")
        self.parsed_threads_html = {}

        for thread in Threads:
            OPPost = thread.find(class_="postContainer opContainer")
            Replies = thread.find_all(class_="postContainer replyContainer")

            self.parsed_threads_html[str(thread["id"]).replace("t","")] = {}
            self.parsed_threads_html[str(thread["id"]).replace("t","")]["OP_Post"] = OPPost
            self.parsed_threads_html[str(thread["id"]).replace("t","")]["Replies"] = {}

            for i in Replies:
                self.parsed_threads_html[str(thread["id"]).replace("t","")]["Replies"][str(i["id"]).replace("pc","")] = i

        self.__ExtractText__()

    # Fetcher
    def __Fetch__(self):
        # Necessaria una richiesta GET con campo User-Agent nell'header
        Req = Request("https://www.4chan.org/"+self.board+"/")
        Req.add_header("User-Agent","TROLOLOLOLOLO")
        
        conn = urllib.request.urlopen(Req)
        page = str(conn.read())
        conn.close()

        self.__Parse__(BeautifulSoup(page,"html.parser"))


# Demone di un thread
class ChanThreadWatchdog (threading.Thread):
    # Costruttore
    def __init__(self,board,thread):
        threading.Thread.__init__(self)
        # Variabili di istanza
        self.board = board
        self.thread = thread
        # Strutture interne
        self.parsed_text = {}
        self.parsed_text["OP_Post"] = None
        self.parsed_text["Replies"] = {}
        self.parsed_html = {}
        self.parsed_html["OP_Post"] = None
        self.parsed_html["Replies"] = {}
        self.parsed_files = {}
        self.parsed_files["OP_Post"] = None
        self.parsed_files["Replies"] = {}
        # Strutture secondarie
        self.available_files = set()
        self.available_text = set()
        self.saved_files = set()
        self.saved_text = set()
        # Variabili per il threading
        self.frequenza = 10
        self.Attivo = False
    
    # Metodo Run
    def run(self):
        self.Attivo = True
        while(self.Attivo):
            self.__Fetch__()
            self.SaveText()
            self.SaveFiles()
            time.sleep(self.frequenza)

    # Ferma il demone
    def stop(self):
        self.Attivo = False

    # Getter
    def getHTMLRawDict(self):
        return self.parsed_html

    def getFileDict(self):
        return self.parsed_files

    def getTextDict(self):
        return self.parsed_text

    # Salvataggio su disco del testo
    def SaveText(self):
        directory = os.path.dirname(self.thread+"/")
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        if (not(self.parsed_text["OP_Post"] == None) and ("OP_Post" in self.available_text)):
            file = open(directory+"/Text.txt",'w')
            file.write("Board: "+self.board+", Thread n. ("+self.thread+")"+"\n")
            file.write("OP Post: "+self.parsed_text["OP_Post"]+"\n")
            file.close()

            self.available_text.remove("OP_Post")
            self.saved_text.add("OP_Post")

        for i in self.parsed_text["Replies"]:
            file = open(directory+"/Text.txt",'a')
            if (i in self.available_text):
                file.write("Reply <"+i+">: "+self.parsed_text["Replies"][i]+"\n")

                self.available_text.remove(i)
                self.saved_text.add(i)
                
            file.close()
    
    # Salvataggio su disco dei file
    def SaveFiles(self):
        directory = os.path.dirname(self.thread+"/files/")
        
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        if (not(self.parsed_files["OP_Post"] == None) and ("OP_Post" in self.available_files)):
            Req = Request("http:"+self.parsed_files["OP_Post"])
            Req.add_header("User-Agent","TROLOLOLOLOLO")
        
            conn = urllib.request.urlopen(Req)
            page = conn.read()
            conn.close()

            file = open(directory+"/"+re.sub("//is[0-9]*.4chan.org/"+self.board+"/","",self.parsed_files["OP_Post"]),'wb')
            file.write(page)
            file.close()

            self.available_files.remove("OP_Post")
            self.saved_files.add("OP_Post")

        for i in self.parsed_files["Replies"]:
            if (i in self.available_files):
                Req = Request("http:"+self.parsed_files["Replies"][i])
                Req.add_header("User-Agent","TROLOLOLOLOLO")
            
                conn = urllib.request.urlopen(Req)
                page = conn.read()
                conn.close()

                file = open(directory+"/"+re.sub("//is[0-9]*.4chan.org/"+self.board+"/","",self.parsed_files["Replies"][i]),'wb')
                file.write(page)
                file.close()

                self.available_files.remove(i)
                self.saved_files.add(i)

    # Locatore di file
    def __ExtractFiles__(self):
        self.parsed_files["OP_Post"] = None
        self.parsed_files["Replies"] = {}
        
        img_c = self.parsed_html["OP_Post"].find_all(class_="fileThumb")
        for img in img_c:
            if (not(img==None)):
                self.parsed_files["OP_Post"] = img["href"]
                if (not ("OP_Post" in self.saved_files)):
                    self.available_files.add("OP_Post")
        
        for i in self.parsed_html["Replies"]:
            img_c = self.parsed_html["Replies"][i].find_all(class_="fileThumb")
            for img in img_c:
                if (not(img==None)):
                    self.parsed_files["Replies"][i] = img["href"]
                    if (not (i in self.saved_files)):
                        self.available_files.add(i)

    # Locatore di testo
    def __ExtractText__(self):
        self.parsed_text["OP_Post"] = None
        self.parsed_text["Replies"] = {}
        
        txt_c = self.parsed_html["OP_Post"].find_all(class_="postMessage")
        for txt in txt_c:
            if (not(txt==None)):
                self.parsed_text["OP_Post"] = txt.getText()
                if (not ("OP_Post" in self.saved_text)):
                        self.available_text.add("OP_Post")
        
        for i in self.parsed_html["Replies"]:
            txt_c = self.parsed_html["Replies"][i].find_all(class_="postMessage")
            for txt in txt_c:
                if (not(txt==None)):
                    self.parsed_text["Replies"][i] = txt.getText()
                    if (not (i in self.saved_text)):
                        self.available_text.add(i)

    # Parser
    def __Parse__(self,threadSoup):
        OPPost = threadSoup.find(class_="postContainer opContainer")
        Replies = threadSoup.find_all(class_="postContainer replyContainer")

        self.parsed_html["OP_Post"] = OPPost
        self.parsed_html["Replies"] = {}

        for i in Replies:
            self.parsed_html["Replies"][str(i["id"]).replace("pc","")] = i

        self.__ExtractFiles__()
        self.__ExtractText__()

    # Fetcher
    def __Fetch__(self):
        # Necessaria una richiesta GET con campo User-Agent nell'header
        Req = Request("https://boards.4chan.org/"+self.board+"/thread/"+self.thread+"/")
        Req.add_header("User-Agent","TROLOLOLOLOLO")

        conn = urllib.request.urlopen(Req)
        thread = str(conn.read())
        conn.close()

        self.__Parse__(BeautifulSoup(thread,"html.parser"))


# Note sulla struttura di 4chan

# THREADS
# class="thread"
# class="postContainer opContainer" && class="postContainer postContainer"
# class="postMessage" contiene il testo
# class="fileThumb" contiene immagini nel campo href

# BOARD
# class="board"
# class="thread"
