main.pdf: main.tex flags-carry.tex flags-select.tex flags-select-nolabels.tex
	pdflatex main.tex

flags-carry.tex: flags-carry.tikz.py flagstats.py
	python3 flags-carry.tikz.py flags-carry.tex

flags-select.tex: flags-select.tikz.py flagstats.py
	python3 flags-select.tikz.py flags-select.tex 1

flags-select-nolabels.tex: flags-select.tikz.py flagstats.py
	python3 flags-select.tikz.py flags-select-nolabels.tex 0
