main.pdf: main.tex flags-carry.tex
	pdflatex main.tex

flags-carry.tex: flags-carry.tikz.py
	python3 $^ $@
