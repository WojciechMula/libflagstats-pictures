main.pdf: main.tex flags-carry.tex flags-select.tex
	pdflatex main.tex

flags-carry.tex: flags-carry.tikz.py flagstats.py
	python3 flags-carry.tikz.py flags-carry.tex

flags-select.tex: flags-select.tikz.py flagstats.py
	python3 flags-select.tikz.py flags-select.tex
