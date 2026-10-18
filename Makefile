.PHONY: all clean

all:
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
	mkdir -p examples
	cp build/main.pdf examples/SYSU-template.pdf

clean:
	latexmk -C -outdir=build main.tex
