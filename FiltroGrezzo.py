from ChanGet import ChanBoardWatchdog
from ChanGet import ChanThreadWatchdog
from ChanGet import Filter

BOARD = input("inserire il nome della board: ").strip()
BoardWatch = ChanBoardWatchdog(BOARD)
BoardWatch.setDeepFilterMode(True)
BoardWatch.setNotificationsMode(True)
f = Filter("filtro1", {"anon"})
BoardWatch.addFilterToSet(f)

print("Starting...")
BoardWatch.start()
