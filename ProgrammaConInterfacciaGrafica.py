# pip install appjar
from appJar import gui
from ChanGet import ChanBoardWatchdog
from ChanGet import ChanThreadWatchdog
from ChanGet import Filter
from Logger import Logger

board_dict = {}
global_filter_set = set()

targeted_board = "GLOBAL"

finestra = gui("Il Grande Parser di 4Chan","600x300")

# Util
def add_board_util(board):
    if (board in board_dict): return
    board_dict[board] = {}
    board_dict[board]["Watchdog"] = ChanBoardWatchdog(board)
    board_dict[board]["Filtri"] = set()
    logf = Logger("log_"+board+".txt")
    board_dict[board]["Watchdog"].setLogger(logf)
    board_dict[board]["Watchdog"].start()

def remove_board_util(board):
    if (board in board_dict):
        board_dict[board]["Watchdog"].stop()
        for i in board_dict[board]["Filtri"]:
            try: finestra.removeLabel("ThreadFilterEntry<"+str(i)+">")
            except: print("Non trovato "+str(i))
        for i in board_dict[board]["Watchdog"].getMonitoredSet():
            try: finestra.removeLabel("ThreadListEntry<"+str(i)+">")
            except: print("Non trovato "+str(i))
        board_dict.pop(board,None)

def apply_filter_util(board,filter_set = set()):
    if (board in board_dict):
        board_dict[board]["Watchdog"].setFilterSet(filter_set)
        board_dict[board]["Filtri"] = filter_set

def create_filter_util(string):
    f_set = set()
    for i in string.split(" "):
        word = i.strip().lower()
        if (word == ""): continue
        f_set.add(word)
    if (len(f_set) > 0):
        return Filter(string.strip().lower(),f_set)
    return None

# Bottoni
def main_add_board_button():
    show_board_gui_new()

def new_board_confirm_button():
    board = finestra.getEntry("NuovaBoardEntry")
    if (board == None or board == ""):
        update_board_gui_main()
        hide_board_gui_new()
        return
    add_board_util(board)
    update_board_gui_main()
    hide_board_gui_new()

def main_add_filter_button():
    print("NOT IMPLEMENTED YET")

def goto_board(var):
    global targeted_board
    targeted_board = var
    show_thread_gui_main(var)

def thread_add_filter_button():
    show_filter_gui_new()

def new_filter_confirm_button():
    f = create_filter_util(finestra.getEntry("NuovoFiltroEntry"))
    if (f == None):
        hide_filter_gui_new()
        update_thread_gui_main(targeted_board)
        return
    board_dict[targeted_board]["Filtri"].add(f)
    apply_filter_util(targeted_board,board_dict[targeted_board]["Filtri"])
    hide_filter_gui_new()
    update_thread_gui_main(targeted_board)

def delete_board_button():
    global targeted_board
    try: finestra.removeButton(str(targeted_board))
    except: print("Non trovato "+str(targeted_board))
    for i in board_dict[targeted_board]["Watchdog"].getMonitoredSet():
        try: finestra.removeLabel("ThreadListEntry<"+str(i)+">")
        except: print("Non trovato "+str(i))
    remove_board_util(targeted_board)
    hide_thread_gui_main()
    hide_filter_gui_new()
    targeted_board = "GLOBAL"

# Costruttori
def init_board_gui_main():
    finestra.setBg("grey")
    finestra.setFont(18)

    finestra.startScrollPane("MainBoards", row=0, column=0)
    finestra.addLabel("MainBoardsTitolo", "Board monitorate")
    finestra.addButton("Aggiungi nuova board",main_add_board_button)
    finestra.stopScrollPane()

    finestra.startScrollPane("MainFiltri", row=1, column=0)
    finestra.addLabel("MainFiltriTitolo", "Filtri globali")
    finestra.addButton("Aggiungi nuovo filtro globale",main_add_filter_button)
    finestra.stopScrollPane()

def init_board_gui_new():
    finestra.startSubWindow("NuovaBoardFinestra",modal=True)
    finestra.addLabel("NuovaBoardTitolo","Inserire la board da monitorare, lasciare vuoto per annullare")
    finestra.addEntry("NuovaBoardEntry")
    finestra.addButton("Procedi con la board",new_board_confirm_button)
    finestra.stopSubWindow()

def init_thread_gui_main():
    finestra.startSubWindow("ThreadFinestra",modal=False)
    finestra.addLabel("ThreadTitolo","ERROR")
    
    finestra.startScrollPane("ThreadFiltri", row=1, column=0)
    finestra.addLabel("ThreadFiltriTitolo", "Filtri")
    finestra.addButton("Aggiungi nuovo filtro",thread_add_filter_button)
    finestra.stopScrollPane()

    finestra.startScrollPane("ThreadTrovati", row=2, column=0)
    finestra.addLabel("ThreadTrovatiTitolo", "Trovati")
    finestra.stopScrollPane()

    finestra.addButton("ThreadDelete",delete_board_button)
    finestra.stopSubWindow()

def init_filter_gui_new():
    finestra.startSubWindow("NuovoFiltroFinestra",modal=True)
    finestra.addLabel("NuovoFiltroTitolo","Inserire una o più parole separate da spazi da monitorare, lasciare vuoto per annullare")
    finestra.addEntry("NuovoFiltroEntry")
    finestra.addButton("Procedi con il filtro",new_filter_confirm_button)
    finestra.stopSubWindow()

# Azionatori
def show_board_gui_new():
    finestra.showSubWindow("NuovaBoardFinestra", hide = False)

def show_thread_gui_main(thread):
    update_thread_gui_main(thread)
    finestra.showSubWindow("ThreadFinestra", hide = False)

def show_filter_gui_new():
    finestra.showSubWindow("NuovoFiltroFinestra", hide = False)

# Nasconditori
def hide_board_gui_new():
    finestra.hideSubWindow("NuovaBoardFinestra", useStopFunction = False)
    finestra.confirmHideSubWindow("NuovaBoardFinestra")

def hide_thread_gui_main():
    finestra.hideSubWindow("ThreadFinestra", useStopFunction = False)
    finestra.confirmHideSubWindow("ThreadFinestra")

def hide_filter_gui_new():
    finestra.hideSubWindow("NuovoFiltroFinestra", useStopFunction = False)
    finestra.confirmHideSubWindow("NuovoFiltroFinestra")

# Aggiornatori
def update_board_gui_main():
    finestra.openScrollPane("MainBoards")
    for i in board_dict:
        try: finestra.removeButton(str(i))
        except: print("Non trovato "+str(i))

    for i in board_dict:
        try: finestra.addButton(str(i),goto_board)
        except: print("Errore generico "+str(i))        
    finestra.stopScrollPane()

    finestra.openScrollPane("MainFiltri")
    
    finestra.stopScrollPane()

def update_thread_gui_main(thread):
    finestra.setLabel("ThreadTitolo",thread)
    finestra.openScrollPane("ThreadFiltri")
    for thr in board_dict:
        for i in board_dict[thr]["Filtri"]:
            try: finestra.removeLabel("ThreadFilterEntry<"+str(i)+">")
            except: print("Non trovato "+str(i))

    for i in board_dict[thread]["Filtri"]:
        try: finestra.addLabel("ThreadFilterEntry<"+str(i)+">",str(i))
        except: print("Non trovato "+str(i))
    finestra.stopScrollPane()
    
    finestra.openScrollPane("ThreadTrovati")
    for thr in board_dict:
        for i in board_dict[thr]["Watchdog"].getMonitoredSet():
            try: finestra.removeLabel("ThreadListEntry<"+str(i)+">")
            except: print("Non trovato "+str(i))

    for i in board_dict[thread]["Watchdog"].getMonitoredSet():
        try: finestra.addLabel("ThreadListEntry<"+str(i)+">",str(i))
        except: print("Non trovato "+str(i))
    finestra.stopScrollPane()

init_board_gui_main()
init_board_gui_new()
init_thread_gui_main()
init_filter_gui_new()

finestra.go()
