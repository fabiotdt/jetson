#Import the tkinter library
from tkinter import *
import time

flowers = {
    'ager' : 'agerato',
    'bocl' : 'bocche_leone',
    'bego' : 'begonie',
    'marg' : 'margherite',
    'cale' : 'calendule',
    'borr' : 'borraggine',
    'fior' : 'fiordaliso',
    'dagr' : 'dalie_grandi',
    'dapi' : 'dalie_picole',
    'garo' : 'garofani',
    'fucs' : 'fucsie',
    'impa' : 'impatients',
    'gera' : 'geranei',
    'prim' : 'primule',
    'rose' : 'rose',
    'tage' : 'tagete',
    'vipo' : 'violette_piccole',
    'viga' : 'violette_grandi'
    }


def writer(name, writer_input, win):
    print(name)
    win.destroy()

def namer(writer_input):

   #Create an instance of the canvas
   win = Tk()

   #Select the title of the window
   win.title("tutorialspoint.com")

   #Define the geometry of the window
   win.geometry("600x600")   

   ager_n = Label(win, text="agerato: ")
   ager_n.grid(row=0, column=0, padx = 1, pady = 1)
   ager = Button(win, text = "ager", command = lambda : writer('ager', writer_input, win))
   ager.grid(row=0, column=1, padx = 1, pady = 1)

   bocl_n = Label(win, text="bocche di leone: ")
   bocl_n.grid(row=1, column=0, padx = 1, pady = 1)
   bocl = Button(win, text = "bocl", command = lambda: writer('bocl', writer_input, win))
   bocl.grid(row=1, column=1, padx = 1, pady = 1)

   bego_n = Label(win, text="begonie: ")
   bego_n.grid(row=2, column=0, padx = 1, pady = 1)
   bego = Button(win, text = "bego", command = lambda: writer('bego', writer_input, win))
   bego.grid(row=2, column=1, padx = 1, pady = 1)

   marg_n = Label(win, text="margherite: ")
   marg_n.grid(row=3, column=0, padx = 1, pady = 1)
   marg = Button(win, text = "marg", command = lambda: writer('marg', writer_input, win))
   marg.grid(row=3, column=1, padx = 1, pady = 1)

   cale_n = Label(win, text="calendule: ")
   cale_n.grid(row=4, column=0, padx = 1, pady = 1)
   cale = Button(win, text = "marg", command = lambda: writer('marg', writer_input, win))
   cale.grid(row=4, column=1, padx = 1, pady = 1)

   borr_n = Label(win, text="borraggine: ")
   borr_n.grid(row=5, column=0, padx = 1, pady = 1)
   borr = Button(win, text = "borr", command = lambda: writer('borr', writer_input, win))
   borr.grid(row=5, column=1, padx = 1, pady = 1)

   fior_n = Label(win, text="fiordaliso: ")
   fior_n.grid(row=6, column=0, padx = 1, pady = 1)
   fior = Button(win, text = "fior", command = lambda: writer('fior', writer_input, win))
   fior.grid(row=6, column=1, padx = 1, pady = 1)

   dagr_n = Label(win, text="dalie grandi: ")
   dagr_n.grid(row=7, column=0, padx = 1, pady = 1)
   dagr = Button(win, text = "dagr", command = lambda: writer('dagr', writer_input, win))
   dagr.grid(row=7, column=1, padx = 1, pady = 1)

   dapi_n = Label(win, text="dalie piccole: ")
   dapi_n.grid(row=8, column=0, padx = 1, pady = 1)
   dapi = Button(win, text = "dapi", command = lambda: writer('dapi', writer_input, win))
   dapi.grid(row=8, column=1, padx = 1, pady = 1)

   garo_n = Label(win, text="garofani: ")
   garo_n.grid(row=9, column=0, padx = 1, pady = 1)
   garo = Button(win, text = "garo", command = lambda: writer('garo', writer_input, win))
   garo.grid(row=9, column=1, padx = 1, pady = 1)

   fucs_n = Label(win, text="fucsie: ")
   fucs_n.grid(row=10, column=0, padx = 1, pady = 1)
   fucs = Button(win, text = "garo", command = lambda: writer('garo', writer_input, win))
   fucs.grid(row=10, column=1, padx = 1, pady = 1)

   impa_n = Label(win, text="impatients: ")
   impa_n.grid(row=11, column=0, padx = 1, pady = 1)
   impa = Button(win, text = "impa", command = lambda: writer('impa', writer_input, win))
   impa.grid(row=11, column=1, padx = 1, pady = 1)

   gera_n = Label(win, text="geranei: ")
   gera_n.grid(row=12, column=0, padx = 1, pady = 1)
   gera = Button(win, text = "gera", command = lambda: writer('gera', writer_input, win))
   gera.grid(row=12, column=1, padx = 1, pady = 1)

   prim_n = Label(win, text="primule: ")
   prim_n.grid(row=13, column=0, padx = 1, pady = 1)
   prim = Button(win, text = "prim", command = lambda: writer('prim', writer_input, win))
   prim.grid(row=13, column=1, padx = 1, pady = 1)

   rose_n = Label(win, text="rose: ")
   rose_n.grid(row=14, column=0, padx = 1, pady = 1)
   rose = Button(win, text = "rose", command = lambda: writer('rose', writer_input, win))
   rose.grid(row=14, column=1, padx = 1, pady = 1)

   taget_n = Label(win, text="tagete: ")
   taget_n.grid(row=15, column=0, padx = 1, pady = 1)
   taget = Button(win, text = "tage", command = lambda: writer('tage', writer_input, win))
   taget.grid(row=15, column=1, padx = 1, pady = 1)
   
   vipo_n = Label(win, text="violette piccole: ")
   vipo_n.grid(row=16, column=0, padx = 1, pady = 1)
   vipo = Button(win, text = "vipo", command = lambda: writer('vipo', writer_input, win))
   vipo.grid(row=16, column=1, padx = 1, pady = 1)

   viga_n = Label(win, text="violette grandi: ")
   viga_n.grid(row=17, column=0, padx = 1, pady = 1)
   viga = Button(win, text = "viga", command = lambda: writer('viga', writer_input, win))
   viga.grid(row=17, column=1, padx = 1, pady = 1)

   win.mainloop()


namer('ciao')