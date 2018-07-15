from ChanGet import ChanBoardWatchdog
from ChanGet import ChanThreadWatchdog

# Variabili di configurazione per la prova
BOARD = input("inserire il nome della board: ").strip()

#try:

BoardWatch = ChanBoardWatchdog(BOARD)
BoardWatch.__Fetch__()

for thread in BoardWatch.getHTMLRawDict():
    tmp = thread
    print("Thread: "+thread)
    print("OP_Post")
    print(BoardWatch.getHTMLRawDict()[thread]["OP_Post"])
    print("")
    print("Replies")
    for reply in BoardWatch.getHTMLRawDict()[thread]["Replies"]:
        print(reply)
        print(BoardWatch.getHTMLRawDict()[thread]["Replies"][reply])
        print("")
    print("")
    

print("ANALIZZO IL TESTO")
print("")

for thread in BoardWatch.getTextDict():
    print(thread)
    print("OP_Post")
    print(BoardWatch.getTextDict()[thread]["OP_Post"])
    print("")
    print("Replies")
    for i in BoardWatch.getTextDict()[thread]["Replies"]:
        print(i)
        print(BoardWatch.getTextDict()[thread]["Replies"][i])
        print("")
    print("")


print("TEST DI UN SINGOLO THREAD")
print("SCANNING https://boards.4chan.org/"+BOARD+"/thread/"+tmp)
print("")

ThreadWatch = BoardWatch.SpawnThreadWatchdog(tmp)
ThreadWatch.__Fetch__()

print("OP_Post")
print(ThreadWatch.getHTMLRawDict()["OP_Post"])
print("")
print("Replies")
for i in ThreadWatch.getHTMLRawDict()["Replies"]:
    print(i)
    print(ThreadWatch.getHTMLRawDict()["Replies"][i])
    print("")


print("ANALIZZO IL TESTO")
print("")

print("OP_Post")
print(ThreadWatch.getTextDict()["OP_Post"])
print("")
print("Replies")
for i in ThreadWatch.getTextDict()["Replies"]:
    print(i)
    print(ThreadWatch.getTextDict()["Replies"][i])
print("")


print("ANALIZZO I FILE")
print("")

print("OP_Post")
print(ThreadWatch.getFileDict()["OP_Post"])
print("")
print("Replies")
for i in ThreadWatch.getFileDict()["Replies"]:
    print(i)
    print(ThreadWatch.getFileDict()["Replies"][i])
print("")


if(input("inserire 'salva' per salvare i file su disco: ").lower().strip()=="salva"):
    ThreadWatch.SaveText()
    ThreadWatch.SaveFiles()

input("Premere invio per chiudere")
    
#except (urllib.error.URLError, TimeoutError):
