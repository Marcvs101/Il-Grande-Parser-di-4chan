from ChanGet import ChanBoardWatchdog
from ChanGet import ChanThreadWatchdog
from ChanGet import Filter
from Logger import Logger

logger= Logger("log.txt")

BOARD = input("inserire il nome della board: ").strip()
BoardWatch = ChanBoardWatchdog(BOARD)
BoardWatch.setDeepFilterMode(True)
BoardWatch.setLogger(logger)
f = Filter("filtro1", {"anon"})
BoardWatch.addFilterToSet(f)

print("Starting...")
BoardWatch.start()
input("crepa? ")
BoardWatch.stop()
