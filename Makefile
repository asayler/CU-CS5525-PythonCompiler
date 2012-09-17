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

CFLAGS = -c -m32 -g
LFLAGS = -m32 -g

SUBMISSIONDIR = ./submission/
HELPERDIR = ./helper/
PLYDIR = ./ply/
BUILDDIR = ./build/
TESTDIR = ./test/

P0TESTDIR = $(TESTDIR)p0/
P0BUILDDIR = $(BUILDDIR)

P0TESTCASESSOURCE = $(wildcard $(P0TESTDIR)*.py)
P0TESTCASESINPUT  = $(wildcard $(P0TESTDIR)*.in)
P0TESTCASESASSEMB = $(patsubst $(P0TESTDIR)%.py, $(P0BUILDDIR)%.s, $(P0TESTCASESSOURCE))
P0TESTCASES = $(patsubst $(P0BUILDDIR)%.s, $(P0BUILDDIR)%.out,  $(P0TESTCASESASSEMB))
P0TESTDIFFS = $(patsubst $(P0BUILDDIR)%.s, $(P0BUILDDIR)%.diff, $(P0TESTCASESASSEMB))

.PHONY: all clean Tests TestsRun P0TestsRun P0Tests 

all: Tests

Tests: P0Tests

TestsRun: P0TestsRun

P0Tests: $(P0TESTCASES)

P0TestsRun: $(P0TESTDIFFS)
	echo $(P0TESTDIFFS)
	cat $(P0BUILDDIR)*.diff

$(P0TESTDIFFS): $(P0BUILDDIR)%.diff: $(P0TESTDIR)%.py $(P0BUILDDIR)%.out $(P0TESTDIR)%.in
	cat $(P0TESTDIR)$*.in | $(P0BUILDDIR)$*.out > $(P0BUILDDIR)$*.output
	cat $(P0TESTDIR)$*.in | $(P0TESTDIR)$*.py > $(P0BUILDDIR)$*.correct
	diff -B -s -q $(P0BUILDDIR)$*.output $(P0BUILDDIR)$*.correct > $@

$(P0BUILDDIR)%.out: $(P0BUILDDIR)%.s $(P0BUILDDIR)runtime.o $(P0BUILDDIR)hashtable.o $(P0BUILDDIR)hashtable_itr.o $(P0BUILDDIR)hashtable_utility.o
	$(CC) $(LFLAGS) $^ -lm -o $@

$(P0TESTCASESASSEMB): $(P0BUILDDIR)%.s: $(P0TESTDIR)%.py *.py
	$(PC) $<
	$(MV) $(@F) $(P0BUILDDIR)

$(P0BUILDDIR)runtime.o: $(HELPERDIR)runtime.c $(HELPERDIR)runtime.h
	$(CC) $(CFLAGS) $< -o $@

$(P0BUILDDIR)hashtable.o: $(HELPERDIR)hashtable.c $(HELPERDIR)hashtable.h
	$(CC) $(CFLAGS) $< -o $@

$(P0BUILDDIR)hashtable_itr.o: $(HELPERDIR)hashtable_itr.c $(HELPERDIR)hashtable_itr.h 
	$(CC) $(CFLAGS) $< -o $@

$(P0BUILDDIR)hashtable_utility.o: $(HELPERDIR)hashtable_utility.c $(HELPERDIR)hashtable_utility.h
	$(CC) $(CFLAGS) $< -o $@

submission:
	$(RM) -r $(SUBMISSIONDIR)
	mkdir $(SUBMISSIONDIR)
	$(CP) *.py $(SUBMISSIONDIR)
	$(CP) $(HELPERDIR)* $(SUBMISSIONDIR)
	$(CP) -r $(PLYDIR) $(SUBMISSIONDIR)
	$(CD) $(SUBMISSIONDIR); zip -r ../submit.zip *
	$(RM) -r $(SUBMISSIONDIR)

clean:
	$(RM) $(P0TESTCASES)
	$(RM) $(BUILDDIR)*.o
	$(RM) $(BUILDDIR)*.out
	$(RM) $(BUILDDIR)*.s
	$(RM) $(BUILDDIR)*.output
	$(RM) $(BUILDDIR)*.correct
	$(RM) $(BUILDDIR)*.diff	
	$(RM) *~
	$(RM) *.pyc
	$(RM) *.out
	$(RM) submit.zip
	$(RM) parsetab.py
