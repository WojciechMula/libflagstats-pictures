import sys
from itertools import chain

from io import StringIO
from flagstats import *

ALWAYS_UPDATED = [FQCFAIL, FUNMAP, FDUP]

SEL = 'fill=blue!50'
UPD = 'fill=green!50'
ACTIVE = 'fill=white'
INACTIVE = 'fill=lightgray'

def draw_bit_labels(file, flags, marks):
    for item in marks:
        try:
            stackpos, flag, align, style, label = item
        except ValueError:
            stackpos, flag, align, style = item
            label = texttt(flag)

        bit = flags[flag]
        bit.style = style
        if align == 'left':
            x1 = bit.xleft
        else:
            x1 = bit.xright

        y1 = bit.ytop + 0.4 + 0.4 * stackpos

        draw_description(file, bit.top.x, bit.top.y, x1, y1, label, align)
    

def draw_select(file, y):
    flags = FLAGS(0.5, 0, y)

    for index in range(0, 16):
        flags[index].style = ACTIVE
        flags[index].draw_index(file)

    # mark the bits that are used to select a mask
    marks = (
        (2, FPAIRED,           'left', SEL),
        (1, FUNMAP,            'left', UPD),
        (0, FSECONDARY,        'right', SEL),
        (1, FQCFAIL,           'right', UPD),
        (2, FDUP,              'right', UPD),
        (3, FSUPPLEMENTARY,    'right', SEL),
    )
    draw_bit_labels(file, flags, marks)

    flags.draw(file)


def draw_mask1(file, y, with_marks):

    flags = FLAGS(0.5, 0.0, y)

    for index in range(0, 16):
        flags[index].style = INACTIVE
        flags[index].label = '0'
        flags[index].draw_index(file)

    for flag in chain(ALWAYS_UPDATED, [FSECONDARY]):
        flags[flag].style = ACTIVE
        flags[flag].label = '1'


    marks = (
        (0, FSECONDARY, 'right', SEL, texttt('%s=1' % FSECONDARY)),
    )
    if with_marks:
        draw_bit_labels(file, flags, marks)

    flags.draw(file)


def draw_mask2(file, y, with_marks):

    flags = FLAGS(0.5, 0.0, y)

    for index in range(0, 16):
        flags[index].style = INACTIVE
        flags[index].label = '0'
        flags[index].draw_index(file)

    for flag in chain(ALWAYS_UPDATED, [FSUPPLEMENTARY]):
        flags[flag].style = ACTIVE
        flags[flag].label = '1'

    marks = (
        (0, FSECONDARY, 'right', ACTIVE, texttt('%s=0' % FSECONDARY)),
        (1, FSUPPLEMENTARY, 'right', SEL, texttt('%s=1' % FSUPPLEMENTARY)),
    )
    if with_marks:
        draw_bit_labels(file, flags, marks)

    flags.draw(file)


def draw_mask3(file, y, with_marks):

    flags = FLAGS(0.5, 0.0, y)

    for index in range(0, 16):
        flags[index].style = INACTIVE
        flags[index].label = '0'
        flags[index].draw_index(file)

    for flag in chain(ALWAYS_UPDATED, [FPAIRED, FREAD1, FREAD2, BIT12, BIT13, BIT14]):
        flags[flag].style = ACTIVE
        flags[flag].label = '1'

    marks = (
        (0, FSECONDARY,     'right', ACTIVE, texttt('%s=0' % FSECONDARY)),
        (1, FSUPPLEMENTARY, 'right', ACTIVE, texttt('%s=0' % FSUPPLEMENTARY)),
        (1, FPAIRED,        'left',  SEL, texttt('%s=1' % FPAIRED)),
    )
    if with_marks:
        draw_bit_labels(file, flags, marks)

    flags.draw(file)


if __name__ == '__main__':
    buf = StringIO()
    f = File(buf)
    f.writeln(r"\begin{tikzpicture}")
    try:
        with_marks = int(sys.argv[2])
    except IndexError:
        with_marks = False

    draw_select(f, 0.0)
    if with_marks:
        draw_mask1(f, -1.5, True)
        draw_mask2(f, -3.5, True)
        draw_mask3(f, -6.0, True)
    else:
        draw_mask1(f, -1.0, False)
        draw_mask2(f, -2.0, False)
        draw_mask3(f, -3.0, False)

    f.writeln(r"\end{tikzpicture}")

    with open(sys.argv[1], 'wt') as f:
        f.write(buf.getvalue())
