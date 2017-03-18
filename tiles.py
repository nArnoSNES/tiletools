from palette import Palette, Color

class Tile(object):
    def __init__(self, bpp=2):
        self.current = 0
        if not (bpp == 2 or bpp ==4):
            raise ValueError("Tile can only be in 2bpp (4 colors) or 4bpp (16 colors) mode. %ibpp is invalid" % bpp)
        self._mode = bpp
        self._tiledata = [[0] * 8 for i in range(8)]

    def display(self):
        return '\n'.join([' '.join(map(str,line)) for line in self._tiledata])
        
    def set_color(self,x,y,c):
        if (self._mode == 0 and c>3):
            raise ValueError("Tile is in 4 colors mode, %i is an invalid color index" % c)
        if (c>15):
            raise ValueError("Tile is in 16 colors mode, %i is and invalid color index" % c)
        if (x<0 or x>7 or y<0 or y>7):
            raise ValueError("Tile is %ix%i in size, (%i,%i) is out of range" % (8,8,x,y))
        self._tiledata[y][x] = c

    def __eq__(self,other):
        return (str(self) == str(other))

    def __getitem__(self, i):
        return self._tiledata[i]

    def __setitem__(self, i, l):
        self._tiledata[i] = l

    def __len__(self):
        return 8

    def __iter__(self):
        return self

    def next(self):
        try:
            result = self._tiledata[self.current]
        except IndexError:
            self.current = 0
            raise StopIteration
        self.current += 1
        return result

    def __str__(self):
        result=[]
        fstr='{0:0%ib}' % self._mode
        for line in self._tiledata:
            temp=['']*self._mode
            for c in line:
                    _bin = fstr.format(c)[::-1]
                    for i in range(self._mode):
                            temp[i] = temp[i] + _bin[i]
            result.extend(temp)
        result = map(chr,map(lambda x: int(x,2),result))
        return ''.join(result)

    def renderImg(self, palette, index=0):
        if (self._mode != 2 and index != 0):
            raise ValueError("Tile is not 2bpp, palette index MUST be 0 (default)")
        if not index in [0,4,8,12]:
            raise ValueError("index value of %i is invalid" % index)
        im = []
        for line in self._tiledata:
            im.append('{ ' + ' '.join(map(lambda c: "#%s" % palette[index+c].to_hex(),line)) + ' }')
        return ' '.join(im)

    def renderTile(self, palette, index=0):
        if (self._mode != 2 and index != 0):
            raise ValueError("Tile is not 2bpp, palette index MUST be 0 (default)")
        if not index in [0,4,8,12]:
            raise ValueError("index value of %i is invalid" % index)
        tile = []
        for line in self._tiledata:
            tile.append(map(lambda c: "#%s" % palette[index+c].to_hex(),line))
        return tile

    @staticmethod
    def from_str(s, bpp=2):
        _t = Tile(bpp)
        data = []
        if (len(s) != bpp*8):
            raise ValueError("String is not of valid length %i for %ibpp mode" % (8*bpp,bpp))
        for line in map(''.join,zip(*[iter(s)]*bpp)):
            bytes = map(lambda x: '{0:08b}'.format(x),map(ord,line))
            temp = [0] * 8
            for pixel in range(8):
                for plane in range(bpp):
                    temp[pixel] += int(bytes[plane][pixel])*(2**plane)
            data.append(temp)
        _t._tiledata = data
        return _t

class Tileset(object):
    def __init__(self,bpp=2):
        if not (bpp == 2 or bpp ==4):
            raise ValueError("Tileset can only contains tiles in 2bpp (4 colors) or 4bpp (16 colors) mode. %ibpp is invalid" % bpp)
        self._mode = bpp
        self.current = 0
        self.tiles = []
    
    def next(self):
        try:
            result = self.tiles[self.current]
        except IndexError:
            self.current = 0
            raise StopIteration
        self.current += 1
        return result
        
    def __iter__(self):
        return self

    def __getitem__(self, i):
        return self.tiles[i]

    def __setitem__(self, i, t):
        if (t._mode != self._mode):
            raise ValueError("Can't add a tile of %ibpp in tileset of %ibpp" % (t._mode,self._mode))
        self.tiles[i] = t

    def __len__(self):
        return len(self.tiles)

    def __eq__(self,other):
        if len(self) != len(other):
            return False
        result = True
        for i in range(len(self)):
            result = (result and self.tiles[i] == other.tiles[i])
        return result

    def append(self,t):
        if (len(self) == 1024):
            raise IndexError("The tileset can only contains 1024 tiles max (32x32)")
        if (t._mode != self._mode):
            raise ValueError("Can't add a tile of %ibpp in tileset of %ibpp" % (t._mode,self._mode))
        self.current = 0
        self.tiles.append(t)
        
    def __str__(self):
        result = []
        for t in self.tiles:
            result.append(str(t))
        return ''.join(result)

class TileVal(object):
    def __init__(self,v=0,h=0,o=0,p=0,t):
        if v not in [0,1]:
            raise ValueError("Vertical flip is either 0 or 1")
        if h not in [0,1]:
            raise ValueError("Horizontal flip is either 0 or 1")
        if o not in [0,1]:
            raise ValueError("Priority bit is either 0 or 1")
        if (p<0 or p>3):
            raise ValueError("Palette number is between 0 and 3")
        if (t<0 or t>1023):
            raise ValueError("Tile number is between 0 and 1023")
        self.vflip = v
        self.hflip = h
        self.order = o
        self.palnum = p
        self.tilenum = t

    def __str__(self):
        _bits = str(v) + str(h) + str(o) + '{0:03b}'.format(p) + '{0:010b}'.format(t)
        _s = [ int(_bits[0:8],2) , int(_bits[8:16],2) ]
        return ''.join(map(chr,_s))

    def renderTile(self,tileset,palettes):
        tile = tileset[self.tilenum].renderTile(palettes[self.palnum])
        if (v==1):
            tile = map(lambda x: x[::-1], tile)
        if (p==1):
            tile = tile[::-1]
        return tile

class Tilemap(object):
    def __init__(self,h=32,w=32):
        self.width = w
        self.height = h
        self.tilevals = [ [Tileval(0)] * w for i in range(h) ]

    def set_tile(self,x,y,t):
        if (x<0 or x>=self.width or y<0 or y>=self.height):
            raise ValueError("Tilemap is %ix%i in size, (%i,%i) is out of range" % (self.width,self.height,x,y))
        self.tilevals[y][x] = t

    def __str__(self):
        return ''.join(map(lambda line: ''.join(map(str,line)),self.tilevals))

    def renderImg(self,tileset,palettes):
        temp = map(lambda line: map(lambda x: x.renderTile(tileset,palettes),line),self.tilevals)
        result = [[''] * self.width*8 for i in range(self.height*8)]
        i = 0
        for tile in temp:
            column=i%self.height
            row=int(i/self.width)
            for j in range(8):
                for k in range(8):
                    result[row*8+j][column*8+k] = tile[j][k]
            i = i + 1
        return ' '.join(map(lambda line: '{ ' + ' '.join(line) + ' }',temp))
        