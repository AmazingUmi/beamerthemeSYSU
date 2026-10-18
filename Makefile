.PHONY: all clean

all:
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
	mkdir -p output/pdf
	cp build/main.pdf output/pdf/SYSU-template.pdf

clean:
	latexmk -C -outdir=build main.tex
	rm -f output/pdf/SYSU-template.pdf
