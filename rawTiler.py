# ------------------------------------
#	Raw Tiler by n_Arno
#	Very simple raw SNES GFX editor.
#	Quick and Ugly dev: not efficient.
# ------------------------------------

import sys
from Tkinter import *
import tkFileDialog
from palette import Palette,Color

version = "V0.1"

gridSize = 32
tileSize = 8
setZoom = 1
mapZoom = 1
palZoom = 20
tilZoom = 8
ncolors = 16
gridColor = (255,0,255)
tilGrid = True

def hexCode(p):
	return "#%02x%02x%02x" % p

def palToTile(p, tilesize=tileSize):
	return [[p] * tilesize for i in range(tilesize)]

def modulo16(p, colors=ncolors):
	return p % colors

# Default Palette: DawnBringer 16 colors palette V1.0 (http://www.pixeljoint.com/forum/forum_posts.asp?TID=12795) 
palette = [(20,12,28),
		(68,36,52),
		(48,52,109),
		(78,74,78),
		(133,76,48),
		(52,101,36),
		(208,70,72),
		(117,113,97),
		(89,125,206),
		(210,125,44),
		(133,149,161),
		(109,170,44),
		(210,170,153),
		(109,194,202),
		(218,212,94),
		(222,238,214)]
palette.extend([gridColor]) # grid color is added to palette, will be accessed by [-1] index
palette = map(hexCode,palette)

tileset = range(gridSize*gridSize)
tileset = map(modulo16,tileset)
tileset = map(palToTile,tileset)

tilemap = [0,1,2]*(int(gridSize*gridSize/3))
tilemap.extend([0]*((gridSize*gridSize)%3))

tilenum = 0

root = Tk()
root.title("Raw Tiler %s" % version)
root.geometry("565x410")

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
			p = Palette.from_file(f)
		p = map(lambda x: (x.red255(),x.blue255(),x.green255()),p)
		p.extend([gridColor]) # grid color is added to palette, will be accessed by [-1] index
		palette = map(hexCode,p)
		renderPalette(palImg, palette)
		renderTileset(setImg, tileset, palette, grid=False)
		renderTilemap(mapImg, tileset, tilemap, palette, grid=False)
		renderTile(tilImg, tileset[tilenum], palette)

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



def fillTileSet(tileset, gridsize=gridSize):
	result = tileset
	result.extend([0 for i in range(len(tileset) - gridsize*gridsize)])
	return result

def convertTileData(tiledata, gridsize=gridSize, tilesize=tileSize):
	result = [[0] * gridsize*tilesize for i in range(gridsize*tilesize)]
	i = 0
	for tile in tiledata:
		column=i%gridsize
		row=int(i/gridsize)
		for j in range(tilesize):
			for k in range(tilesize):
				result[row*tilesize+j][column*tilesize+k] = tile[j][k]
		i = i + 1
	return result

def renderTile(image, tile, palette, size=tilZoom, grid=tilGrid):
	sepPoint = ""
	setLine = " "
	im = []
	for line in tile:
		hl = []
		for pixel in line:
			hexcode = palette[pixel]
			hl.append(" ".join([hexcode]*size))
			if grid:
				hl.append(palette[-1])
		if grid:
			hl.append(" ".join([palette[-1]]*size))
		im.append(" ".join(["{" + " ".join(hl) + "}"]*size))
	image.put(" ".join(im))

def renderTilemap(image, tileset, tilemap, palette, size=mapZoom, grid=False):
	tileData = []
	for tile in tilemap:
		tileData.append(tileset[tile])
	tempTile = convertTileData(tileData)
	renderTile(image, tempTile, palette, size=size, grid=grid)

def renderTileset(image, tileset, palette, size=setZoom, grid=False):
	tileData = fillTileSet(tileset)
	tempTile = convertTileData(tileData)
	renderTile(image, tempTile, palette, size=size, grid=grid)

def renderPalette(image, palette, size=palZoom, grid=False):
	width = size
	height = size
	im = []
	for i in range(2):
		hl = []
		for j in range(8):
			hexcode = palette[i*8+j]
			hl.append(" ".join([hexcode]*width))
		im.append(" ".join(["{" + " ".join(hl) + "}"]*height))
	image.put(" ".join(im))

mapFrm = Frame(root,relief=GROOVE, borderwidth=2)
mapFrm.grid(row=0, column=0, padx=5, pady=5)
Label(mapFrm, text="Tilemap", state=DISABLED).grid(sticky=W)
mapImg = PhotoImage(width=gridSize*tileSize*mapZoom, height=gridSize*tileSize*mapZoom)
renderTilemap(mapImg, tileset, tilemap, palette, grid=False)
tilLbl = Label(mapFrm, image=mapImg, borderwidth=0)
tilLbl.grid(sticky=N, padx=5, pady=5)

setFrm = Frame(root,relief=GROOVE, borderwidth=2)
setFrm.grid(row=0, column=1, padx=5, pady=5)
Label(setFrm, text="Tileset", state=DISABLED).grid(sticky=W)
setImg = PhotoImage(width=gridSize*tileSize*setZoom, height=gridSize*tileSize*setZoom)
renderTileset(setImg, tileset, palette, grid=False)
setLbl = Label(setFrm, image=setImg, borderwidth=0)
setLbl.grid(padx=5, pady=5)

palFrm = Frame(root,relief=GROOVE, borderwidth=2)
palFrm.grid(row=1, column=0, padx=5, pady=5)
Label(palFrm, text="Palette", state=DISABLED).grid(sticky=W)
palImg = PhotoImage(width=palZoom*8, height=palZoom*2)
renderPalette(palImg, palette)
palLbl = Label(palFrm, image=palImg, borderwidth=0)
palLbl.grid(sticky=NW, padx=5, pady=5)

tilFrm = Frame(root,relief=GROOVE, borderwidth=2)
tilFrm.grid(row=1, column=1, padx=5, pady=5)
Label(tilFrm, text="Selected Tile", state=DISABLED).grid(sticky=W)
tilImg = PhotoImage(width=tileSize*tilZoom+tilGrid*tileSize, height=tileSize*tilZoom+tilGrid*tileSize)
renderTile(tilImg, tileset[tilenum], palette)
tilLbl = Label(tilFrm, image=tilImg, borderwidth=0)
tilLbl.grid(padx=5, pady=5, sticky=W)

root.mainloop()