export TEXINPUTS := .//:./style//:sections//:${TEXINPUTS}
export BIBINPUTS := .//:./bibs//:${TEXINPUTS}

THESIS = swiatlow_thesis

all:
	pdflatex ${THESIS}
	# bibtex   ${THESIS}
	# pdflatex ${THESIS}
	# pdflatex ${THESIS}
	# clear
	# du -hs
	# ls -ltrh
	open -a skim ${THESIS}.pdf
	sh scripts/pages.sh
	git status

