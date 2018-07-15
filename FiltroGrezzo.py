from ChanGet import ChanBoardWatchdog
from ChanGet import ChanThreadWatchdog
from ChanGet import Filter

BOARD = input("inserire il nome della board: ").strip()
BoardWatch = ChanBoardWatchdog(BOARD)
f = Filter("filtro1", {"prova"})
BoardWatch.addFilterToSet(f)

print("Starting...")
BoardWatch.start()
input("Crepa? ")
BoardWatch.stop()
