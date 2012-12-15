# CU CS5525
# Fall 2012
# Python Compiler
#
# Makefile
# Makefile to build LaTeX documents
#
# Repository:
#    https://github.com/asayler/CU-CS5525-PythonCompiler
#
# By :
#    Anne Gatchell
#       http://annegatchell.com/
#    Andrew (Andy) Sayler
#       http://www.andysayler.com
#    Michael (Mike) Vitousek
#       http://csel.cs.colorado.edu/~mivi2269/
#
#    Copyright (c) 2012 by Anne Gatchell, Andy Sayler, Mike Vitousek
#    Permission is granted to copy, distribute and/or modify this document
#    under the terms of the GNU Free Documentation License, Version 1.3
#    or any later version published by the Free Software Foundation;
#    with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
#    A copy of the license is included in the COPYING file in this directory.

PROPOSAL_INCLUDES := 
REPORT_INCLUDES   := CompilerFlow.pdf
SLIDES_INCLUDES   := CompilerFlow.pdf

INCLUDE_DIR := include

BIBTEX     ?= bibtex -terse
LATEX      ?= pdflatex -file-line-error
LATEXFIRST ?= -interaction=batchmode
LATEXLAST  ?= -halt-on-error
INKSCAPE   ?= inkscape
CONVERT    ?= convert
CP	   ?= cp

VPATH = $(INCLUDE_DIR)/svg:$(INCLUDE_DIR)/pdf:$(INCLUDE_DIR)/png

.PHONY: all clean cleanall

all: proposal.pdf report.pdf slides.pdf clean

clean:
	$(RM) *.aux *.bbl *.blg *.dvi *.log *.out *.nav *.snm *.toc *.vrb *~
	$(RM) $(INCLUDE_DIR)/*.pdf
	$(RM) *-blx.bib
	$(RM) *.xml

cleanall: clean
	$(RM) proposal.pdf report.pdf slides.pdf

.PHONY: proposal report slides

proposal: proposal.pdf clean

report: report.pdf clean

slides: slides.pdf clean

proposal.pdf: proposal.aux proposal.bbl
	$(LATEX) $(LATEXFIRST) proposal.tex
	$(LATEX) $(LATEXLAST) proposal.tex
	@touch $^ $@

report.pdf: report.aux report.bbl
	$(LATEX) $(LATEXFIRST) report.tex
	$(LATEX) $(LATEXLAST) report.tex
	@touch $^ $@

slides.pdf: slides.aux slides.bbl
	$(LATEX) $(LATEXFIRST) slides.tex
	$(LATEX) $(LATEXLAST) slides.tex
	@touch $^ $@

proposal.bbl: proposal.aux refs.bib
	$(BIBTEX) $<

report.bbl: report.aux refs.bib
	$(BIBTEX) report.aux

slides.bbl: slides.aux refs.bib
	$(BIBTEX) slides.aux

proposal.aux: proposal.tex $(PROPOSAL_INCLUDES)
	$(LATEX) $(LATEXFIRST) $<

report.aux: report.tex $(REPORT_INCLUDES)
	$(LATEX) $(LATEXFIRST) $<

slides.aux: slides.tex $(SLIDES_INCLUDES)
	$(LATEX) $(LATEXFIRST) $<

%.pdf:%-src.svg
	$(INKSCAPE) $< -D --export-pdf=$(INCLUDE_DIR)/$@

%.pdf:%-src.pdf
	$(CP) $< $(INCLUDE_DIR)/$@

%.pdf:%-src.png
	$(CONVERT) $< $(INCLUDE_DIR)/$@
