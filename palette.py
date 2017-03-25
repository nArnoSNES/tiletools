class Color(object):
    def __init__(self, c=0):
        if not (c>=0 and c<32768):
            raise ValueError('Color arg %i not in range(32768)' % c)
        self._color = c

    def __eq__(self,other):
        return (self._color == other._color)

    def __str__(self):
        _high = int('FF00',16)
        _low = int('00FF',16)
        _c = [ (self._color & _high)>>8,(self._color & _low) ]
        return ''.join(map(chr,_c))

    def _blue_bin(self):
        return '{0:016b}'.format(self._color)[1:6]

    def blue(self):
        return int(self._blue_bin(),2)

    def blue255(self):
        return self.blue()<<3

    def _green_bin(self):
        return '{0:016b}'.format(self._color)[6:11]

    def green(self):
        return int(self._green_bin(),2)

    def green255(self):
        return self.green()<<3

    def _red_bin(self):
        return '{0:016b}'.format(self._color)[11:16]

    def red(self):
        return int(self._red_bin(),2)

    def red255(self):
        return self.red()<<3

    def to_hex(self):
        return "%02x%02x%02x" % (self.red255(),self.green255(),self.blue255())

    def renderImg(self):
        return '{#%s}' % self.to_hex()

    @staticmethod
    def from_rgb(red=0,green=0,blue=0):
        if not (red>=0 and red<256):
            raise ValueError('red arg %i not in range(256)' % red)
        if not (green>=0 and green<256):
            raise ValueError('green arg %i not in range(256)' % green)
        if not (blue>=0 and blue<256):
            raise ValueError('blue arg %i not in range(256)' % blue)
        _r = '{0:05b}'.format(red>>3)
        _g = '{0:05b}'.format(green>>3)
        _b = '{0:05b}'.format(blue>>3)
        _n = Color(int(_b+_g+_r,2)) 
        return _n

    @staticmethod
    def from_hex(hexstr):
        if not (len(hexstr) == 6):
            raise ValueError('string %s is not a 6 char long' % hexstr)
        _rgb = ()
        try:
            _rgb = tuple(map(lambda x:int(''.join(x),16),zip(*[iter(hexstr)]*2)))
        except:
            raise ValueError('string %s is not a valid hex string' % hexstr)
        _n = Color.from_rgb(*_rgb)
        return _n

    @staticmethod
    def from_str(s):
        if not (len(s) == 2):
            raise ValueError('string %s is not a 2 char long' % s)
        return Color(ord(s[0])*256+ord(s[1]))

class Palette(object):
    def __init__(self):
        self.palette = [Color(0)]*16
        self.current = 0

    def __iter__(self):
        return self
        
    def __eq__(self,other):
        return (str(self) == str(other))

    def __getitem__(self, i):
        return self.palette[i]

    def __setitem__(self, i, c):
        self.palette[i] = c

    def __len__(self):
        return 16

    def __str__(self):
        return ''.join(map(str,self.palette))

    def next(self):
        try:
            result = self.palette[self.current]
        except IndexError:
            self.current = 0
            raise StopIteration
        self.current += 1
        return result

    def to_file(self,f):
        for c in self.palette:
            f.write(str(c)[::-1])
        return

    @staticmethod
    def from_file(f):
        _p = Palette()
        for i in range(16):
            c = f.read(2)
            _p.palette[i] = Color.from_str(c[::-1])
        return _p

class Palettes(object):
    def __init__(self):
        self.current = 0
        self.palettes = [ Palette() for i in range(4) ]
    
    def next(self):
        try:
            result = self.palettes[self.current]
        except IndexError:
            self.current = 0
            raise StopIteration
        self.current += 1
        return result
        
    def __iter__(self):
        return self

    def __getitem__(self, i):
        return self.palettes[i]

    def __setitem__(self, i, p):
        self.palettes[i] = p

    def __len__(self):
        return 4

    def __eq__(self,other):
        result = True
        for i in range(4):
            result = (result and self.palettes[i] == other.palettes[i])
        return result

    def renderImg(self):
        im = []
        for p in self.palettes:
            im.append('{ ' + ' '.join(map(lambda c: "#%s" % c.to_hex(),p))  + ' }')
        return ' '.join(im)

    @staticmethod
    def from_file(f):
        _ps = Palettes()
        for i in range(4):
            _ps[i] = Palette.from_file(f)
        return _ps