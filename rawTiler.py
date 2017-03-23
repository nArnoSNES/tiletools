# ------------------------------------
#    Raw Tiler by n_Arno
#    Very simple raw SNES GFX editor.
#    Quick and Ugly dev: not efficient.
# ------------------------------------

import sys

from Tkinter import *
from tkMessageBox import *
import tkFileDialog

from tiles import *

# Temp ----------------------------
with open('title.pal','rb') as f:
    ps = Palettes.from_file(f)

with open('title.pic','rb') as f:
    ts = Tileset.from_file(f,bpp=4)

with open('title.map','rb') as f:
    tm = Tilemap.from_file(f,h=28)
# Temp ----------------------------

def clickMap(event):
    showinfo('Tilemap clicked at', '%i,%i'%(event.x/(32*2),event.y/(32*2)))

def clickSet(event):
    showinfo('Tileset clicked at', '%i,%i'%(event.x/(32*2),event.y/(32*2)))

def ClickPal(event):
    showinfo('Palette clicked at', '%i,%i'%(event.x/(10),event.y/(10)))

def ClickTil(event):
    showinfo('Tile clicked at', '%i,%i'%(event.x/(10),event.y/(10)))

version = "V0.1"

root = Tk()
root.title("Raw Tiler %s" % version)
root.geometry("1280x768")

ABOUT_TEXT = """
Raw Tiler %s by @n_Arno

This very simple editor allow to load/edit and save raw SNES GFX files.
Tileset, Tilemap and palette are loadable and editable separately.

Current limitation: 8x8 tile, 32x32 tilemap, 16 colors palette

This software is distributed under CC BY-NC-SA
""" % version

LIC_ICON='''\
R0lGODlhWAAfAPcAAAEBAX+Bf7vBu5+hnUFBQePj483Ry6uxqyEhIbO5scPJw5GTkWFhYTExMbG3
sbu5ucvLy42Li8PHw9/f33FxcREREdHV0a+1rZ+dnb/FvykpKcnNx3l9eYeHh6Opo7e9t5mXlz87
PYOFg7/Dv1FRUa+zr7W7tcnJyQsLC73Dvf///8/TzzU3Nbm/uXdzdRkZGdfV1S0tLaOnoe/v762z
qyUlJbW7s8fLxZOZk8vPy4+Pj9PX07G3r31/fa2rq5+Xm11fXQ0PDb+/vyMfIYWBg73BvaOhoc3R
zbO5s8XJxW9tbTMzMbW1tcnHx3Vzc9PV06+1r8HFwSkrKcnNyX97fZeZl4WHhbu/ux8bHa2zrSsn
J8/Pz4GBgb3Bu5+jn0NFQ+nn58XJw5GVkWllZzMxMbO3sYmNicXHw+Hf4XFzb9PV0Z+fn8HFv3t9
eY+Hi6erp7m9tz8/P4WFhVtXWbGzr7e7tcfLxw0NDb/DvdHTzz83Obu/uXl1dxsbGzEtL/Hx8Skl
J6+vr2NfYZuZmZWZlQ8PDysrK83Py5GPj8/RzbW5s7G1r8vNya+zrQAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAAAALAAAAABYAB8A
Bwj/AAsBGEiwoMGDCBMqXMiwIUMTdVp0wcNGwg07U3LkOHJEIyM7NxSwwdOlRR1FSBxAuUAjy4GX
MGPKnEmzpk2aBBV9aJFihMUNORKtyGNBjRoLFlYkyrHhhoQMKVp8sFFGJUsaN7Nq3Tpz4E4BURTY
2ZhHxJc7Be98EZFnRQ47SdgU2VPHhAMeUBph5aChoAYON/n6BWxTMMG/OAHA6RJFAtAVC/os7LNg
xaEpSaKkgPNB0d0shPoCiKOEQpyBGnDMFCM6DgXTqFXLFCNlIGnYAFLLHNiFjYINBlaQIFiIARch
QrgAETiQhAQDGxRkKGmiqgy0JCao2K5iwvAgYmJ6/8Gunbt3AODFk+fe/Xt4mANTSLBzKM9wAIW4
zGDPfU0F1M9tIAEeAsChSBl9AcHdQP3lFlNfgnCHyBwNavAgAAqqUEATTRSw3RoOwgdAFEnkINxA
DZTHH3d/+NFcHjnEtZkJPQBAAgwLAsDecIRxAAAZIGyHyAt3OOGhCjy+5OONKgwwxJNDPLBdki8N
5NgRC6C434r8zdDAQAscMcVTAnzQl4pcThBiXzUMEcIYAPTQAQA+bKemhQecqUITQ+ghiBNPItJd
iAcMdEMOeUhWyBZccjmDQH1YkMMNbBQIAAHsATFQhNydViUBTvABpZE4dgrApyr88cMQbmyHwRAx
bP/naZUA2HGECANx0WijIAIgQiICprAHAEqwVxB7FJxaaLF7OkGQE09wl2yVFKSKwBBabFfAk2Co
MC2tU6zwBQAVbCkECXHE0cN256arA3cCfbHCFGeMMGy1OTLInRLKAoCvtk7E8OQcUvJbJbNMxCCE
tk9qZzCtjOSBVoZFGERAIAZlKAgAd8CYRAYCjJbpQBnK2m8cLGKgAgxQujmryCo8YEQT2/nwpMki
HmLBQO+q4OIQEwgxxBouphjI0B8O9MSkbHShZ47sqanFS0/PMYQfLrrgAxVYADB1ngBo9+oQRHCh
xRBBSi1iDjsMtLAKuRob54pCDKTGEZl1EYCNcu//CECPfGvIxQsoIPLHlH8rGTgRLStxOJWFAnCI
Gm5vN9C6OQZA90A7vFUpHAlCvR2/Xx9AgxYYchcBhaN7DdPpqatwgg8+lEp6TAPlsDMAPX85xAxb
DBHAl34AP4SuTdp9CKVdfPDGeuZ9J9tLAwRhI5rnBTH9AdVfH7X0uAPAiAVoMbAdxgUJgj5BGfLb
cQ5hgAwHEh6I1gAQFLjo9XsxDWA//vrTAv9g4j8UAXAgAtwNAMI1nEJwp11xQF4gCEBBzW1nCACQ
1xQUgIcrfAAJPCiBYVBDmJpwAHWHKSFNTjiYxNgqS7zbFZd6ZYUj2EECRWiBCUCoF6748IcKLFGi
//CDJhn+4T+RYloOD7QSGmAFiFDcipWA06sGbEmGM9BfmASEB7qk5AIuiaIYs0KQHoRLUwDwQyJk
OIEv2WgFjMCVQ+ZIxzoWhAKHOBF+9LOiGXCBOSyQVI3sSMhCLqQHukMjfoBwHCH0QBDMsZEFDlEF
hUCNIHBDSCZ1pK+FiG6OiFzBGiSjEMq4hRCeZJAqN3kQy3Eyk6w8liw56RAKBMUCC/iC9QiilgXk
4QiMGKQlXalKS76Slp6EZb4asoQDbGQoatjBUZJigBw04jQMgSUmU6kjuGkzld+kYxwicAVGaMQj
V4gANhuyzFgaZJPKHOY33WnIetrzngVBAT73yQTPhgQEADs=
''' # base64 encoded CC BY-NC-SA gif icon

def about():
    toplevel = Toplevel()
    toplevel.attributes("-toolwindow",1) # Windows only :-/
    toplevel.title("About...")
    Label(toplevel, text=ABOUT_TEXT, height=0, width=100).grid(row=0,columnspan=2)
    licImg = PhotoImage(data=LIC_ICON)
    lab = Label(toplevel, image=licImg)
    lab.image = licImg # needed to avoid garbage collection
    lab.grid(row=1, column=0)
    Button(toplevel, text="OK", width=15, command=toplevel.destroy).grid(row=1, column=1)
    toplevel.focus_force()

def default_cmd():
    pass

def loadPal():
    ftypes = [('Palette Files', '*.pal'), ('All files', '*')]
    dlg = tkFileDialog.Open(root, filetypes = ftypes)
    fl = dlg.show()

    if fl != '':
        with open(fl,'rb') as f:
            pass

menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open All", command=default_cmd)
filemenu.add_command(label="Save All", command=default_cmd)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

mapmenu = Menu(menubar, tearoff=0)
mapmenu.add_command(label="Load", command=default_cmd)
mapmenu.add_command(label="Save", command=default_cmd)
mapmenu.add_command(label="Save As", command=default_cmd)
mapmenu.add_separator()
mapmenu.add_command(label="Toggle Grid", command=default_cmd)
menubar.add_cascade(label="Tilemap", menu=mapmenu)

setmenu = Menu(menubar, tearoff=0)
setmenu.add_command(label="Load", command=default_cmd)
setmenu.add_command(label="Save", command=default_cmd)
setmenu.add_command(label="Save As", command=default_cmd)
setmenu.add_separator()
setmenu.add_command(label="Toggle Grid", command=default_cmd)
menubar.add_cascade(label="Tileset", menu=setmenu)

palmenu = Menu(menubar, tearoff=0)
palmenu.add_command(label="Load", command=loadPal)
palmenu.add_command(label="Save", command=default_cmd)
palmenu.add_command(label="Save As", command=default_cmd)
palmenu.add_separator()
palmenu.add_command(label="Toggle Grid", command=default_cmd)
menubar.add_cascade(label="Palette", menu=palmenu)

menubar.add_command(label="About", command=about)

# display the menu
root.config(menu=menubar)

# Tilemap
lblMap = LabelFrame(root, text="Tilemap", padx=5, pady=5)
lblMap.grid(row=0,column=0)
cnvMap = Canvas(lblMap, bd=0, width=32*8*2, height=32*8*2)
cnvMap.grid(row=0,column=0)
imgMap = PhotoImage(width=32*8, height=32*8)
imgMap.put(tm.renderImg(ts,ps))
imgMap = imgMap.zoom(2,2)
cnvMap.create_image(0,0,image=imgMap,anchor="nw")
cnvMap.bind("<Button-1>", clickMap)

# Tileset
lblSet = LabelFrame(root, text="Tileset", padx=5, pady=5)
lblSet.grid(row=0,column=1)
cnvSet = Canvas(lblSet, bd=0, width=32*8*2, height=32*8*2)
cnvSet.grid(row=0,column=0)
imgSet = PhotoImage(width=32*8, height=32*8)
imgSet.put(ts.renderImg(ps[0]))
imgSet = imgSet.zoom(2,2)
cnvSet.create_image(0,0,image=imgSet,anchor="nw")
cnvSet.bind("<Button-1>", clickSet)

# Palettes
lblPal = LabelFrame(root, text="Palettes", padx=5, pady=5)
lblPal.grid(row=1,column=0)
cnvPal = Canvas(lblPal, bd=0, width=16*10, height=4*10)
cnvPal.grid(row=0,column=0)
imgPal = PhotoImage(width=16, height=4)
imgPal.put(ps.renderImg())
imgPal = imgPal.zoom(10,10)
cnvPal.create_image(0,0,image=imgPal,anchor="nw")
cnvPal.bind("<Button-1>", ClickPal)

# Tile
lblTil = LabelFrame(root, text="Tile", padx=5, pady=5)
lblTil.grid(row=1,column=1)
cnvTil = Canvas(lblTil, bd=0, width=8*10, height=8*10)
cnvTil.grid(row=0,column=0)
imgTil = PhotoImage(width=8, height=8)
imgTil.put(ts[0].renderImg(ps[0]))
imgTil = imgTil.zoom(10,10)
cnvTil.create_image(0,0,image=imgTil,anchor="nw")
cnvTil.bind("<Button-1>", ClickTil)

root.mainloop()