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

def namer():

   #Create an instance of the canvas
   win = Tk()

   #Select the title of the window
   win.title("tutorialspoint.com")

   #Define the geometry of the window
   win.geometry("600x600")   

   ager_n = Label(win, text="agerato: ")
   ager_n.grid(row=0, column=0,)
   #ager_n.pack(padx = 1, pady = 1)
   ager = Button(win, text = "ager", command = lambda : win.destroy())
   ager.pack(padx = 1, pady = 1)
   ager.grid(row=0, column=1)
   name = ager.cget('text')

   bocl_n = Label(win, text="bocche di leone: ")
   bocl_n.pack(side = LEFT, padx = 1, pady = 1)
   bocl = Button(win, text = "bocl", command = lambda: win.destroy())
   bocl.pack(side = RIGHT, padx = 1, pady = 1)
   name = bocl.cget('text')

   bego_n = Label(win, text="begonie: ")
   bego_n.pack(side = LEFT, padx = 1, pady = 1)
   bego = Button(win, text = "bego", command = lambda: win.destroy())
   bego.pack(side = RIGHT,padx = 1, pady = 1)
   name = bego.cget('text')

   marg_n = Label(win, text="margherite: ")
   marg_n.pack(side = LEFT, padx = 1, pady = 1)
   marg = Button(win, text = "marg", command = lambda: win.destroy())
   marg.pack(side = RIGHT,padx = 1, pady = 1)
   name = marg.cget('text')

   cale_n = Label(win, text="calendule: ")
   cale_n.pack(side = LEFT, padx = 1, pady = 1)
   cale = Button(win, text = "marg", command = lambda: win.destroy())
   cale.pack(side = RIGHT,padx = 1, pady = 1)
   name = cale.cget('text')

   borr_n = Label(win, text="borraggine: ")
   borr_n.pack(side = LEFT, padx = 1, pady = 1)
   borr = Button(win, text = "borr", command = lambda: win.destroy())
   borr.pack(side = RIGHT,padx = 1, pady = 1)
   name = borr.cget('text')

   fior_n = Label(win, text="fiordaliso: ")
   fior_n.pack(side = LEFT, padx = 1, pady = 1)
   fior = Button(win, text = "fior", command = lambda: win.destroy())
   fior.pack(side = RIGHT,padx = 1, pady = 1)
   name = fior.cget('text')

   dagr_n = Label(win, text="dalie grandi: ")
   dagr_n.pack(side = LEFT, padx = 1, pady = 1)
   dagr = Button(win, text = "dagr", command = lambda: win.destroy())
   dagr.pack(side = RIGHT,padx = 1, pady = 1)
   name = dagr.cget('text')

   dapi_n = Label(win, text="dalie piccole: ")
   dapi_n.pack(side = LEFT, padx = 1, pady = 1)
   dapi = Button(win, text = "dapi", command = lambda: win.destroy())
   dapi.pack(side = RIGHT,padx = 1, pady = 1)
   name = dapi.cget('text')

   garo_n = Label(win, text="garofani: ")
   garo_n.pack(side = LEFT, padx = 1, pady = 1)
   garo = Button(win, text = "garo", command = lambda: win.destroy())
   garo.pack(side = RIGHT,padx = 1, pady = 1)
   name = garo.cget('text')

   fucs_n = Label(win, text="fucsie: ")
   fucs_n.pack(side = LEFT, padx = 1, pady = 1)
   fucs = Button(win, text = "fucs", command = lambda: win.destroy())
   fucs.pack(side = RIGHT,padx = 1, pady = 1)
   name = fucs.cget('text')

   impa_n = Label(win, text="impatients: ")
   impa_n.pack(side = LEFT, padx = 1, pady = 1)
   impa = Button(win, text = "impa", command = lambda: win.destroy())
   impa.pack(side = RIGHT,padx = 1, pady = 1)
   name = impa.cget('text')

   gera_n = Label(win, text="geranei: ")
   gera_n.pack(side = LEFT, padx = 1, pady = 1)
   gera = Button(win, text = "gera", command = lambda: win.destroy())
   gera.pack(side = RIGHT,padx = 1, pady = 1)
   name = gera.cget('text')

   prim_n = Label(win, text="primule: ")
   prim_n.pack(side = LEFT, padx = 1, pady = 1)
   prim = Button(win, text = "prim", command = lambda: win.destroy())
   prim.pack(side = RIGHT,padx = 1, pady = 1)
   name = prim.cget('text')

   rose_n = Label(win, text="rose: ")
   rose_n.pack(side = LEFT, padx = 1, pady = 1)
   rose = Button(win, text = "rose", command = lambda: win.destroy())
   rose.pack(side = RIGHT,padx = 1, pady = 1)
   name = rose.cget('text')

   taget_n = Label(win, text="tagete: ")
   taget_n.pack(side = LEFT, padx = 1, pady = 1)
   taget = Button(win, text = "tage", command = lambda: win.destroy())
   taget.pack(side = RIGHT,padx = 1, pady = 1)
   name = taget.cget('text')
   
   vipo_n = Label(win, text="violette piccole: ")
   vipo_n.pack(side = LEFT, padx = 1, pady = 1)
   vipo = Button(win, text = "vipo", command = lambda: win.destroy())
   vipo.pack(side = RIGHT,padx = 1, pady = 1)
   name = vipo.cget('text')

   viga_n = Label(win, text="violette grandi: ")
   viga_n.pack(side = LEFT, padx = 1, pady = 1)
   viga = Button(win, text = "viga", command = lambda: win.destroy())
   viga.pack(side = RIGHT,padx = 1, pady = 1)
   name = viga.cget('text')

   win.mainloop()
   return name


my_name = namer()
print(my_name)