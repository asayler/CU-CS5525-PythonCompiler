# CU CS5525
# Fall 2012
# Python Compiler
#
# Makefile
# Makefile to build LaTeX reports
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andy Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/

PAPER_INCLUDES :=

INCLUDE_DIR    := include

BIBTEX     ?= bibtex -terse
LATEX      ?= pdflatex -file-line-error
LATEXFIRST ?= -interaction=batchmode
LATEXLAST  ?= -halt-on-error
INKSCAPE   ?= inkscape
CONVERT    ?= convert
CP	   ?= cp

VPATH = $(INCLUDE_DIR)/svg:$(INCLUDE_DIR)/pdf:$(INCLUDE_DIR)/png

.PHONY: all clean cleanall

all: proposal.pdf report.pdf clean

clean:
	$(RM) *.aux *.bbl *.blg *.dvi *.log *.out *.nav *.snm *.toc *.vrb *~
	$(RM) $(INCLUDE_DIR)/*.pdf

cleanall: clean
	$(RM) proposal.pdf report.pdf

.PHONY: proposal report

proposal: proposal.pdf clean

report: report.pdf clean

proposal.pdf: proposal.aux proposal.bbl
	$(LATEX) $(LATEXFIRST) proposal.tex
	$(LATEX) $(LATEXLAST) proposal.tex
	@touch $^ $@

report.pdf: report.aux report.bbl
	$(LATEX) $(LATEXFIRST) report.tex
	$(LATEX) $(LATEXLAST) report.tex
	@touch $^ $@

proposal.bbl: proposal.aux refs.bib
	$(BIBTEX) proposal.aux

report.bbl: report.aux refs.bib
	$(BIBTEX) report.aux

proposal.aux: proposal.tex $(PROPOSAL_INCLUDES)
	$(LATEX) $(LATEXFIRST) proposal.tex

report.aux: report.tex $(PAPER_INCLUDES)
	$(LATEX) $(LATEXFIRST) report.tex

%.pdf:%-src.svg
	$(INKSCAPE) $< -D --export-pdf=$(INCLUDE_DIR)/$@

%.pdf:%-src.pdf
	$(CP) $< $(INCLUDE_DIR)/$@

%.pdf:%-src.png
	$(CONVERT) $< $(INCLUDE_DIR)/$@
