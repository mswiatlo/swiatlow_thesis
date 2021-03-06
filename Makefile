export TEXINPUTS := .//:./style//:sections//:${TEXINPUTS}
export BIBINPUTS := .//:./bibs//:${TEXINPUTS}

THESIS = swiatlow_thesis

all:
	pdflatex ${THESIS}
	pdflatex ${THESIS}
	bibtex   ${THESIS}
	pdflatex ${THESIS}
	pdflatex ${THESIS}
	# clear
	# du -hs
	# ls -ltrh
	open -a skim ${THESIS}.pdf
	sh scripts/pages.sh

clean:
	rm -f *.aux *.log *.pdf *.bbl *.blg *.brf *.cb *.ind *.idx *.ilg  *.bbl \
	 	*.inx *.dvi *.toc *.out *~ ~* spellTmp 
