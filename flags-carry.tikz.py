import sys
import itertools

from io import StringIO
from flagstats import *


def draw_flags(file):
    flags = FLAGS(0.5, 0, 0)

    for index in range(0, 12):
        flags[index].style = 'fill=white'

    for flag in [FMUNMAP, FUNMAP, FPROPER_PAIR, FPAIRED]:
        flags[flag].style = 'fill=green!25'

    # draw the bits
    flags.draw(file)

    # mark the bits that are propagated
    x1 = flags[FMUNMAP].xleft
    for index, flag in enumerate([FMUNMAP, FUNMAP, FPROPER_PAIR, FPAIRED]):
        bit = flags[flag]
        y1 = bit.top.y + 0.5 + 0.4 * index
        draw_description(file, bit.top.x, bit.top.y, x1, y1, texttt(flag.label), 'left')

    # mark spare bits
    draw_horiz_brace(file, flags[15].xleft, flags[12].xright, flags[0].ytop, "unused")

    # label expression
    expressions = {
        12: r"\footnotesize{\texttt{%s and %s and not %s}}" % (FPAIRED, FPROPER_PAIR, FUNMAP),
        13: r"\footnotesize{\texttt{%s and %s and not %s}}" % (FPAIRED, FMUNMAP, FUNMAP),
        14: r"\footnotesize{\texttt{%s and not %s and not %s}}" % (FPAIRED, FMUNMAP, FUNMAP),
    }

    for index, (bit, expression) in enumerate(expressions.items()):
        x1 = flags[12].xright
        y1 = flags[bit].ybottom - (0.7 + 0.4 * index)
        draw_description(file, flags[bit].bottom.x, flags[bit].bottom.y, x1, y1, expression, 'right')

    # label a few bits
    for bit in itertools.chain(range(0, 12), [15]):
        flags[bit].draw_index(file)


if __name__ == '__main__':
    buf = StringIO()
    buf.write(r"\begin{tikzpicture}")
    draw_flags(File(buf))
    buf.write(r"\end{tikzpicture}")

    with open(sys.argv[1], 'wt') as f:
        f.write(buf.getvalue())
