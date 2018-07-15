import ChanGet
import re


TARGET = input("Fornire il link al thread: ").strip()
BOARD = re.sub("http[s]?://boards.4chan.org/","",TARGET)
BOARD = re.sub("/thread/[#p0-9]*","",BOARD)
THREAD = re.sub("http[s]?://boards.4chan.org/[0-9 a-zA-Z]*/thread/","",TARGET)
THREAD = re.sub("#p[0-9]*","",THREAD)

print(BOARD, THREAD)

ThreadWatch = ChanGet.ChanThreadWatchdog(BOARD,THREAD)
ThreadWatch.start()

input("Premere invio per chiudere")
ThreadWatch.stop()
