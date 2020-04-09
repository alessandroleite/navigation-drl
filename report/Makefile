TEX_NAME=report.tex
default: build_and_clean

build:
	pdflatex ${TEX_NAME}
	-bibtex  ${TEX_NAME}
	pdflatex ${TEX_NAME}
	makeglossaries ${TEX_NAME}
	pdflatex ${TEX_NAME}

clean_pwd:
	rm -f *.acn *.alg *.aux *.bbl *.blg *.brf *.fls *.glsdefs *.glo *.ilg *.ind *.ist *.lof *.log *.lol *.lot *.maf *.mtc* *.out *.spl *.synctex.* *.toc *.upa *.upb *.xwm 2> /dev/null
	@find . -name "*.fdb_latexmk" -exec rm -rf {} \;

clean:
	make clean_pwd	

build_and_clean:
	make build
	make clean
