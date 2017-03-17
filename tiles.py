from palette import Palette, Color

class Tile(object):
    def __init__(self, bpp=2):
        self.current = 0
        if not (bpp == 2 or bpp ==4):
            raise ValueError("Tile can only be in 2bpp (4 colors) or 4bpp (16 colors) mode. %ibpp is invalid" % bpp)
        self._mode = bpp
        self._tiledata = [[0] * 8 for i in range(8)]

    def display(self):
        return '\n'.join([''.join(map(str,line)) for line in self._tiledata])
        
    def set_color(self,x,y,c):
        if (self._mode == 0 and c>3):
            raise ValueError("Tile is in 4 colors mode, %i is an invalid color index" % c)
        if (c>15):
            raise ValueError("Tile is in 16 colors mode, %i is and invalid color index" % c)
        if (x<0 or x>7 or y<0 or y>7):
            raise ValueError("Tile is %ix%i in size, (%i,%i) is out of range" % (self._size,self._size,x,y))
        self._tiledata[y][x] = c

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