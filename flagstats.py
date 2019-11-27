# constants

class Flag:
    def __init__(self, index, label):
        self.index = index
        self.label = label


    def __str__(self):
        return escape(self.label)


FPAIRED        = Flag(0, 'FPAIRED')
FPROPER_PAIR   = Flag(1, 'FPROPER_PAIR')
FUNMAP         = Flag(2, 'FUNMAP')
FMUNMAP        = Flag(3, 'FMUNMAP')
FREVERSE       = Flag(4, 'FREVERSE')
FMREVERSE      = Flag(5, 'FMREVERSE')
FREAD1         = Flag(6, 'FREAD1')
FREAD2         = Flag(7, 'FREAD2')
FSECONDARY     = Flag(8, 'FSECONDARY')
FQCFAIL        = Flag(9, 'FQCFAIL')
FDUP           = Flag(10, 'FDUP')
FSUPPLEMENTARY = Flag(11, 'FSUPPLEMENTARY')
BIT12          = Flag(12, 'BIT12')
BIT13          = Flag(13, 'BIT13')
BIT14          = Flag(14, 'BIT14')


# model of flags word


class FLAGS:
    def __init__(self, size, dx, dy):
        self.dx = dx
        self.dy = dy
        self.size = 0.5
        self.default_style = 'fill=lightgray'
        self.bits = list(self.__build())


    def __build(self):
        x = self.dx
        y = self.dy
        for index in range(16):
            label = ''
            style = self.default_style
            x = (15 - index) * self.size

            yield BIT(x, y, self.size, label, style, index)


    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.bits[idx]
        else:
            return self.bits[idx.index]


    def __iter__(self):
        return iter(self.bits)


    def draw(self, file):
        for bit in iter(self):
            bit.draw(file)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BIT:
    def __init__(self, x, y, size, label, style, index):
        self.x = x
        self.y = y
        self.size = size
        self.label = label
        self.style = style
        self.index = index


    def draw(self, file):
        x = self.x
        y = self.y
        w = self.size
        h = self.size

        file.writeln(r'\draw [%s] (%0.2f, %0.2f) rectangle (%0.2f, %0.2f);' %
                    (self.style, x, y, x + w, y + h))

        if self.label:
            file.writeln(r'\node at (%0.2f, %0.2f) {%s};' % (x + w/2, y + h/2, self.label))


    def draw_index(self, file):
        file.writeln(r'\node[below] at (%0.2f, %0.2f) {%s};' %
                     (self.bottom.x, self.bottom.y, f"\\tiny{self.index}"))


    @property
    def top(self):
        return Point(self.x + self.size/2, self.ytop)

    @property
    def bottom(self):
        return Point(self.x + self.size/2, self.ybottom)

    @property
    def xleft(self):
        return self.x

    @property
    def xright(self):
        return self.x + self.size

    @property
    def ytop(self):
        return self.y + self.size

    @property
    def ybottom(self):
        return self.y


# drawing utilities

def escape(s):
    return s.replace('_', r'\_')


def texttt(s):
    return r'\texttt{%s}' % s


def bold(s):
    return r'\textbf{%s}' % s


def draw_description(file, x0, y0, x1, y1, label, anchor):
    file.writeln(r'\draw (%0.2f, %0.2f) -- (%0.2f, %0.2f) -- (%0.2f, %0.2f);' %
        (x0, y0, x0, y1, x1, y1)
    )

    file.writeln(r'\node[%s] at (%0.2f, %0.2f) {%s};' % (anchor, x1, y1, label))


def draw_horiz_brace(file, x0, x1, y, label):
    file.writeln(r"\draw [decorate,decoration={brace,amplitude=10pt}] "
                 r"(%0.2f, %0.2f) -- (%0.2f, %0.2f) node [midway,above,yshift=10pt] {%s};" %
                 (x0, y, x1, y, label))


class File:
    def __init__(self, file):
        self.file = file

    def writeln(self, s):
        self.file.write(s)
        self.file.write('\n')
