# File: Makefile
#
# By: Andy Sayler <www.andysayler.com>
# In association with:
#   Michael (Mike) Vitousek
#     https://github.com/mvitousek/python-compiler-mmv
#   Anne Gatchell
#     https://github.com/halloannielala/compiler-5525
#
# CU CS 5525 - Compilers
# Creation Date: 2012/09/06
#
# Description:
#     This is the Makefile for the compiler test files

CC = gcc
PC = ./compile.py
CP = cp
MV = mv
CD = cd

CFLAGS  = -c -m32 -g
LFLAGS  = -m32 -g
PCFLAGS = #-v 0 --dot

SUBMISSIONDIR = ./submission/
HELPERDIR = ./helper/
BUILDDIR = ./build/
TESTDIR = ./test/

TESTCASESSOURCE = $(wildcard $(TESTDIR)*.py)
TESTCASESINPUT  = $(patsubst %.py,           %.in,           $(TESTCASESSOURCE))
TESTCASESASSEMB = $(patsubst $(TESTDIR)%.py, $(BUILDDIR)%.s, $(TESTCASESSOURCE))
TESTCASES       = $(patsubst $(BUILDDIR)%.s, $(BUILDDIR)%.out,  $(TESTCASESASSEMB))
TESTDIFFS       = $(patsubst $(BUILDDIR)%.out, $(BUILDDIR)%.diff, $(TESTCASES))
TESTTEST        = $(patsubst $(BUILDDIR)%.s, $(BUILDDIR)%.test, $(TESTCASESASSEMB))

.PHONY: all clean Tests TestsRun

all: Tests

Assemb: $(TESTCASESASSEMB)

Tests: $(TESTCASES)

TestsRun: $(TESTDIFFS)
	cat $^

$(TESTTEST): %.test: %.s
	echo $*
	echo $(*F)
	echo $(*)

$(TESTDIFFS): $(BUILDDIR)%.diff: $(BUILDDIR)%.out $(TESTDIR)%.in
	cat $(TESTDIR)$*.in | $(BUILDDIR)$*.out > $(BUILDDIR)$*.output
	cat $(TESTDIR)$*.in | $(TESTDIR)$*.py > $(BUILDDIR)$*.correct
	diff -B -s -q $(BUILDDIR)$*.output $(BUILDDIR)$*.correct > $@

$(BUILDDIR)%.out: $(BUILDDIR)%.s $(BUILDDIR)runtime.o $(BUILDDIR)hashtable.o $(BUILDDIR)hashtable_utility.o $(BUILDDIR)hashtable_itr.o
	$(CC) $(LFLAGS) $^ -lm -o $@

$(TESTCASESASSEMB): $(BUILDDIR)%.s: $(TESTDIR)%.py *.py
	$(PC) $(PCFLAGS) $<
	$(MV) $(@F) $(BUILDDIR)

$(BUILDDIR)runtime.o: $(HELPERDIR)runtime.c $(HELPERDIR)runtime.h
	$(CC) $(CFLAGS) $< -o $@

$(BUILDDIR)hashtable.o: $(HELPERDIR)hashtable.c $(HELPERDIR)hashtable.h
	$(CC) $(CFLAGS) $< -o $@

$(BUILDDIR)hashtable_itr.o: $(HELPERDIR)hashtable_itr.c $(HELPERDIR)hashtable_itr.h 
	$(CC) $(CFLAGS) $< -o $@

$(BUILDDIR)hashtable_utility.o: $(HELPERDIR)hashtable_utility.c $(HELPERDIR)hashtable_utility.h
	$(CC) $(CFLAGS) $< -o $@

submission:
	$(RM) -r $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	$(CP) *.py $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)* $(SUBMISSIONDIR)
	$(CD) $(SUBMISSIONDIR); zip -r ../submit.zip *
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(TESTCASES)
	$(RM) $(BUILDDIR)*.o
	$(RM) $(BUILDDIR)*.out
	$(RM) $(BUILDDIR)*.s
	$(RM) $(BUILDDIR)*.output
	$(RM) $(BUILDDIR)*.correct
	$(RM) $(BUILDDIR)*.diff
	$(RM) *~
	$(RM) $(TESTDIR)*~
	$(RM) $(BUILDDIR)*~
	$(RM) $(HELPERDIR)*~
	$(RM) \#*\#
	$(RM) *.s
	$(RM) *.pyc
	$(RM) *.out
	$(RM) *.dot
	$(RM) *.svg
	$(RM) *.jpg
	$(RM) submit.zip
	$(RM) -r $(SUBMISSIONDIR)
